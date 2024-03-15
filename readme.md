# Homework: Keyword Search

## Description

This repository contains two Python scripts that perform keyword search within files.

### Search Using Threads

File: `hw_threading.py`

This script utilizes threads to search for keywords within files. It divides the list of files into several chunks and processes each chunk in a separate thread. The search results are output to the `search_log.log` file.

### Search Using Multiprocessing

File: `hw_multiprocessing.py`

This script utilizes multiprocessing to search for keywords within files. Each file is processed in a separate process, and the search results are combined. The search results are output to the `multiprocessing_log.log` file.
