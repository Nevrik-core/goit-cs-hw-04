from concurrent.futures import ThreadPoolExecutor
import os
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - PID %(process)d - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("log_thread_pool.log"), logging.StreamHandler()])


# Функція для пошуку слів за алгоритмом Боєра-Мура
def boyer_moore_search(text, pat):
    m = len(pat)
    n = len(text)

    if m == 0 or m > n:
        return -1

    bad_char = {char: index for index, char in enumerate(pat)}

    s = 0
    while s <= n - m:
        j = m - 1

        while j >= 0 and pat[j] == text[s + j]:
            j -= 1

        if j < 0:
            return s

        s += max(1, j - bad_char.get(text[s + j], -1))

    return -1


# Функція для пошуку ключового слова в файлі
def search_keyword_in_file(file_path, keyword):
    pid = os.getpid()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            found_at = boyer_moore_search(content, keyword)
            if found_at != -1:
                logging.info(f"[PID {pid}] Keyword '{keyword}' found in {file_path}")
                return (keyword, file_path)
            else:
                logging.info(f"[PID {pid}] Keyword '{keyword}' not found in {file_path}")
                return (keyword, None)
    except FileNotFoundError:
        logging.error(f"[PID {pid}] File not found: {file_path}")
        return (keyword, None)
    except Exception as e:
        logging.error(f"[PID {pid}] Error processing file {file_path}: {e}")
        return (keyword, None)

# Основна функція
def main_multiprocessing_search(file_paths, keywords):
    start_time = time.time()
    found_files = {keyword: [] for keyword in keywords}

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(search_keyword_in_file, file_path, keyword) for keyword in keywords for file_path in file_paths]
        for future in futures:
            keyword, file_path = future.result()
            if file_path:
                found_files[keyword].append(file_path)

    logging.info(f"Execution time: {time.time() - start_time} seconds")
    return found_files

if __name__ == "__main__":
    file_paths = ['file1.txt', 'file2.txt', 'file3.txt']
    keywords = ['windows', 'Висновки', 'Wikipedia']
    found_files = main_multiprocessing_search(file_paths, keywords)

    for keyword, files in found_files.items():
        if files:
            logging.info(f"Keyword '{keyword}' found in files: {', '.join(files)}")
        else:
            logging.info(f"Keyword '{keyword}' not found in any files.")
