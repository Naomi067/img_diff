import os
from enum import Enum
import re

class AppType(Enum):
    # 外观类型枚举
    Hair = 1
    Dress = 2
    Weapon = 3
    Umbrella = 4
    Headdress= 5
    Mask= 6
    Back= 7
    Tails= 8
    HangingOrnaments= 9
    Mount= 10
    Wings= 11
    DevelopWings= 12
    SpecialEffects= 13
    EquipmentEnhanceEffects= 15
    SkillEffects= 16


def isLegalVersion(timestamp):
    # 检查输入版本文件存在
    path = getVersionPath(timestamp)
    if not os.path.exists(path):
        return False
    return True

def getVersionPath(timestamp):
    # 拿到版本对应的图片路径
    folder_name = 'G:/img_diff/tools/AllImages/L32'
    path = folder_name+ '/' + str(timestamp)
    return path

def getApparanceType(appname):
    # 通过外观名称获得外观类型
    result = re.findall(r'\d+([a-zA-Z]+)\d+', appname)
    for i in list(AppType):
        if i.name == result[0]:
            return i.value
    return -1

def getVersionIncludes(timestamp):
    # 获得当前版本包括的外观类型
    path = getVersionPath(timestamp)
    includes = os.listdir(path)
    typelist = list()
    for i in includes:
        i = getApparanceType(i)
        typelist.append(i)
    typelist = set(typelist)
    return typelist

def isComparableVersions(ori,tar):
    # 判断版本包括的外观类型是否相同
    oriset = getVersionIncludes(ori)
    tarset = getVersionIncludes(tar)
    return oriset == tarset

def isClipped(appname):
    # 外观名称判断是不是需要剪裁的类型
    type = getApparanceType(appname)
    if type in {1,5,6}:
        return True
    return False

if __name__ == '__main__':
    # print(getApparanceType('school7Headdress60207'))
    print(getVersionIncludes('1686299097'))
    print(isClipped('school7Weapon60207'))