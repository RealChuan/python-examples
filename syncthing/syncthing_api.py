import requests
import time
import json


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return "%3.2f %s" % (num, x)
        num /= 1024.0


class SyncthingApi:
    def __init__(self, deviceId, apikey, url, folder):
        self.deviceId = deviceId
        self.apikey = apikey
        self.url = url
        self.folder = folder
        self.header = {"X-API-Key": apikey}

        self.localBytes = 0
        self.globalBytes = 0
        self.inSyncBytes = 0
        self.needBytes = 0

        self.currentMilliSeconds = 0

    def getDBStatus(self):
        response = requests.get(
            self.url + "/rest/db/status",
            headers=self.header,
            params={"folder": self.folder},
        )
        if response.status_code == 200:
            return response.json()
        else:
            print("db/status Error: " + str(response.status_code) + " " + response.text)
            return None

    def getFolderStatus(self):
        # `/rest/db/status`接口来获取文件夹的状态，包括`state`, `stateChanged`等信息¹。这个接口返回的数据中，`state`表示文件夹的当前状态，可能的值有`idle`, `scanning`, `cleaning`, `syncing`, `error`, `unknown`²。`stateChanged`表示文件夹状态最后一次改变的时间²
        status = self.getDBStatus()
        if status is None:
            return

        # Extract the relevant values
        state = status["state"]
        stateChanged = status["stateChanged"]

        # Print the result
        print("The current state of the folder is", state)
        print("The folder state last changed at", stateChanged)

    def getFolderSyncedSize(self):
        # 获取已完成同步大小和文件夹总大小，`/rest/db/status`接口来获取文件夹的状态，包括`globalBytes`, `localBytes`, `inSyncBytes`, `needBytes`等信息¹。这个接口返回的数据中，`globalBytes`表示文件夹的总大小，`inSyncBytes`表示已完成同步的大小¹。
        status = self.getDBStatus()
        if status is None:
            return

        # Extract the relevant values
        globalBytes = status["globalBytes"]
        inSyncBytes = status["inSyncBytes"]

        # Print the result
        print("The total size of the folder is", convert_bytes(globalBytes))
        print(
            "The size of the folder that has been synced is",
            convert_bytes(inSyncBytes),
        )

    def getFolderFileNum(self):
        # `/rest/db/need`接口来获取文件夹中需要同步的文件列表¹。这个接口返回的数据中包含了`progress`, `queued`, `rest`三个数组，分别表示正在同步的文件，等待同步的文件，和其他需要同步的文件¹。您可以计算这三个数组的长度之和，就是未上传和下载的文件个数
        response = requests.get(
            self.url + "/rest/db/need",
            headers=self.header,
            params={"folder": self.folder},
        )
        if response.status_code == 200:
            need = response.json()

            # Extract the relevant arrays
            progress = need["progress"]
            queued = need["queued"]
            rest = need["rest"]

            # Calculate the file count
            file_count = len(progress) + len(queued) + len(rest)

            # Print the result
            print("The number of files that need to be synced is", file_count)
        else:
            print("db/need Error: " + str(response.status_code) + " " + response.text)

    def getFolderSpeed(self):
        # Get the folder status and completion
        status = self.getDBStatus()
        if status is None:
            return

        response = requests.get(
            self.url + "/rest/db/completion",
            headers=self.header,
            params={"folder": self.folder, "device": self.deviceId},
        )
        if response.status_code != 200:
            print(
                "db/completion Error: "
                + str(response.status_code)
                + " "
                + response.text
            )
            return

        completion = response.json()

        # Extract the relevant values
        localBytes = status["localBytes"]
        inSyncBytes = status["inSyncBytes"]
        globalBytes = completion["globalBytes"]
        needBytes = completion["needBytes"]

        currentMilliSeconds = int(round(time.time() * 1000))
        timeDiff = currentMilliSeconds - self.currentMilliSeconds

        if self.currentMilliSeconds > 0:
            if timeDiff < 1000:
                return
            else:
                speed = (
                    abs(
                        (localBytes - inSyncBytes)
                        - (self.localBytes - self.inSyncBytes)
                    )
                    / timeDiff
                    * 1000
                )
                speed2 = (
                    abs((globalBytes - needBytes) - (self.globalBytes - self.needBytes))
                    / timeDiff
                    * 1000
                )
                print(
                    "The sync speed between local and remote device is",
                    convert_bytes(speed),
                    "per second",
                )
                print(
                    "The sync speed on remote device is",
                    convert_bytes(speed2),
                    "per second",
                )

        self.localBytes = localBytes
        self.globalBytes = globalBytes
        self.inSyncBytes = inSyncBytes
        self.needBytes = needBytes
        self.currentMilliSeconds = currentMilliSeconds

    def getDbBrowse(self):
        response = requests.get(
            self.url + "/rest/db/browse",
            headers=self.header,
            params={"folder": self.folder},
        )
        if response.status_code == 200:
            browse = response.json()
            print("The browse is", json.dumps(browse, indent=4, sort_keys=True))
        else:
            print("db/browse Error: " + str(response.status_code) + " " + response.text)

    def getConfigFolders(self):
        response = requests.get(self.url + "/rest/config/folders", headers=self.header)
        if response.status_code == 200:
            folders = response.json()
            print("The folders are", json.dumps(folders, indent=4, sort_keys=True))
        else:
            print(
                "config/folders Error: "
                + str(response.status_code)
                + " "
                + response.text
            )

    def getSystemlog(self):
        response = requests.get(
            self.url + "/rest/system/log",
            headers=self.header,
            params={"since": 0, "limit": 1},
        )
        if response.status_code == 200:
            log = response.json()
            print("The last log is", json.dumps(log, indent=4, sort_keys=True))
        else:
            print(
                "system/log Error: " + str(response.status_code) + " " + response.text
            )

    def postSystemReset(self):
        response = requests.post(
            self.url + "/rest/system/reset",
            headers=self.header,
            data={"folder": self.folder},
        )
        if response.status_code == 200:
            print("The system reset is successful")
        else:
            print(
                "system/reset Error: " + str(response.status_code) + " " + response.text
            )

    def getEvents(self, event):
        response = requests.get(
            self.url + "/rest/events",
            headers=self.header,
            params={"events": event, "since": 0, "limit": 1},
        )
        if response.status_code == 200:
            events = response.json()
            print("The last event is", json.dumps(events, indent=4, sort_keys=True))
        else:
            print("events Error: " + str(response.status_code) + " " + response.text)

    def getEventsDisk(self):
        response = requests.get(
            self.url + "/rest/events/disk",
            headers=self.header,
            params={"since": 0, "timeout": 10, "limit": 1},
        )
        if response.status_code == 200:
            events = response.json()
            print("The last event is", json.dumps(events, indent=4, sort_keys=True))
        else:
            print("events Error: " + str(response.status_code) + " " + response.text)


