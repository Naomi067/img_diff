import os
from enum import Enum
import re
from datetime import datetime, timedelta
from enum import Enum
from config import Config
import cv2

ALLIMAGES_PATH = 'G:/img_diff/tools/AllImage'
DIR_PATH = 'G:/img_diff/tools/AllImages/L32'
DIR_PATH_RESULT = 'G:/img_diff/tools/AllImages/L32_result'
HOME_DIR_PATH = 'G:/img_diff/tools/AllImages/homeImages'
HOME_DIR_PATH_RESULT = 'G:/img_diff/tools/AllImages/homeImages_result'
D21_DIR_PATH = 'G:/img_diff/tools/AllImages/D21'
D21_DIR_PATH_RESULT = 'G:/img_diff/tools/AllImages/D21_result'

class Mode(Enum):
    FASHION = 0
    HOME = 1
    D21 = 2

def getPathByMode(mode):
    # [通用]根据比较类型获得图片路径
    if mode == Mode.HOME:
        return HOME_DIR_PATH
    elif mode == Mode.D21:
        return D21_DIR_PATH
    elif mode == Mode.FASHION:
        return DIR_PATH
    
def getResultPathByMode(mode):
    # [通用]根据比较类型获得图片路径
    if mode == Mode.HOME:
        return HOME_DIR_PATH_RESULT
    elif mode == Mode.D21:
        return D21_DIR_PATH_RESULT
    elif mode == Mode.FASHION:
        return DIR_PATH_RESULT

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

def getPolicy(mode):
    # [通用]根据比较类型获得算法策略
    if mode == Mode.HOME:
        return ['histProcess'],'cutProcess'
    elif mode == Mode.D21:
        return ['histProcess'],'cutProcess'
    elif mode == Mode.FASHION:
        # return ['pHashProcess','histProcess'],'cutProcess'
        return ['histProcess'],'cutProcess'
    
def getSSIMthValue(mode):
    # [算法] 不同模式阈值不同
    if mode == Mode.HOME:
        return  Config.THRESH_ALGRITHON_HOME
    elif mode == Mode.FASHION:
        return Config.THRESH_ALGRITHON
    elif mode == Mode.D21:
        return Config.THRESH_ALGRITHON
    
def getCutValue(mode,img):
    # [算法] 不同模式阈值不同
    h, w = img.shape[:2]
    if mode == Mode.HOME:
        return  img[0:h-Config.HOME_AREA_H_L,Config.HOME_AREA_W:w-Config.HOME_AREA_W]
    elif mode == Mode.FASHION:
        return img[0:h,Config.HEADRESS_AREA:w-Config.HEADRESS_AREA]
    elif mode == Mode.D21:
        return img

def hconcatImg(mode,normalimg,threshimg):
    # [算法] 不同模式拼接图片
    if mode == Mode.HOME or mode == Mode.FASHION:
        return cv2.hconcat([normalimg,threshimg])
    elif mode == Mode.D21:
        return threshimg

def getMostLikelyScore(policy):
    # [通用]根据算法策略设定分数比较的初始值
    scores = []
    for i in range(0,len(policy)):
        scores.append(99999999)
    return scores # 这个是用来计算最相近的图片分数 初始值需要按照policy来给

def getAllVersionMode(mode):
    # [通用]获取所有版本
    path = getPathByMode(mode)
    print(path)
    dir_list = os.listdir(path)
    dir_list = [d for d in dir_list if os.path.isdir(os.path.join(path, d))]
    return dir_list

def getOriVersion(mode):
    # [通用]拿到初始版本
    dir_list = getAllVersionMode(mode)
    if mode == Mode.HOME or mode == Mode.FASHION:
        dir_list = [d for d in dir_list if isLegalVersion(d,mode) and isLastWeekDayTimestamp(d)]
    elif mode == Mode.D21:
        # d21的不同需求是当周的版本来对比
        dir_list = [d for d in dir_list if isLegalVersion(d,mode) and isNewWeekDayTimestamp(d)]
    return dir_list

def getAllWeekVersions(mode):
    # [通用]拿到所有的本周待比较版本
    dir_list = getAllVersionMode(mode)
    dir_list = [d for d in dir_list if isLegalVersion(d,mode) and isNewWeekDayTimestamp(d)]
    return dir_list

def isLegalVersion(timestamp,mode):
    # [通用]检查输入版本文件存在
    path = getVersionPathwithTimestampMode(mode,timestamp)
    if not os.path.exists(path):
        return False
    return True

def getThisWeekAllReportListbyMode(mode):
    if mode == Mode.HOME:
        return getHomeThisWeekAllReportList()
    elif mode == Mode.D21:
        return getD21ThisWeekAllReportList()
    elif mode == Mode.FASHION:
        return getThisWeekAllReportList()

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

