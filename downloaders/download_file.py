import asyncio
from abc import ABC, abstractmethod
from math import ceil
import requests
from datetime import datetime
from multiprocessing import Pool, Queue, Process

from downloaders.constants import HTTP_OK, FILE_START
from utils.async_utils import download_multi_chunks
from utils.utils import allocate_out_file, download_range, get_file_size
from settings import logger, CPU_COUNT


class AbstractDownloader(ABC):
    @classmethod
    def download(cls, url, output, number_of_chunks=CPU_COUNT, number_of_processes=CPU_COUNT):
        """
        :param url: The remote file location
        :param output: Path to local copy
        :param number_of_chunks: Split the file to number_of_chunks chunks.
        :param number_of_processes: Split the work to number_of_processes processes
        :return: the result of download done
        """

        chunk_size, file_size, start_time = cls.pre_download(output, url, number_of_chunks)
        res = cls._download(url, output, file_size, chunk_size, number_of_processes)
        cls.post_download(start_time, res)
        return res

    @staticmethod
    def post_download(start_time, res):
        """
        :param start_time: When did the download started (UTC time)
        :param res: Download results
        :return:
        """

        diff = datetime.utcnow() - start_time
        logger.info(f'Finished downloading after {diff}')

    @staticmethod
    def pre_download(output, url, number_of_chunks):
        """
        :param output: Path to local file
        :param url: Remote file location
        :param number_of_chunks: Split the file to number_of_chunks chunks.
        :return: Chunk size to split by
        """

        start_time = datetime.utcnow()
        logger.info(f'Started downloading {start_time}')
        file_size = get_file_size(url)
        chunk_size = ceil(file_size / number_of_chunks)
        allocate_out_file(output, file_size)
        return chunk_size, file_size, start_time

    @staticmethod
    @abstractmethod
    def _download(url, output, file_size, chunk_size, number_of_processes):
        raise NotImplementedError()


class SingleThreadDownloaderStrategy(AbstractDownloader):
    @staticmethod
    def _download(url, output, *args, **kwargs):
        r = requests.get(url, stream=True)
        if r.status_code == HTTP_OK:
            with open(output, 'wb') as f:
                for chunk in r:
                    f.write(chunk)


class MultiProcessDownloaderStrategy(AbstractDownloader):
    @staticmethod
    def _download(url, output, file_size, chunk_size, number_of_processes):
        args = []
        for chunk in range(FILE_START, file_size, chunk_size):
            args.append((url, chunk, chunk + chunk_size - 1, output))
        pool = Pool(number_of_processes)
        pool.starmap(download_range, args)
        pool.close()
        pool.join()


class MultiProcessAsyncDownloaderStrategy(AbstractDownloader):
    @staticmethod
    def _download(url, output, file_size, chunk_size, number_of_processes):
        processes = []
        queues = []
        results = []

        sub_chunk_size = ceil(chunk_size / number_of_processes)
        for chunk in range(FILE_START, file_size, chunk_size):
            queue = Queue()
            p = Process(target=MultiProcessAsyncDownloaderStrategy.download_chunks,
                        args=(queue, str(sub_chunk_size), str(chunk_size), url, output, str(chunk)))
            p.start()

            processes.append(p)
            queues.append(queue)

        for q in queues:
            results.append(q.get())
            q.close()
        for p in processes:
            p.join()
            p.close()
        return results

    @staticmethod
    def download_chunks(q, sub_chunk_size, chunk_size, input, output, chunk):
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(
            download_multi_chunks(int(sub_chunk_size), int(chunk_size), input, output, int(chunk))
        )
        return q.put(res)
