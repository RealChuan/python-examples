# Desc: Get host information
# Usage: python host_info.py www.baidu.com

import socket
import sys


class HostInfo(object):
    def __init__(self, host):
        self.host = host

    def get_host_info(self):
        try:
            info = socket.getaddrinfo(self.host, None)
            print("IPV4 address:")
            for i in info:
                if i[0] == socket.AF_INET:
                    print(i[4][0])
            print("IPV6 address:")
            for i in info:
                if i[0] == socket.AF_INET6:
                    print(i[4][0])
            print("Hostname:")
            for i in info:
                print(i[2])
            print("Alias:")
            for i in info:
                print(i[1])
            print("Address list:")
            for i in info:
                print(i[4])
        except socket.gaierror as e:
            print("Error: {}".format(e))


def usage():
    print("Usage: python host_info.py <host>")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    host = sys.argv[1]
    host_info = HostInfo(host)
    host_info.get_host_info()
