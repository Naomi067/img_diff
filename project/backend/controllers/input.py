from qaweb import webapi_blueprint
from qaweb import input_output
from qaweb import get_model_instance
from urllib.parse import quote
from flask import request, Response
from werkzeug.wsgi import FileWrapper
from qaweb import get_file_model

@webapi_blueprint.route("/upload_imag",methods = ["POST"])
@input_output.json_output
def upload_imag(project_id, author, image_version, image_name, image_type):
    """上传图片
    Tags:
        image
    Args:
        project_id(str): 项目id
        image_version(str): 图片版本
        image_name(str): 图片名称
        image_type(str): 图片类型
    Returns:
        str: 图片上传结果
    """
    extra_info = {
        "project_id": project_id,
        "author": author,
    }
    file_info = list(request.files.values())[0]
    grid_fs = get_file_model()
    file_id = grid_fs.add_file(file_info.filename, file_info, extra_info)
    # 这里需要判断下图片是否上传成功
    imag_model = get_model_instance("image_info")
    # image_info需要的信息通过request拿 
    # or 可以通过filename解析出来 
    # or 直接调用接口时传参
    # image_version = request.form.get("image_version")
    # image_name = request.form.get("image_name")
    result = imag_model.add_member(image_version = image_version, image_name = image_name, image_file = file_id,image_type = image_type)
    return True, result

## 下载图片文件
def get_imag_file(file_id):
    grid_fs = get_file_model()
    file_info = grid_fs.get_file(file_id=file_id)
    file_name = quote(file_info.filename)
    content_type = file_info.content_type
    return Response(FileWrapper(file_info), mimetype=content_type,\
        headers={"Content-disposition": f"attachment; filename={file_name};filename*=utf-8''{file_name}"})

## 删除图片文件
def deletle_imag_file(file_id, project_id, author):
    grid_fs = get_file_model()
    file_info = grid_fs.get_file(file_id=file_id)
    if author!= file_info.author or project_id!= file_info.project_id:
        return False
    return grid_fs.del_file(file_id)