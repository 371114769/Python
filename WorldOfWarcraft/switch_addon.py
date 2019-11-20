import os

# 用户名字
NAME1 = "Raytine"
NAME2 = "Any"

# 魔兽世界怀旧服或正式服的根目录
# 把脚本放在根目录的话，不填也行
rootfolder = "E:\\BattleNet\\World of Warcraft\\_classic_"
ROOT_FOLDER = rootfolder or os.path.abspath(__file__)

# 需要备份的文件夹名
TARGET_FOLDERS = ["Interface", "Fonts", "WTF"]


def get_relevent_folder():
    relevent_list = []
    for target in TARGET_FOLDERS:
        relevent_list += [file for file in os.listdir(ROOT_FOLDER) if target in file]
    print(*[f'--"{s}"' for s in relevent_list], sep="\n")
    print()
    return relevent_list


def rename():
    global tonamed
    print("folders before renaming:")
    all_folders = get_relevent_folder()
    has_switch = False

    print("=" * 60)
    for folder in all_folders:
        if NAME1 in folder:
            tonamed = NAME2
        elif NAME2 in folder:
            tonamed = NAME1
        else:
            continue

        if tonamed not in folder:
            has_switch = True
            os.rename(f"{ROOT_FOLDER}\\{folder.split(' ', 1)[0]}", f"{ROOT_FOLDER}\\{folder.split(' ', 1)[0]} - {tonamed}")
            print(f"> switched: {folder.split(' ', 1)[0]:>19} -> {folder.split(' ', 1)[0]} - {tonamed}")
            os.rename(f"{ROOT_FOLDER}\\{folder}", f"{ROOT_FOLDER}\\{folder.split(' ', 1)[0]}")
            print(f"> renamed: {folder:>19} --> {folder.split(' ', 1)[0]}")
    if not has_switch:
        print(f"Already prepared for user: {tonamed}")
    print("=" * 60)
    print()

    return has_switch


if rename():
    print(f"folders for {tonamed} after renamed:")
    get_relevent_folder()
print("Success")
print()

input("[press enter to leave]")
