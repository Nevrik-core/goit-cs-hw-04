from multiprocessing import Process, Queue
import logging
import time

# Налаштування логування
logging.basicConfig(level=logging.DEBUG,
                    format=f'%(asctime)s - %(processName)s: %(levelname)s - %(message)s')

# Створення обробника для запису логів у файл
file_handler = logging.FileHandler("log_multiprocessing.log", mode='w')
file_handler.setFormatter(logging.Formatter(f'%(asctime)s - %(processName)s: %(levelname)s - %(message)s'))

# Додавання обробника до логера
logging.getLogger().addHandler(file_handler)


def worker(file_path, keywords, results_queue):
    local_results = {}
    logging.debug(f"Worker started processing: {file_path}")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    logging.debug(f"Keyword '{keyword}' found in {file_path}")
                    if keyword not in local_results:
                        local_results[keyword] = [file_path]
                    elif file_path not in local_results[keyword]:
                        local_results[keyword].append(file_path)
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
    results_queue.put(local_results)


def main_multiprocessing(file_paths, keywords):
    start_time = time.time()
    results_queue = Queue()
    processes = []

    for file_path in file_paths:
        process = Process(target=worker, args=(file_path, keywords, results_queue))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    # Об'єднання результатів
    combined_results = {}
    while not results_queue.empty():
        local_results = results_queue.get()
        for keyword, paths in local_results.items():
            if keyword not in combined_results:
                combined_results[keyword] = paths
            else:
                for path in paths:
                    if path not in combined_results[keyword]:
                        combined_results[keyword].append(path)

    # Виведення результатів
    for keyword, paths in combined_results.items():
        logging.info(f"Keyword '{keyword}' found in files: {', '.join(paths)}")

    logging.info(f"Execution time: {time.time() - start_time} seconds")

if __name__ == '__main__':
    file_paths = ['file1.txt', 'file2.txt', 'file3.txt']
    keywords = ['Wikipedia', 'windows', 'Висновки']
    main_multiprocessing(file_paths, keywords)
