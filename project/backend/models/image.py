from qaweb import ModelBase
from qaweb import WebApiBase

class WebApiWithoutUpdateCheck(WebApiBase):
    def check_can_update(self, old_obj):
        return True, ""

    def check_can_delete(self, data):
        return  True, ""

class ImageInfo(ModelBase):
    model_name = "图片信息"
    collection_name = "image_info"
    fields = {
        "image_version":{
            "name":"图片版本",
            "type":"str",
            "desc":"该图片上传时对应游戏的svn版本",
        },
        "image_name":{
            "name":"图片名称",
            "type":"str",
            "desc":"图片的外观名称",
        },
        "image_type":{
            "name":"图片类型",
            "type":"str",
            "desc":"图片的外观类型",
        },
        "image_anomaly":{
            "name":"异常图片",
            "type":"bool",
            "desc":"图片是否是异常图片",
            "required":False,
        },
        "image_original":{
            "name":"原始图片",
            "type":"bool",
            "desc":"图片是否是原始图片",
            "required":False,
        },
        "image_file":{
            "name":"图片文件id",
            "type":"str",
            "desc":"图片文件id",
        },
    }
    primary_key = ["image_version", "image_name", "image_type"]
    webapi_cls = WebApiWithoutUpdateCheck