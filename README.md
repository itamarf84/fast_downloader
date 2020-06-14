# fast_downloader
  fast_downloader is a utility package for remote file downloading that contains
  both synchronous and asynchronous support as well as multiprocess.

  The number of resources allocated is set by configurable parameters,
  making it easier to optimize for numerous use-case.

# Key features
  1. downloading a remote file with a single thread.
  2. downloading a remote file as chunks of data with multiprocessing.
  3. downloading a remote file as chunks of data asynchronously.
  4. downloading a remote file as chunks of data with multiprocessing done asynchronously.

# Installation

  Run pip install fast_downloader
  
# Getting started

  SingleThreadDownloaderStrategy.download(URL, LOCAL_FILE_PATH)
  
  
  MultiProcessDownloaderStrategy.download(URL, LOCAL_FILE_PATH)


  async def do(...):
    ...
    
    await AsyncDownloaderStrategy.download(ZIP_FILE_URL, LOCAL_FILE_PATH)...
    
    ...
  
  
  MultiProcessAsyncDownloaderStrategy.download(url=ZIP_FILE_URL, output=LOCAL_FILE_PATH,    number_of_chunks=12,number_of_processes=6) 
  
  
# License
  fast_downloader is offered under the Apache 2 license.
# Requirements
  Puthon >= 3.5.3
# 


