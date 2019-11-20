import zipfile
import os
import getpass
import shutil
import psutil
import win32api


# 魔兽世界怀旧服或正式服的根目录
# 把脚本放在根目录的话，不填也行
rootfolder = "E:\\BattleNet\\World of Warcraft\\_classic_"

# 备份压缩包的文件名，按个人意愿更改
FILE_NAME = f"AddonBackup - {getpass.getuser()}.zip"

# U盘名，如果检测到的话，则复制进U盘里
# 留空则不备份进U盘
FLASH_DEVICE = "SMALL DISK"

# 需要备份的文件夹名
TARGET_FOLDERS = ["Interface", "Fonts", "WTF"]

ROOT_FOLDER = rootfolder or os.path.abspath(__file__)
ZIP_PATH = os.path.join(ROOT_FOLDER, FILE_NAME)


class Folder():
    folders = []
    files_from_all_folders = []
    count_files_from_all_folders = 0
    count_folders_from_all_folders = 0

    def __init__(self, folder):
        print("walking through:", folder)
        self.file_list = []
        self.count_files = 0
        self.count_folders = 0
        self.name = folder
        try:
            self.walkthrough_folder(os.path.join(ROOT_FOLDER, folder))
        except FileNotFoundError:
            print(f"{folder} not found")
            return
        Folder.folders.append(folder)
        Folder.count_files_from_all_folders += self.count_files
        Folder.count_folders_from_all_folders += self.count_folders
        print(f"files: {self.count_files}\nfolders:{self.count_folders}")
        print("")

    def walkthrough_folder(self, path):
        """遍历文件夹"""
        for file in os.listdir(path):
            cur_path = os.path.join(path, file)

            # 统计文件和文件夹数量
            if os.path.isfile(cur_path):
                self.count_files += 1
            elif os.path.isdir(cur_path):
                self.count_folders += 1

            # 遍历子文件夹
            if os.path.isdir(cur_path):
                self.walkthrough_folder(cur_path)

            # 获得每个文件的路径
            self.file_list.append(cur_path)
            Folder.files_from_all_folders.append(cur_path)

    @classmethod
    def backup(cls):
        """打包文件"""
        allfile = len(cls.files_from_all_folders)
        pb = PB(allfile, 'files')
        with zipfile.ZipFile(ZIP_PATH,
                             "w",
                             compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as zf:
            print(f"ZIPPING to {ZIP_PATH}...")
            for index, f in enumerate(cls.files_from_all_folders):
                pb.print(index + 1)
                zf.write(f)
        print("\nZIP completed")


class PB():
    """进度条"""

    def __init__(self, total, unit='KB', div=1, dot=None, start=0):
        self.start = start
        self.unit = unit
        self.div = div
        self.dot = dot
        self.total = round(total / self.div, dot)
        self.justify = len(str(total))

    def print(self, cur):
        cur = round(cur / self.div, self.dot)
        progress = round((cur) / self.total * 20)
        remain = 40 - progress * 2
        print(f"\r[{'█' * progress}{' ' * remain}] {(cur):>{self.justify}}/{self.total} {self.unit}", end="")


def get_small_disk_path():
    """检测目标U盘有无插入"""
    if not FLASH_DEVICE:
        return
    print("Looking for SMALLDISK")
    for d in psutil.disk_partitions():
        if d.opts.find("removable") > -1:
            print(d)
            print(win32api.GetVolumeInformation(d.mountpoint))
            if win32api.GetVolumeInformation(d.mountpoint)[0] == FLASH_DEVICE:
                print("find it!")
                return d.mountpoint


def to_flash():
    """把备份压缩包复制进U盘"""
    disk_mountpoint = get_small_disk_path()
    if not disk_mountpoint:
        return
    dst = os.path.join(disk_mountpoint, FILE_NAME)
    print(f"copying to {dst}")
    size = os.path.getsize(ZIP_PATH)
    pb = PB(size, 'MB', 1024 * 1024, 1)
    shutil.copy2(ZIP_PATH, dst, progress=pb)
    print("\nSuccess")


if __name__ == "__main__":
    for folder in TARGET_FOLDERS:
        f = Folder(folder)
    if Folder.count_files_from_all_folders:
        Folder.backup()
        print("")
        to_flash()
    input("[press enter to exit]")
