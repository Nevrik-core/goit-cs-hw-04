# Homework: Keyword Search

## Description

This repository showcases various Python scripts designed for performing keyword searches within text files using different parallel computing approaches: multithreading, multiprocessing, and the `concurrent.futures` module. Each script utilizes the Boyer-Moore search algorithm for efficient keyword detection.

### Search Using Threads

**File**: `hw_threading.py`

This script employs threads to concurrently search for keywords within files. It splits the list of files into chunks, with each chunk processed by a separate thread. The search results are logged to `log_thread_search.log`.

### Search Using Multiprocessing

**File**: `hw_multiprocessing.py`

Leveraging multiprocessing, this script processes each file in a separate process to utilize multiple CPU cores for concurrent execution. The results from each process are combined and logged to `log_multiprocessing.log`.

### Pooling with `concurrent.futures`

**Multiprocessing Pool**

**File**: `multiprocessing_pool.py`

This script uses `ProcessPoolExecutor` from the `concurrent.futures` module to manage a pool of processes for executing the search tasks. It demonstrates a more organized and scalable approach to multiprocessing. The search is performed using the Boyer-Moore algorithm, and results are logged to `log_multi_pool.log`.

**Threading Pool**

**File**: `thread_pool.py`

Similar to the multiprocessing pool script, `thread_pool.py` utilizes `ThreadPoolExecutor` to manage a pool of threads. This is beneficial for I/O-bound tasks and simplifies the management of concurrent execution within threads. The Boyer-Moore algorithm is applied for keyword search, with results logged to `log_thread_pool.log`.
