__all__ = ['llama_generate', 'Options']

import json
import ctypes
from queue import Queue
from copy import deepcopy
from typing import Iterator
from threading import Thread
from functools import partial

from transformers import AutoTokenizer
from huggingface_hub import hf_hub_download

from .formatter import get_tokenizer, get_special_tokens, format_messages
from .model import Model
from .options import Options, convert_options_to_bytes
from ._llama_cli_cuda_12_5 import lib, ffi


_LLAMA_YIELD_TOKEN_T = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
_LLAMA_SHOULD_STOP_T = ctypes.CFUNCTYPE(ctypes.c_int)


def _llama_yield_token_func(chunk_bytes: bytes, queue=None, callback=None, metadata=None):
    stop_on_special_token = metadata['stop_on_special_token']
    special_tokens = metadata['special_tokens']

    try:
        b: bytes = metadata['prev_chunk_bytes'] + chunk_bytes
        chunk = b.decode()
    except UnicodeDecodeError:
        metadata['prev_chunk_bytes'] += chunk_bytes
        return

    metadata['prev_chunk_bytes'] = b''
    
    if not stop_on_special_token:
        queue.put(chunk)
        return

    # detect stop token
    buffer = metadata['buffer']
    buffer += chunk
    metadata['buffer'] = buffer
    
    subtoken_found = False
    token_found = False
    
    for token in special_tokens:
        for i in range(len(token)):
            subtoken = token[:i + 1]

            # if subtoken in buffer:
            if buffer[-len(subtoken):] == subtoken:
                # print(f'{subtoken = }, {buffer = }')
                subtoken_found = True

                if token in buffer:
                    # print(f'{token = }')
                    index = buffer.index(token)
                    chunk = buffer[:index]
                    buffer = buffer[index + len(token):]
                    metadata['buffer'] = buffer
                    metadata['should_stop'] = True
                    token_found = True
    
    if subtoken_found:
        return

    if token_found:
        return
    
    buffer = metadata['buffer']
    queue.put(buffer)
    metadata['buffer'] = ''


def _llama_should_stop_func(queue=None, callback=None, metadata=None) -> int:
    return 1 if metadata['should_stop'] else 0


def _llama_cli_main(argc, argv, queue=None, callback=None, metadata=None):
    _llama_yield_token = _LLAMA_YIELD_TOKEN_T(partial(_llama_yield_token_func, queue=queue, callback=callback, metadata=metadata))
    _llama_should_stop = _LLAMA_SHOULD_STOP_T(partial(_llama_should_stop_func, queue=queue, callback=callback, metadata=metadata))

    _llama_yield_token_address = ctypes.cast(_llama_yield_token, ctypes.c_void_p).value
    _llama_should_stop_address = ctypes.cast(_llama_should_stop, ctypes.c_void_p).value

    cffi__llama_yield_token_callback = ffi.cast('void (*_llama_yield_token_t)(const char * token)', _llama_yield_token_address)
    cffi__llama_should_stop_callback = ffi.cast('int (*_llama_should_stop_t)(void)', _llama_should_stop_address)

    r = lib._llama_cli_main(argc, argv, cffi__llama_yield_token_callback, cffi__llama_should_stop_callback, 1)
    
    if r != 0:
        queue.put(None)
        return
    
    if queue is not None:
        queue.put(None)
    elif callback is not None:
        callback(None)


def llama_generate(options: Options, callback=None) -> Iterator[str] | None:
    tokenizer: AutoTokenizer
    creator_hf_repo: str
    prompt: str
    queue: Queue | None

    assert options.model and isinstance(options.model, Model)

    options: Options = deepcopy(options)
    model: Model = options.model
    tokenizer = get_tokenizer(model.creator_hf_repo)
    options.model = hf_hub_download(repo_id=model.hf_repo, filename=model.hf_file)

    if isinstance(options.prompt, list):
        options.prompt = format_messages(tokenizer, options.prompt)

    if callback:
        queue = None
    else:
        queue = Queue()

    metadata: dict = {
        'prev_chunk_bytes': b'',
        'buffer': '',
        'stop_on_special_token': True,
        'should_stop': False,
        'special_tokens': get_special_tokens(tokenizer),
    }

    argv: list[bytes] = [b'llama-cli'] + convert_options_to_bytes(options)
    argv = [ffi.new('char[]', n) for n in argv]
    argc = len(argv)

    if callback:
        _llama_cli_main(argc, argv, queue, callback, metadata)
        yield ''
    else:
        t = Thread(target=_llama_cli_main, args=(argc, argv, queue, callback, metadata))
        t.start()

        while True:
            chunk = queue.get()
            queue.task_done()

            if chunk is None:
                break

            yield chunk

        queue.join()
        t.join()
