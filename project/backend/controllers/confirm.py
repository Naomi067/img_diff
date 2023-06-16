from qaweb import webapi_blueprint
from qaweb import input_output
from qaweb import get_model_instance
import os
import utils
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMAGES_DIR = os.path.join(BASE_DIR, 'frontend', 'public', 'images')

@webapi_blueprint.route("/set_confirm",methods = ["POST"])
@input_output.json_output
def set_confirm(image_name,image_anomaly,image_version_ori,image_version_tar):
    """
    Tags:
        confirm
    Args:
        image_name(str): 图片名称
        image_anomaly(str): 图片是否为正常图片
        image_version_ori(str): 初始版本
        image_version_tar(str): 对比版本
    Returns:
        str: 格式化好的时间
    """
    # 后面写下存库和更新库
    if image_anomaly == 1:
        image_anomaly = True
    elif image_anomaly == 2:
        image_anomaly = False
    confrim_model = get_model_instance("confirm_info")
    confirm_info = confrim_model.get_all_members(image_name=image_name,image_version_ori=image_version_ori,image_version_tar=image_version_tar)
    confirm_info = list(confirm_info)
    print(confirm_info)
    print(len(confirm_info))
    if confirm_info and len(confirm_info) > 0:
        confirm_info = list(confirm_info)[0]
        print(confirm_info)
        return confrim_model.update_member(_id=confirm_info["_id"],image_anomaly=image_anomaly)
    return confrim_model.add_member(image_name=image_name,image_anomaly=image_anomaly,image_version_ori=image_version_ori,image_version_tar=image_version_tar)

@webapi_blueprint.route("/get_confirm",methods = ["POST"])
@input_output.json_output
def get_confirm(image_name,image_version_ori,image_version_tar):
    confrim_model = get_model_instance("confirm_info")
    confirm_info = confrim_model.get_all_members(image_name=image_name,image_version_ori=image_version_ori,image_version_tar=image_version_tar)
    confirm_info = list(confirm_info)
    if confirm_info and len(confirm_info) > 0:
        confirm_info = list(confirm_info)[0]
        image_anomaly = confirm_info.get("image_anomaly")
        if image_anomaly == True:
            image_anomaly = 1
        elif image_anomaly == False:
            image_anomaly = 2
        return True,image_anomaly


@webapi_blueprint.route("/get_unconfirm_version",methods = ["GET"])
@input_output.json_output
def get_unconfirm_version():
    confrim_version_model = get_model_instance("version_confirm_info")
    data = list()
    for files in os.listdir(IMAGES_DIR):
        version_ori,version_tar,ori_ft, tar_ft = utils.file_to_version(files)
        files_num = len(os.listdir(IMAGES_DIR+'/'+files))
        confrim_version_info = confrim_version_model.get_all_members(version_ori=version_ori,version_tar=version_tar)
        confrim_version_info = list(confrim_version_info)
        if not confrim_version_info or len(confrim_version_info) == 0:
            confrim_version_model.add_member(version_ori=version_ori,version_tar=version_tar,version_confirmed=False)
            data.append({
                "oriinfo":ori_ft,
                "tarinfo":tar_ft,
                "num":files_num
            })                                                                      
        else: 
            confrim_version_info =confrim_version_info[0]
            if not confrim_version_info.get("version_confirmed"):
                data.append({
                    "oriinfo":ori_ft,
                    "tarinfo":tar_ft,
                    "num":files_num
                })
    print(data)
    return True,data

@webapi_blueprint.route("/get_confirmed_version",methods = ["GET"])
@input_output.json_output
def get_confirmed_version():
    confrim_version_model = get_model_instance("version_confirm_info")
    data = list()
    for files in os.listdir(IMAGES_DIR):
        version_ori,version_tar,ori_ft, tar_ft = utils.file_to_version(files)
        files_num = len(os.listdir(IMAGES_DIR+'/'+files))
        confrim_version_info = confrim_version_model.get_all_members(version_ori=version_ori,version_tar=version_tar)
        confrim_version_info = list(confrim_version_info)
        if confrim_version_info and len(confrim_version_info) > 0:
            confrim_version_info =confrim_version_info[0]
            if confrim_version_info.get("version_confirmed"):
                data.append({
                    "oriinfo":ori_ft,
                    "tarinfo":tar_ft,
                    "num":files_num
                })                                                                      
    print(data)
    return True,data

@webapi_blueprint.route("/confirmed_version",methods = ["POST"])
@input_output.json_output
def confirmed_version(image_version_ori,image_version_tar):
    confrim_version_model = get_model_instance("version_confirm_info")
    confrim_version_info = confrim_version_model.get_all_members(version_ori=image_version_ori,version_tar=image_version_tar)
    confrim_version_info = list(confrim_version_info)
    print(confrim_version_info)
    if confrim_version_info and len(confrim_version_info) > 0:
        confrim_version_info = confrim_version_info[0]
        return confrim_version_model.update_member(_id=confrim_version_info["_id"],version_confirmed=True)
    return confrim_version_model.add_member(version_ori=image_version_ori,version_tar=image_version_tar,version_confirmed=True)


