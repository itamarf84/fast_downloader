# fast_downloader
remote file downloader util api 

The utility supports:
1. downloading remote a file.
2. downloading remote a file as chunks of data with multiprocessing.
3. downloading remote file as chunks of data asynchronously.
4. downloading remote file as chunks of data with multiprocessing done asynchronously.


Example:
  SingleThreadDownloaderStrategy.download(URL, LOCAL_FILE_PATH)...
  MultiProcessDownloaderStrategy.download(URL, LOCAL_FILE_PATH)...

  async def do(...):
    ...
    await AsyncDownloaderStrategy.download(ZIP_FILE_URL, LOCAL_FILE_PATH)...
    ...
  MultiProcessAsyncDownloaderStrategy.download(url=ZIP_FILE_URL, output=LOCAL_FILE_PATH, number_of_chunks=12,number_of_processes=6) 
