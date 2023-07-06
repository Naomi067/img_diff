from qaweb import api_blueprint,webapi_blueprint
from qaweb import input_output
from qaweb import get_model_instance
from flask import jsonify, request
import time
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMAGES_DIR = os.path.join(BASE_DIR, 'frontend', 'public', 'images')

@api_blueprint.route('/get_version_abnormal_images',methods = ["GET"])
@input_output.json_output
def get_version_abnormal_images():
    version1 = request.args.get('originalVersion')
    version2 = request.args.get('compareVersion')
    dir_name = f"{version1}_{version2}_abnormal"
    dir_path = os.path.join(IMAGES_DIR, dir_name)
    # print("@wangxin7 get_version_abnormal_images {}".format(ans_dir_path))
    images = []
    for filename in os.listdir(dir_path):
        if filename.endswith('.jpg'):
            path = os.path.join(dir_path, filename)
            name = os.path.splitext(filename)[0]
            images.append({"id": len(images) + 1, "name": name, "path": path, "dir_name": dir_name})
    # print("@wangxin7 get_version_abnormal_images {}".format(images))
    dir_name_add = f"{version1}_{version2}_add"
    dir_path_add = os.path.join(IMAGES_DIR, dir_name_add)
    for filename in os.listdir(dir_path_add):
        if filename.endswith('.jpg'):
            path = os.path.join(dir_path_add, filename)
            name = os.path.splitext(filename)[0]
            images.append({"id": len(images) + 1, "name": name, "path": path, "dir_name": dir_name_add})
    return jsonify(images)

@api_blueprint.route('/get_versions',methods = ["GET"])
@input_output.json_output
def get_versions():
    # print("@wangxin7 get_versions {}".format(IMAGES_DIR))
    version_dict = dict()
    ori_version_list=list()
    tar_version_list=list()
    version_set = set()  # 记录已经生成的版本对
    for filename in os.listdir(IMAGES_DIR):
        ori_version = filename.split('_')[0]
        tar_version = filename.split('_')[1]
        version_pair = (ori_version, tar_version)
        if version_pair in version_set:
            continue
        version_set.add(version_pair)
        ori_version_list.append({"id":len(ori_version_list)+1,"name": filename.split('_')[0]})
        tar_version_list.append({"id":len(tar_version_list)+1,"name": filename.split('_')[1]})
    version_dict.update({"ori_version_list":ori_version_list,"tar_version_list":tar_version_list})
    # print("@wangxin7 get_versions 2 {}".format(version_dict))
    return jsonify(version_dict)
