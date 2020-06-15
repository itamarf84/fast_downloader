from typing import Optional, Tuple
import requests

from fast_downloader.settings import logger
from fast_downloader.utils.constants import BUFFER_START, BUFFER_SIZE


def allocate_out_file(output: str, size: int) -> None:
    with open(output, "wb") as f:
        f.seek(size - 1)
        f.write(b"\0")


def get_file_size(url: str) -> int:
    headers_resp = requests.head(url, stream=True)
    headers_resp.raise_for_status()
    content_length = headers_resp.headers.get('Content-length')
    if not content_length:
        content_length = len(headers_resp.content)
    return int(content_length)


def write_chunk(chunk_start: int, chunk_end: int, input: bytearray, out: str) -> int:
    input_len = len(input)
    bytes_left_to_write_on_chunk = chunk_end - chunk_start + 1
    bytes_to_write = bytes_left_to_write_on_chunk if bytes_left_to_write_on_chunk < input_len else input_len
    with open(out, 'rb+') as out_file:
        partial_input = input[BUFFER_START:bytes_to_write]
        out_file.seek(chunk_start)
        out_file.write(partial_input)
    return bytes_to_write


def download_range(url: str, start: int, end: int, output: str, buffer_size: Optional[int] = BUFFER_SIZE) -> Tuple[int, int]:
    headers = {'Range': f'bytes={start}-{end}'}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    place = start
    for part in response.iter_content(buffer_size):
        bytes_written = write_chunk(place, end, part, output)
        place += bytes_written
        if place > end:
            break
    logger.debug(f'finished {start} till {end}')
    return start, end