if __name__ == "__main__":
    deviceId = "S5YAD7T-2SF4QQI-67J7EV6-JWNPPB6-FDHIGNI-QNLNDRO-NOOGGDU-BYI4FAN"
    apikey = "QfwYDE2yXj9ysgXWgNNUN6QYkJ95gLoQ"
    url = "http://localhost:8384"
    folder = "eyJ1aWQiOjEwMDEsInVuYXNfZGV2aWNlSUQiOiIzVEE2R1pLLTVTTU5IUFAtRFNTVEtFSS1JSU5URUZULVpUVFFaUVctM0VER0pMWS1OMkhDQ0xXLTQzWE5RQVUiLCJjbGllbnRfZGV2aWNlSUQiOiJTNVlBRDdULTJTRjRRUUktNjdKN0VWNi1KV05QUEI2LUZESElHTkktUU5MTkRSTy1OT09HR0RVLUJZSTRGQU4iLCJ1bmFzcGF0aCI6IlwvbW50XC9uYXNcL2RhdGFcL2hvbWVzXC9hZG1pblwvdS1kcml2ZVwvdGVzdF8xIiwibG9jYWxwYXRoIjoiQzpcL1VzZXJzXC9GWFlcL0Rvd25sb2Fkc1wvVS1Ecml2ZS1URVNUXC8xIiwidXNlcm5hbWUiOiJhZG1pbiIsImNsaWVudHVzZXJuYW1lIjoiIn0="
    sleepTime = 5

    syncApi = SyncthingApi(deviceId, apikey, url, folder)

    while True:
        syncApi.getFolderStatus()
        syncApi.getFolderSyncedSize()
        syncApi.getFolderFileNum()
        syncApi.getFolderSpeed()
        syncApi.getDbBrowse()
        syncApi.getConfigFolders()
        syncApi.getSystemlog()
        syncApi.postSystemReset()
        syncApi.getEventsDisk()
        syncApi.getEvents("FolderScanProgress")

        time.sleep(sleepTime)

        print(
            "----------------",
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "----------------",
        )
