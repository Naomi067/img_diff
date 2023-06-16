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

class ConfirmInfo(ModelBase):
    model_name = "图片确认信息"
    collection_name = "confirm_info"
    fields = {
        "image_name":{
            "name":"图片名称",
            "type":"str",
            "desc":"图片的外观名称",
        },
        "image_version_ori":{
            "name":"图片基准版本",
            "type":"str",
            "desc":"图片基准版本",
        },
        "image_version_tar":{
            "name":"图片对比版本",
            "type":"str",
            "desc":"图片对比版本",
        },
        "image_anomaly":{
            "name":"是否正常图片",
            "type":"bool",
            "desc":"是否正常图片",
            "required":False,
        },
    }
    primary_key = ["image_name", "image_version_ori", "image_version_tar"]
    webapi_cls = WebApiWithoutUpdateCheck

class VersionConfirmInfo(ModelBase):
    model_name = "对比版本已确认信息"
    collection_name = "version_confirm_info"
    fields = {
        "version_ori":{
            "name":"基准版本",
            "type":"str",
            "desc":"基准版本",
        },
        "version_tar":{
            "name":"对比版本",
            "type":"str",
            "desc":"对比版本",
        },
        "version_confirmed":{
            "name":"是否已确认",
            "type":"bool",
            "desc":"是否已确认",
            "required":False,
        },
    }
    primary_key = ["version_ori", "version_tar"]
    webapi_cls = WebApiWithoutUpdateCheck
