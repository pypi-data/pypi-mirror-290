'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2024-08-14 16:53:04
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2024-08-14 17:00:15
FilePath: \python\multithreaded_downloader\downloader\downloader.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from queue import Queue
import requests
import threading
import os
# from utils import ensure_directory_exists

class DownloadThread(threading.Thread):
    def __init__(self, bytes_queue: Queue, url):
        super().__init__(daemon=True)
        self.bytes_queue = bytes_queue
        self.url = url

    def run(self):
        while not self.bytes_queue.empty():
            bytes_range = self.bytes_queue.get()
            headers = {
                "User-Agent": "Mozilla/5.0 ...",
                "Range": f"bytes={bytes_range[1]}"
            }
            try:
                response = requests.get(self.url, headers=headers)
                response.raise_for_status()
                with open(f"files/{bytes_range[0]}.tmp", "wb") as f:
                    f.write(response.content)
            except Exception as e:
                print(f"Failed to download range {bytes_range[1]}: {e}")

def get_file_size(url) -> int:
    response = requests.head(url)
    return int(response.headers['Content-Length'])

def get_thread_download(file_length, copies_count) -> Queue:
    bytes_queue = Queue(copies_count)
    start_bytes = -1
    for i in range(copies_count):
        bytes_size = int(file_length/copies_count) * i
        if i == copies_count - 1:
            bytes_size = file_length
        bytes_length = f"{start_bytes+1}-{bytes_size}"
        bytes_queue.put([i, bytes_length])
        start_bytes = bytes_size
    return bytes_queue

class MultiThreadedDownloader:
    def __init__(self, url, filename, thread_count=8, copies_count=10):
        self.url = url
        self.filename = filename
        self.thread_count = thread_count
        self.copies_count = copies_count

    def create_threads(self, bytes_queue):
        thread_list = []
        for _ in range(self.thread_count):
            thread = DownloadThread(bytes_queue, self.url)
            thread.start()
            thread_list.append(thread)
        for thread in thread_list:
            thread.join()

    def composite_file(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        with open(self.filename, "ab") as final_file:
            for i in range(self.copies_count):
                temp_filename = f"files/{i}.tmp"
                if os.path.exists(temp_filename):
                    with open(temp_filename, "rb") as bytes_f:
                        final_file.write(bytes_f.read())
                    os.remove(temp_filename)
        return self.filename

    def download(self):
        if not os.path.exists('files'):
            os.makedirs('files')
        file_length = get_file_size(self.url)
        copies_queue = get_thread_download(file_length, self.copies_count)
        self.create_threads(copies_queue)
        return self.composite_file()
    
   

# def main():
#     url = "http://img1.baidu.com/it/u=2476325767,3197989021&fm=26&fmt=auto"
#     filename = "downloaded_image.jpg"
#     downloader = MultiThreadedDownloader(url, filename, thread_count=8, copies_count=10)
#     result_file = downloader.download()
#     print(f"Downloaded file: {result_file}")

# if __name__ == '__main__':
#     main()
