import requests
import os
from contextlib import closing
import arrow


class Download():
    def __init__(self, url, method='get', dstdir=".", filename=None, **kwarg):
        self.url = url
        self.method = method
        self.filename = filename or url.rsplit('/', 1)[1]
        self.dst = f"{dstdir}/{self.filename}"
        self.start_time = arrow.now()
        self.content_size = 0

        if not self.to_continue(**kwarg):
            self.download(**kwarg)

    def download(self, mode="wb", **kwarg):
        print(f"downloading {self.url}...")
        with closing(requests.request(self.method, self.url, stream=True, **kwarg)) as res:
            # 单次请求最大值, 太小会闪退, 调大的话速度也会更快
            chunk_size = 1024 * 1024
            self.content_size = int(res.headers['content-length'])  # 内容体总大小
            if not self.content_size:
                print(f"Have it Already?\n'{self.dst}'")
                return
            downloaded = 0
            with open(self.dst, mode) as file:
                print(res.iter_content())
                for data in res.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    downloaded += len(data)
                    self.progress(downloaded)
                else:
                    print('\nDone.')
                    print(f"save to '{self.dst}'")

    def to_continue(self, **kwarg):
        if not os.path.exists(self.dst):
            return False
        size = os.path.getsize(self.dst)
        headers = {"Range": f"bytes={size}-"}
        self.download(mode="ab", headers=headers, **kwarg)
        return True

    def progress(self, current):
        percent = round((current / self.content_size) * 100, 2)

        time_used = (arrow.now() - self.start_time).seconds
        speed = round((current / time_used) / 1024, 0) if time_used else 0
        speed = f"{round(speed / 1024, 1)}MB/s" if speed >= 1024 else f"{speed}KB/s"

        content_size_for_show = self.content_size if current <= self.content_size else current

        print(f"\r Downloading：{percent}%({round(current/1024)}KB/{round(content_size_for_show/1024)}KB) {speed}", end=" ")


if __name__ == "__main__":
    url = 'https://raw.githubusercontent.com/ostwalprasad/WordFrequencyPython/master/output/words.txt'
    Download(url, filename="test_download.txt")
