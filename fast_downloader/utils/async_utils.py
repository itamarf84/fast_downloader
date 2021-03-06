import asyncio
from typing import Optional, Tuple, List

import requests
import aiofiles
from aiohttp import request as areq

from fast_downloader.settings import logger
from fast_downloader.utils.constants import BUFFER_START, BUFFER_SIZE


async def async_allocate_out_file(output, size) -> None:
    async with aiofiles.open(output, mode="wb") as f:
        f.seek(size - 1)
        f.write(b"\0")


async def async_get_file_size(url: str) -> int:
    async with areq(method='GET', url=url, chunked=True, raise_for_status=True) as headers_resp:
        content_length = headers_resp.headers.get('Content-Length')
        if not content_length:
            content_length = len(headers_resp.content)
    return int(content_length)


async def async_write_chunk(chunk_start: int, chunk_end: int, input: bytes, out: str) -> int:
    input_len = len(input)
    bytes_left_to_write_on_chunk = chunk_end - chunk_start + 1
    bytes_to_write = bytes_left_to_write_on_chunk if bytes_left_to_write_on_chunk < input_len else input_len

    async with aiofiles.open(out, mode='rb+') as out_file:
        partial_input = input[BUFFER_START:bytes_to_write]
        await out_file.seek(chunk_start)
        await out_file.write(partial_input)
    return bytes_to_write


async def async_download_range(url: str, start: int, end: int, output: str, buffer_size: Optional[int] = BUFFER_SIZE) -> Tuple[int, int]:
    headers = {'Range': f'bytes={start}-{end}'}
    place = start
    async with areq(method='GET', url=url, headers=headers, chunked=True, raise_for_status=True, read_until_eof=False) as response:
        async for part in response.content.iter_chunked(buffer_size):
            bytes_written = await async_write_chunk(place, end, part, output)
            place += bytes_written
            if place > end:
                break
    logger.debug(f'finished {start} till {end}')
    return start, end


async def download_multi_chunks(chunk_size: int, input_len: int , input: str, output: str, start: Optional[int] = 0) -> List[Tuple[int, int]]:
    buffer_end = start + input_len
    tasks = [
        async_download_range(
            input,
            chunk,
            min(chunk + chunk_size - 1, buffer_end),
            output)
        for chunk in range(start, buffer_end, chunk_size)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
