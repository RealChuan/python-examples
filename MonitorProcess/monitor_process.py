# -*- coding: utf-8 -*-
"""
监控程序资源使用情况
python monitor_process.py -p <process_name> [-i <interval>] [-d <duration>] [-s <save_path>]
python monitor_process.py --process=<process_name> [--interval=<interval>] [--duration=<duration>] [--save=<save_path>]
参数说明：
-p <process_name>，--process=<process_name>：程序名称
-i <interval>，--interval=<interval>：监控间隔时间，默认为3秒
-d <duration>，--duration=<duration>：监控持续时间，默认为60秒
-s <save_path>，--save=<save_path>：折线图保存路径，默认不保存
"""

import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import getopt


class MonitorProcess:
    def __init__(self, process_name, interval=3, duration=60, save_path=None):
        self.process_name = process_name
        self.interval = interval
        self.duration = duration
        self.save_path = save_path
        self.cpu_percent = []
        self.memory_percent = []
        self.disk_read = []
        self.disk_write = []
        self.time = []
        self.fig = plt.figure(figsize=(10, 8))
        self.ax1 = self.fig.add_subplot(2, 2, 1)
        self.ax2 = self.fig.add_subplot(2, 2, 2)
        self.ax3 = self.fig.add_subplot(2, 2, 3)
        self.ax4 = self.fig.add_subplot(2, 2, 4)
        self.ani = animation.FuncAnimation(
            self.fig, self.update, interval=self.interval * 1000, blit=False
        )
        self.ani_running = True
        plt.show()

    def update(self, i):
        if self.ani_running:
            self.time.append(i)
            self.cpu_percent.append(psutil.cpu_percent())
            self.memory_percent.append(psutil.virtual_memory().percent)
            self.disk_read.append(psutil.disk_io_counters().read_bytes)
            self.disk_write.append(psutil.disk_io_counters().write_bytes)
            self.ax1.clear()
            self.ax1.plot(self.time, self.cpu_percent, color="red")
            self.ax1.set_title("CPU Percent")
            self.ax1.set_xlabel("Time (s)")
            self.ax1.set_ylabel("CPU Percent (%)")
            self.ax2.clear()
            self.ax2.plot(self.time, self.memory_percent, color="green")
            self.ax2.set_title("Memory Percent")
            self.ax2.set_xlabel("Time (s)")
            self.ax2.set_ylabel("Memory Percent (%)")
            self.ax3.clear()
            self.ax3.plot(self.time, self.disk_read, color="blue", label="Read")
            self.ax3.plot(self.time, self.disk_write, color="orange", label="Write")
            self.ax3.set_title("Disk IO")
            self.ax3.set_xlabel("Time (s)")
            self.ax3.set_ylabel("Disk IO (bytes)")
            self.ax3.legend()
            self.ax4.clear()
            self.ax4.plot(self.time, self.cpu_percent, color="red", label="CPU")
            self.ax4.plot(self.time, self.memory_percent, color="green", label="Memory")
            self.ax4.plot(self.time, self.disk_read, color="blue", label="Read")
            self.ax4.plot(self.time, self.disk_write, color="orange", label="Write")
            self.ax4.set_title("All")
            self.ax4.set_xlabel("Time (s)")
            self.ax4.set_ylabel("Percent (%)")
            self.ax4.legend()
            if i >= self.duration:
                self.ani_running = False
                if self.save_path is not None:
                    self.fig.savefig(self.save_path)
                plt.close(self.fig)


def main(argv):
    process_name = ""
    interval = 3
    duration = 60
    save_path = None
    try:
        opts, args = getopt.getopt(
            argv, "hp:i:d:s:", ["help", "process=", "interval=", "duration=", "save="]
        )
    except getopt.GetoptError:
        print(
            "python monitor_process.py -p <process_name> [-i <interval>] [-d <duration>] [-s <save_path>]"
        )
        print(
            "python monitor_process.py --process=<process_name> [--interval=<interval>] [--duration=<duration>] [--save=<save_path>]"
        )
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
                "python monitor_process.py -p <process_name> [-i <interval>] [-d <duration>] [-s <save_path>]"
            )
            print(
                "python monitor_process.py --process=<process_name> [--interval=<interval>] [--duration=<duration>] [--save=<save_path>]"
            )
            sys.exit()
        elif opt in ("-p", "--process"):
            process_name = arg
        elif opt in ("-i", "--interval"):
            interval = int(arg)
        elif opt in ("-d", "--duration"):
            duration = int(arg)
        elif opt in ("-s", "--save"):
            save_path = arg
    if process_name == "":
        print(
            "python monitor_process.py -p <process_name> [-i <interval>] [-d <duration>] [-s <save_path>]"
        )
        print(
            "python monitor_process.py --process=<process_name> [--interval=<interval>] [--duration=<duration>] [--save=<save_path>]"
        )
        sys.exit(2)
    monitor_process = MonitorProcess(process_name, interval, duration, save_path)


if __name__ == "__main__":
    main(sys.argv[1:])
