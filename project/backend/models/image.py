from qaweb import ModelBase

class ImageInfo(ModelBase):
    model_name = "图片信息"
    collection_name = "image_info"
    fields = {
        "image_version":{
            "name":"图片版本",
            "type":"str",
            "name":"该图片上传时对应游戏的svn版本",
        },
        "image_name":{
            "name":"图片名称",
            "type":"str",
            "name":"图片的外观名称",
        },
        "image_type":{
            "name":"图片类型",
            "type":"str",
            "name":"图片的外观类型",
        },
        "image_anomaly":{
            "name":"异常图片",
            "type":"bool",
            "name":"图片是否是异常图片",
        },
        "image_original":{
            "name":"原始图片",
            "type":"bool",
            "name":"图片是否是原始图片",
        },
    }