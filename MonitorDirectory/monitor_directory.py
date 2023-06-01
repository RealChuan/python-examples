import os
import hashlib
import logging
from queue import Queue
import unittest
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


class FileEventHandler(FileSystemEventHandler):
    """
    文件监控事件处理类
    """

    def __init__(self, queue):
        super(FileEventHandler, self).__init__()
        self.queue = queue

    def on_moved(self, event):
        """
        文件移动事件
        :param event:
        :return:
        """
        if event.is_directory:
            logger.info(
                "directory moved from {0} to {1}".format(
                    event.src_path, event.dest_path
                )
            )
        else:
            logger.info(
                "file moved from {0} to {1}".format(event.src_path, event.dest_path)
            )
            self.queue.put((event.src_path, event.dest_path))

    def on_created(self, event):
        """
        文件创建事件
        :param event:
        :return:
        """
        if event.is_directory:
            logger.info("directory created:{0}".format(event.src_path))
        else:
            logger.info("file created:{0}".format(event.src_path))
            self.queue.put((event.src_path, None))

    def on_deleted(self, event):
        """
        文件删除事件
        :param event:
        :return:
        """
        if event.is_directory:
            logger.info("directory deleted:{0}".format(event.src_path))
        else:
            logger.info("file deleted:{0}".format(event.src_path))
            self.queue.put((event.src_path, None))

    def on_modified(self, event):
        """
        文件修改事件
        :param event:
        :return:
        """
        if event.is_directory:
            logger.info("directory modified:{0}".format(event.src_path))
        else:
            logger.info("file modified:{0}".format(event.src_path))
            self.queue.put((event.src_path, None))


class FileMonitor(object):
    """
    文件监控类
    """

    def __init__(self, path):
        self.path = path
        self.observer = Observer()
        self.queue = Queue()
        self.event_handler = FileEventHandler(self.queue)

    def start(self):
        """
        开始监控
        :return:
        """
        self.schedule()
        self.observer.start()

    def schedule(self):
        """
        调度监控事件
        :return:
        """
        self.observer.schedule(self.event_handler, self.path, recursive=True)

    def stop(self):
        """
        停止监控
        :return:
        """
        self.observer.stop()
        self.observer.join()

    def get_change(self):
        """
        获取变化的文件列表
        :return:
        """
        change_list = []
        while True:
            try:
                change = self.queue.get(block=False)
                change_list.append(change)
            except Exception as e:
                break
        return change_list


class FileCompare(object):
    """
    文件比较类
    """

    def __init__(self, path):
        self.path = path
        self.file_list = []
        self.file_dict = {}

    def get_file_list(self):
        """
        获取文件列表
        :return:
        """
        for root, dirs, files in os.walk(self.path):
            for file in files:
                self.file_list.append(os.path.join(root, file))

    def get_file_md5(self, file_path):
        """
        获取文件的md5值
        :param file_path:
        :return:
        """
        md5 = None
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                md5 = hashlib.md5(f.read()).hexdigest()
        return md5

    def get_file_dict(self):
        """
        获取文件字典
        :return:
        """
        for file in self.file_list:
            md5 = self.get_file_md5(file)
            if md5:
                self.file_dict[file] = md5

    def compare(self, file_path):
        """
        比较文件
        :param file_path:
        :return:
        """
        md5 = self.get_file_md5(file_path)
        if md5:
            if file_path in self.file_dict.keys():
                if md5 != self.file_dict[file_path]:
                    return True
            else:
                return True
        return False

    def compare_all(self):
        """
        比较所有文件
        :return:
        """
        change_list = []
        for file in self.file_list:
            if self.compare(file):
                change_list.append((file, None))
        return change_list


class FileChangeHandler(object):
    """
    文件变化处理类
    """

    def __init__(self, path):
        self.path = path
        self.file_monitor = FileMonitor(self.path)
        self.file_compare = FileCompare(self.path)

    def get_change(self):
        """
        获取变化的文件列表
        :return:
        """
        change_list = []
        change_list.extend(self.file_monitor.get_change())
        change_list.extend(self.file_compare.compare_all())
        return change_list

    def start(self):
        """
        开始监控
        :return:
        """
        self.file_monitor.start()

    def stop(self):
        """
        停止监控
        :return:
        """
        self.file_monitor.stop()


class FileChangeHandlerTest(unittest.TestCase):
    """
    文件变化处理类测试类
    """

    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), "test")
        self.file_change_handler = FileChangeHandler(self.path)
        self.file_change_handler.start()

    def tearDown(self):
        self.file_change_handler.stop()

    def test_get_change(self):
        self.file_change_handler.get_change()


if __name__ == "__main__":
    unittest.main()
