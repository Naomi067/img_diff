import time
import re
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POLICY_IMAGES_DIR = os.path.join(BASE_DIR, 'tools', 'AllImages', 'L32')

def file_to_version(filename):
    # 根据文件名称解析对比版本和基准版本
    ori_ver = filename.split('_')[0]
    tar_ver = filename.split('_')[1]
    ori_st = time.localtime(int(ori_ver))
    tar_st = time.localtime(int(tar_ver))
    ori_ft = time.strftime('%Y-%m-%d %H:%M:%S', ori_st)
    tar_ft = time.strftime('%Y-%m-%d %H:%M:%S', tar_st)
    ori_ft = ori_ver+' ['+ ori_ft+']'
    tar_ft = tar_ver+' ['+ tar_ft+']'
    return ori_ver,tar_ver,ori_ft, tar_ft

appearance_type_name = {
    '1': ["时装", "发型", "Hair"],
    '2': ["时装", "时装", "Dress"],
    '3': ["时装", "武器", "Weapon"],
    '4': ["时装", "伞", "Umbrella"],
    '5': ["饰品", "头饰", "Headdress"],
    '6': ["饰品", "面饰", "Mask"],
    '7': ["饰品", "背饰", "Back"],
    '8': ["饰品", "尾饰", "Tails"],
    '9': ["饰品", "悬饰", "HangingOrnaments"],
    '10': ["坐骑", "坐骑", "Mount"],
    '11': ["翅膀", "常规", "Wings"],
    '12': ["翅膀", "养成", "DevelopWings"],
    '13': ["光效", "特效", "SpecialEffects"],
    '15': ["光效", "精炼", "EquipmentEnhanceEffects"],
    '16': ["光效", "技能", "SkillEffects"]
}

def image_to_app_type(imageName):
    pattern = r'[a-zA-Z]+\d+([a-zA-Z]+)\d+_[a-zA-Z]+\d+\.jpg'
    match = re.match(pattern, imageName) 
    if match:
        name = match.group(1)
        for key, value in appearance_type_name.items():
            if value[2] == name:
                return f"{value[0]}_{value[1]}"
    else:
        return "未知时装类型"
    
def image_to_app_type_2(imageName):
    pattern = r'[a-zA-Z]+\d+([a-zA-Z]+)\d'
    match = re.match(pattern, imageName) 
    if match:
        name = match.group(1)
        for key, value in appearance_type_name.items():
            if value[2] == name:
                return f"{value[0]}_{value[1]}"
    else:
        return "未知时装类型"

def get_compare_num_all(filename):
    tar_ver = filename.split('_')[1]
    version_dir = POLICY_IMAGES_DIR+'/'+tar_ver
    image_list = os.listdir(version_dir)
    name_list = []
    num = len(image_list)
    for i in image_list:
        name_list.append(image_to_app_type_2(i))
    name_list = str(set(name_list))
    return num,name_list

def is_add_file(filename):
    name_parts = filename.split('_')
    ori_version, tar_version, tag = name_parts
    if tag == 'abnormal':
        return False
    return True

if __name__ == '__main__':
    print(image_to_app_type("school7Tails120043_tick1.jpg"))
    get_compare_num_all("1686299097_1687143091_abnormal")
