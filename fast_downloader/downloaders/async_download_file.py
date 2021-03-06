from abc import ABC, abstractmethod
from math import ceil
from datetime import datetime
from typing import Optional, List, Tuple

from fast_downloader.settings import logger, CPU_COUNT
from fast_downloader.utils.async_utils import download_multi_chunks, async_get_file_size, async_allocate_out_file


class AbstractAsyncDownloader(ABC):
    @classmethod
    async def download(cls, url: str, output: str, number_of_chunks: Optional[int] = CPU_COUNT) -> List[Tuple[int, int]]:
        """
        :param url: The remote file location
        :param output: Path to local copy
        :param number_of_chunks: Split the file to number_of_chunks chunks.
        :return: The result of download done
        """

        chunk_size, file_size, start_time = await cls.pre_download(output, url, number_of_chunks)
        res = await cls._download(url, output, file_size, chunk_size)
        await cls.post_download(start_time, res)
        return res

    @staticmethod
    async def post_download(start_time: datetime, res: Optional[List[Tuple[int, int]]]) -> None:
        """
        :param start_time: When did the download started (UTC time)
        :param res: Download results
        :return:
        """
        diff = datetime.utcnow() - start_time
        logger.info(f'Finished downloading after {diff}')

    @staticmethod
    async def pre_download(output: str, url: str, number_of_chunks: int) -> Tuple[int, int, datetime]:
        """
        :param output: Path to local file
        :param url: Remote file location
        :param number_of_chunks: Split the file to number_of_chunks chunks.
        :return: Chunk size to split by
        """

        start_time = datetime.utcnow()
        logger.info(f'Started downloading {start_time}')
        file_size = await async_get_file_size(url)
        chunk_size = ceil(file_size / number_of_chunks)
        await async_allocate_out_file(output, file_size)
        return chunk_size, file_size, start_time

    @staticmethod
    @abstractmethod
    async def _download(url: str, output: str, file_size: int, chunk_size: int) -> List[Tuple[int, int]]:
        raise NotImplementedError()


class AsyncDownloaderStrategy(AbstractAsyncDownloader):
    @staticmethod
    async def _download(url: str, output: str, file_size: int, chunk_size: int) -> List[Tuple[int, int]]:
        res = await download_multi_chunks(chunk_size, file_size, url, output)
        return res
