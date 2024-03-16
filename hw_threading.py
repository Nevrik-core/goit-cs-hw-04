import threading
from queue import Queue
import logging
import time

# Налаштування логування
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Створення обробника для запису логів у файл
file_handler = logging.FileHandler("log_thread_search.log", mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'))

# Створення обробника для виводу логів в консоль
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'))

# Додавання обох обробників до логера
logger.addHandler(file_handler)
logger.addHandler(stream_handler)



def worker(file_paths, keywords, results, lock):
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        with lock:
                            if keyword not in results:
                                results[keyword] = []
                            results[keyword].append(file_path)
                            logger.info(f"Keyword '{keyword}' found in file: {file_path}")
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")

def main_threading(file_paths, keywords):
    start_time = time.time()
    threads = []
    results = {}
    lock = threading.Lock()

    n = len(file_paths) // 2
    file_paths_chunks = [file_paths[i:i + n] for i in range(0, len(file_paths), n)]

    for chunk in file_paths_chunks:
        thread = threading.Thread(target=worker, args=(chunk, keywords, results, lock))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # Виведення результатів
    for keyword, file_paths in results.items():
        logger.info(f"Keyword '{keyword}' found in files: {', '.join(file_paths)}")

    logger.info(f"Execution time: {time.time() - start_time} seconds")

if __name__ == '__main__':
    file_paths = ['file1.txt', 'file2.txt', 'file3.txt']
    keywords = ['Wikipedia', 'windows', 'Висновки']
    main_threading(file_paths, keywords)
