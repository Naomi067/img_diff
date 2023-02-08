from qaweb import webapi_blueprint
from qaweb import input_output
from qaweb import get_model_instance
import time

@webapi_blueprint.route("/get_time",methods = ["POST"])
@input_output.json_output
def get_time(time_seconds = None):
    """获取格式化时间
    Tags:
        time
    Args:
        time_seconds(str, optional): 时间戳，没有时默认当前时间
    Returns:
        str: 格式化好的时间
    """
    time_seconds = time_seconds or time.time()
    return True, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_seconds))


@webapi_blueprint.route("/get_imag_by_name",methods = ["POST"])
@input_output.json_output
def get_imag_by_name(name):
    """根据图片名称来搜索图片
    Tags:
        image
    Args:
        name(str): 图片名称
    """
    imag_model = get_model_instance("image_info")
    return True, imag_model.get_all_members(image_name = name)


