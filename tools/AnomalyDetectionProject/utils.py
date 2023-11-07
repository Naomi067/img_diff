import os
from enum import Enum
import re
from datetime import datetime, timedelta

DIR_PATH = 'G:/img_diff/tools/AllImages/L32'
DIR_PATH_RESULT = 'G:/img_diff/tools/AllImages/L32_result'

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

def getAllVersions():
    # 拿到版本列表
    dir_list = os.listdir(DIR_PATH)
    dir_list = [d for d in dir_list if os.path.isdir(os.path.join(DIR_PATH, d))]
    return dir_list

def getThisWeekAllReportList():
    # 拿到当周所有报告列表
    target_dirs = []
    name_dirs = []
    output_dirs = []
    for root, dirs, files in os.walk(DIR_PATH_RESULT):
        for dir in dirs:
            if dir.endswith(('_abnormal', '_add')):
                dir_path = os.path.join(root, dir)
                if os.listdir(dir_path) and isNewWeekDay(dir):
                    target_dirs.append(os.path.join(root, dir))
                    output_dirs.append(getResultDirInfo(dir))
                    name_dirs.append(dir)
    return target_dirs,name_dirs,output_dirs


def getResultDirInfo(name_dir):
    # 根据结果目录名称获取对比职业和外观类型信息
    ori_version = name_dir.split('_')[0]
    # tar_version = name_dir.split('_')[1]
    suffixs = name_dir.split('_')[2]
    ori_type = getVersionIncludes(ori_version)
    ori_school = getSchoolIncludes(ori_version)
    # tar_type = getVersionIncludes(tar_version)
    # tar_school = getSchoolIncludes(tar_version)
    return "职业{}外观类型{}-{}:".format(ori_school, ori_type, suffixs)

def isNewWeekDay(result_dir_name):
    # 获取当前日期和本周第一天的日期
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp_str = result_dir_name.split('_')[1]
    timestamp = datetime.fromtimestamp(int(timestamp_str))
    if start_of_week <= timestamp:
        return True
    else:
        return False

def getVersionPath(timestamp):
    # 拿到版本对应的图片路径
    # folder_name = 'G:/img_diff/tools/AllImages/L32'
    path = DIR_PATH+ '/' + str(timestamp)
    return path

def getApparanceType(appname):
    # 通过外观名称获得外观类型
    result = re.findall(r'\d+([a-zA-Z]+)\d+', appname)
    for i in list(AppType):
        if i.name == result[0]:
            return i.value
    return -1

def getSchoolType(appname):
    # 通过外观名称获得外观类型
    result = re.search(r'school(\d+)', appname)
    if result:
        school = result.group(1)
        return school
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

def getSchoolIncludes(timestamp):
    # 获得当前版本包括的外观类型
    path = getVersionPath(timestamp)
    includes = os.listdir(path)
    school = getSchoolType(includes[0])
    return school

def getTotalCount(timestamp):
    # 获得版本原文件目录的数量
    path = getVersionPath(timestamp)
    includes = os.listdir(path)
    return len(includes)

def getTotalCountByResult(result_dir_name):
    # 根据结果目录获得版本原文件目录的数量
    timestamp = result_dir_name.split('_')[1]
    return getTotalCount(timestamp)

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

def compare(score, most_like_score):    
    if isinstance(score, (int, float)):
        return score < most_like_score
    elif isinstance(score, list):
        return any(s < mls for s, mls in zip(score, most_like_score))
    else:
        raise ValueError('Score must be a number or a list of numbers')

def timeFormat(timestamp):
    # 时间戳转化为年-月-日格式的日期
    date = datetime.fromtimestamp(int(timestamp))
    return date.strftime('%Y-%m-%d')  # 输出年-月-日格式的日期

def getAppNameById(id):
    # 想通过id来查外观名字
    pass

if __name__ == '__main__':
    # print(getApparanceType('school7Headdress60207'))
    # print(getVersionIncludes('1686299097'))
    # print(isClipped('school7Weapon60207'))
    # getAppNameById(120083)
    getThisWeekAllReportList()