def getD21ThisWeekAllReportList():
    # [D21]拿到当周所有报告列表 待修改
    target_dirs = [] # 报告需要的文件列表
    name_dirs = [] # 前端展示的可选文件列表
    output_dirs = [] # 前端展示的可选文件列表的时间戳提示
    ori_dirs = [] # 原始文件列表
    for root, dirs, files in os.walk(D21_DIR_PATH_RESULT):
        for dir in dirs:
            if dir.endswith(('_abnormal')) and isNewWeekDay(dir):
                # dir_path = os.path.join(root, dir)
                # print("getD21ThisWeekAllReportList"+dir_path)
                ori_dirs.append(os.path.join(D21_DIR_PATH,dir.split('_')[0]+'_'+dir.split('_')[1]))
                target_dirs.append(os.path.join(root, dir))
                output_dirs.append(timeFormat(dir.split('_')[-2]))
                name_dirs.append(dir)
    # print(target_dirs,set(ori_dirs),name_dirs,output_dirs)
    ori_dirs = list(set(ori_dirs))
    for i in ori_dirs:
        print(i)
        target_dirs.append(i)
        output_dirs.append(timeFormat(i.split('_')[-1]))
        name_dirs.append(i.split('\\')[-1])
    print(target_dirs,name_dirs,output_dirs)
    return target_dirs,name_dirs,output_dirs

def getResultDirInfo(name_dir):
    # [时装]根据结果目录名称获取对比职业和外观类型信息
    ori_version = name_dir.split('_')[0]
    # tar_version = name_dir.split('_')[1]
    suffixs = name_dir.split('_')[2]
    ori_type = getVersionFashionInfo(ori_version)
    ori_school = getSchoolIncludes(ori_version)
    # tar_type = getVersionFashionInfo(tar_version)
    # tar_school = getSchoolIncludes(tar_version)
    return "职业{}外观类型{}-{}:".format(ori_school, ori_type, suffixs)

def isLastWeekDayTimestamp(timstamp):
    # 获取当前日期和上周第一天的日期
    if timstamp == 'json':
        return False
    timstamp = extractTimestamp(timstamp)
    now = datetime.now()
    start_of_last_week = now - timedelta(days=now.weekday() + 7)
    start_of_last_week = start_of_last_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # 获取本周第一天的日期
    start_of_this_week = now - timedelta(days=now.weekday())
    start_of_this_week = start_of_this_week.replace(hour=0, minute=0, second=0, microsecond=0)

    # 将时间戳转换为 datetime 对象
    timestamp_datetime = datetime.fromtimestamp(int(timstamp))
    # 判断时间戳是否在范围内
    if start_of_last_week <= timestamp_datetime < start_of_this_week:
        return True
    else:
        return False

def isNewWeekDay(result_dir_name):
    # [通用]获取当前日期和本周第一天的日期
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp_str = result_dir_name.split('_')[-2]
    timestamp = datetime.fromtimestamp(int(timestamp_str))
    if start_of_week <= timestamp:
        return True
    else:
        return False

def isNewWeekDayTimestamp(timstamp):
    # [通用]获取当前日期和本周第一天的日期
    if timstamp == 'json':
        return False
    timstamp = extractTimestamp(timstamp)
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp = datetime.fromtimestamp(int(timstamp))
    if start_of_week <= timestamp:
        return True
    else:
        return False

def getVersionPathwithTimestampMode(mode,timestamp):
    # [通用]拿到版本对应的图片路径
    path = getPathByMode(mode)
    path = path+ '/' + str(timestamp)
    return path

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

def getVersionFashionInfo(timestamp):
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

def isComparableVersions(ori,tar,mode):
    # [通用]判断版本包括的外观类型是否相同
    if mode == Mode.FASHION:
        oriset = getVersionFashionInfo(ori)
        tarset = getVersionFashionInfo(tar)
        return oriset == tarset
    return True

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
    # [工具]时间戳转化为年-月-日格式的日期
    date = datetime.fromtimestamp(int(timestamp))
    return date.strftime('%Y-%m-%d')  # 输出年-月-日格式的日期

# def getAppNameById(id):
#     # 想通过id来查外观名字
#     pass

def extractTimestamp(version):
    # [工具]识别提取版本的时间戳
    if re.match(r'^\d+$', version):  # 如果tarversion是纯数字
        timestamp = int(version)
    else:  # 如果tarversion是数值_时间戳的格式
        match = re.search(r'_(\d+)$', version)
        if match:
            timestamp = int(match.group(1))
        else:
            # 在这里处理未匹配到时间戳的情况
            timestamp = None  # 或者抛出异常，根据你的需求
    return timestamp

def getD21ExeType(version):
    if len(version.split('_')) > 2:
        return version.split('_')[2]
    else:
        return version.split('_')[0]
    
def d21ResultDirToOriDir(result_dir_name):
    pattern = r'_([a-zA-Z0-9]+\.exe_\d+)_'
    result = re.search(pattern, result_dir_name)
    if result:
        extracted_part = result.group(1)
        # print(extracted_part)
        return extracted_part
        
if __name__ == '__main__':
    # print(getApparanceType('school7Headdress60207'))
    # print(getVersionFashionInfo('1686299097'))
    # print(isClipped('school7Weapon60207'))
    # getAppNameById(120083)
    # getThisWeekAllReportList()
    # getD21ThisWeekAllReportList()
    d21ResultDirToOriDir("1")