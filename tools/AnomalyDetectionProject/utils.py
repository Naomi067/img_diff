import os
from enum import Enum
import re
from datetime import datetime, timedelta

ALLIMAGES_PATH = 'G:/img_diff/tools/AllImage'
DIR_PATH = 'G:/img_diff/tools/AllImages/L32'
DIR_PATH_RESULT = 'G:/img_diff/tools/AllImages/L32_result'
HOME_DIR_PATH = 'G:/img_diff/tools/AllImages/homeImages'
HOME_DIR_PATH_RESULT = 'G:/img_diff/tools/AllImages/homeImages_result'
ORI_VERSION = ["1698894505","1699267487","1699264826"]

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

def getImagePath(homemode):
    # [通用]根据比较类型获得图片路径
    if homemode:
        return HOME_DIR_PATH
    return DIR_PATH

def getPolicy(homemode):
    # [通用]根据比较类型获得算法策略
    if homemode:
        return ['histProcess'],'cutProcess'
    else:
        return ['pHashProcess','histProcess'],'cutProcess'
    
def getMostLikelyScore(policy):
    # [通用]根据算法策略设定分数比较的初始值
    scores = []
    for i in range(0,len(policy)):
        scores.append(99999999)
    return scores # 这个是用来计算最相近的图片分数 初始值需要按照policy来给

def isLegalVersion(timestamp,homemode):
    # [通用]检查输入版本文件存在
    if not homemode:
        path = getVersionPath(timestamp)
        if not os.path.exists(path):
            return False
        return True
    else:
        path = getHomeVersionPath(timestamp)
        if not os.path.exists(path):
            return False
        return True

def getAllVersions():
    # [时装]拿到版本列表
    dir_list = os.listdir(DIR_PATH)
    dir_list = [d for d in dir_list if os.path.isdir(os.path.join(DIR_PATH, d))]
    return dir_list

def getAllHomeVersions():    
    # [家园]拿到版本列表
    dir_list = os.listdir(HOME_DIR_PATH)
    dir_list = [d for d in dir_list if os.path.isdir(os.path.join(HOME_DIR_PATH, d))]
    return dir_list

def getOriVersion():
    # [时装]拿到初始版本
    return ORI_VERSION

def getAllWeekVersions(homemdoe):
    # [时装]拿到所有的本周待比较版本
    dir_list = getAllVersions()
    dir_list = [d for d in dir_list if isLegalVersion(d,homemdoe) and isNewWeekDayTimestamp(d)]
    return dir_list

def getThisWeekAllReportList():
    # [时装]拿到当周所有报告列表
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

def getHomeThisWeekAllReportList():
    # [家园]拿到当周所有报告列表
    target_dirs = []
    name_dirs = []
    output_dirs = []
    for root, dirs, files in os.walk(HOME_DIR_PATH_RESULT):
        for dir in dirs:
            if dir.endswith(('_abnormal', '_add')):
                dir_path = os.path.join(root, dir)
                if os.listdir(dir_path) and isNewWeekDay(dir):
                    target_dirs.append(os.path.join(root, dir))
                    output_dirs.append(timeFormat(dir.split('_')[1]))
                    name_dirs.append(dir)
    return target_dirs,name_dirs,output_dirs


def getResultDirInfo(name_dir):
    # [时装]根据结果目录名称获取对比职业和外观类型信息
    ori_version = name_dir.split('_')[0]
    # tar_version = name_dir.split('_')[1]
    suffixs = name_dir.split('_')[2]
    ori_type = getVersionIncludes(ori_version)
    ori_school = getSchoolIncludes(ori_version)
    # tar_type = getVersionIncludes(tar_version)
    # tar_school = getSchoolIncludes(tar_version)
    return "职业{}外观类型{}-{}:".format(ori_school, ori_type, suffixs)

def isNewWeekDay(result_dir_name):
    # [通用]获取当前日期和本周第一天的日期
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp_str = result_dir_name.split('_')[1]
    timestamp = datetime.fromtimestamp(int(timestamp_str))
    if start_of_week <= timestamp:
        return True
    else:
        return False

def isNewWeekDayTimestamp(timstamp):
    # [通用]获取当前日期和本周第一天的日期
    if timstamp == 'json':
        return False
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp = datetime.fromtimestamp(int(timstamp))
    if start_of_week <= timestamp:
        return True
    else:
        return False

def getVersionPath(timestamp):
    # [时装]拿到版本对应的图片路径
    path = DIR_PATH+ '/' + str(timestamp)
    return path

def getHomeVersionPath(timestamp):
    # [家园]拿到版本对应的图片路径
    path = HOME_DIR_PATH+ '/' + str(timestamp)
    return path

def getApparanceType(appname):
    # [时装]通过外观名称获得外观类型
    result = re.findall(r'\d+([a-zA-Z]+)\d+', appname)
    for i in list(AppType):
        if i.name == result[0]:
            return i.value
    return -1

def getSchoolType(appname):
    # [时装]通过外观名称获得外观类型
    result = re.search(r'school(\d+)', appname)
    if result:
        school = result.group(1)
        return school
    return -1

def getVersionIncludes(timestamp):
    # [时装]获得当前版本包括的外观类型
    path = getVersionPath(timestamp)
    includes = os.listdir(path)
    typelist = list()
    for i in includes:
        i = getApparanceType(i)
        typelist.append(i)
    typelist = set(typelist)
    return typelist

def getSchoolIncludes(timestamp):
    # [时装]获得当前版本包括的外观类型
    path = getVersionPath(timestamp)
    includes = os.listdir(path)
    school = getSchoolType(includes[0])
    return school

def getTotalCount(timestamp):
    # [时装]获得版本原文件目录的数量
    path = getVersionPath(timestamp)
    includes = os.listdir(path)
    return len(includes)

def getHomeTotalCount(timestamp):
    # [家园]获得版本原文件目录的数量
    path = getHomeVersionPath(timestamp)
    includes = os.listdir(path)
    return len(includes)

def getTotalCountByResult(result_dir_name):
    # [时装]根据结果目录获得版本原文件目录的数量
    timestamp = result_dir_name.split('_')[1]
    return getTotalCount(timestamp)

def getHomeTotalCountByResult(result_dir_name):
    # [家园]根据结果目录获得版本原文件目录的数量
    timestamp = result_dir_name.split('_')[1]
    return getHomeTotalCount(timestamp)

def isComparableVersions(ori,tar,homemode):
    # [通用]判断版本包括的外观类型是否相同
    if homemode:
        return True
    oriset = getVersionIncludes(ori)
    tarset = getVersionIncludes(tar)
    return oriset == tarset

def isClipped(appname):
    # [时装]外观名称判断是不是需要剪裁的类型
    type = getApparanceType(appname)
    if type in {1,5,6}:
        return True
    return False

def compare(score, most_like_score):    
    # [通用]比较两个分数
    if isinstance(score, (int, float)):
        return score < most_like_score
    elif isinstance(score, list):
        return any(s < mls for s, mls in zip(score, most_like_score))
    else:
        raise ValueError('Score must be a number or a list of numbers')

def timeFormat(timestamp):
    # [通用]时间戳转化为年-月-日格式的日期
    date = datetime.fromtimestamp(int(timestamp))
    return date.strftime('%Y-%m-%d')  # 输出年-月-日格式的日期

# def getAppNameById(id):
#     # 想通过id来查外观名字
#     pass

if __name__ == '__main__':
    # print(getApparanceType('school7Headdress60207'))
    # print(getVersionIncludes('1686299097'))
    # print(isClipped('school7Weapon60207'))
    # getAppNameById(120083)
    getThisWeekAllReportList()