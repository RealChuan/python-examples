# -*- coding: utf-8 -*-

import os
import sys
import getopt
import requests
from Crypto.Cipher import AES


class M3U8Downloader:
    def __init__(self, url, save_path, key=None, timeout=30):
        self.url = url
        self.save_path = save_path
        self.key = key
        self.timeout = timeout
        self.ts_list = []
        self.ts_name_list = []
        self.ts_key_list = []
        self.ts_key_name_list = []
        self.ts_key_dict = {}
        self.ts_key_name_dict = {}
        self.ts_key_iv_dict = {}
        self.ts_key_iv_name_dict = {}

    def download(self):
        self.parse_m3u8()
        self.download_ts()
        self.merge_ts()

    def parse_m3u8(self):
        r = requests.get(self.url, timeout=self.timeout)
        if r.status_code != 200:
            print("m3u8下载失败")
            sys.exit(1)
        lines = r.text.split("\n")
        for line in lines:
            if line.startswith("#EXT-X-KEY"):
                self.parse_key(line)
            elif line.startswith("#EXTINF"):
                self.parse_ts(line)

    def parse_key(self, line):
        key = line.split(",")[1].split("=")[1].strip('"')
        if key.startswith("0x"):
            key = key[2:]
            key = bytes.fromhex(key)
        else:
            key = requests.get(key, timeout=self.timeout).content
        self.key = key

    def parse_ts(self, line):
        ts = line.split(",")[1]
        self.ts_list.append(ts)

    def download_ts(self):
        for ts in self.ts_list:
            if self.key:
                self.download_ts_with_key(ts)
            else:
                self.download_ts_without_key(ts)

    def download_ts_with_key(self, ts):
        r = requests.get(ts, timeout=self.timeout)
        if r.status_code != 200:
            print("ts下载失败")
            sys.exit(1)
        ts_data = r.content
        ts_data = self.decrypt_ts(ts_data)
        ts_name = ts.split("/")[-1]
        self.ts_name_list.append(ts_name)
        ts_path = os.path.join(self.save_path, ts_name)
        with open(ts_path, "wb") as f:
            f.write(ts_data)

    def download_ts_without_key(self, ts):
        r = requests.get(ts, timeout=self.timeout)
        if r.status_code != 200:
            print("ts下载失败")
            sys.exit(1)
        ts_data = r.content
        ts_name = ts.split("/")[-1]
        self.ts_name_list.append(ts_name)
        ts_path = os.path.join(self.save_path, ts_name)
        with open(ts_path, "wb") as f:
            f.write(ts_data)

    def decrypt_ts(self, ts_data):
        if self.key:
            if len(self.key) == 16:
                cipher = AES.new(self.key, AES.MODE_CBC, iv=self.key)
            elif len(self.key) == 32:
                cipher = AES.new(self.key, AES.MODE_CBC, iv=self.key[:16])
            else:
                print("key长度不正确")
                sys.exit(1)
            ts_data = cipher.decrypt(ts_data)
        return ts_data

    def merge_ts(self):
        if self.key:
            self.merge_ts_with_key()
        else:
            self.merge_ts_without_key()

    def merge_ts_with_key(self):
        for ts_name in self.ts_name_list:
            ts_path = os.path.join(self.save_path, ts_name)
            with open(ts_path, "rb") as f:
                ts_data = f.read()
            ts_data = self.decrypt_ts(ts_data)
            ts_path = os.path.join(self.save_path, ts_name)
            with open(ts_path, "wb") as f:
                f.write(ts_data)

    def merge_ts_without_key(self):
        with open(self.save_path, "wb") as f:
            for ts_name in self.ts_name_list:
                ts_path = os.path.join(self.save_path, ts_name)
                with open(ts_path, "rb") as f1:
                    ts_data = f1.read()
                f.write(ts_data)


def usage():
    print(
        "Usage: python m3u8_download.py -u <url> -o <output> [-k <key>] [-t <timeout>]"
    )
    print("   -u <url>      m3u8文件的url")
    print("   -o <output>   输出文件路径")
    print("   -k <key>      AES加密的key")
    print("   -t <timeout>  超时时间，默认为30秒")
    print("   -h            帮助")
    print("Example: python m3u8_download.py -u http://example.com/1.m3u8 -o 1.mp4")
    print(
        "         python m3u8_download.py -u http://example.com/1.m3u8 -o 1.mp4 -k 1234567890123456"
    )
    print(
        "         python m3u8_download.py -u http://example.com/1.m3u8 -o 1.mp4 -k http://example.com/1.key"
    )


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:o:k:t:")
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    url = None
    save_path = None
    key = None
    timeout = 30
    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit(0)
        elif opt == "-u":
            url = arg
        elif opt == "-o":
            save_path = arg
        elif opt == "-k":
            key = arg
        elif opt == "-t":
            timeout = int(arg)
    if not url or not save_path:
        usage()
        sys.exit(1)
    m3u8_downloader = M3U8Downloader(url, save_path, key, timeout)
    m3u8_downloader.download()


if __name__ == "__main__":
    main()
