import cv2
import os
import numpy as np
import logging
import shutil
from PIL import Image
from PIL import ImageFile
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='policy_test.log')

class ImageDir:
    # 图片路径处理 根据版本和外观名称拿到对应路径
    def __init__(self,oriversion,tarversion):
        self.folder_name = 'G:/img_diff/tools/AllImages/L32'
        self.oriversion = oriversion
        self.tarversion = tarversion
        self._create_folder()
        self._get_tarappname()
        self._get_template_dir()
        self._get_json_file_dir()
    
    def _create_folder(self):
        self.oripath = self.folder_name+ '/' + self.oriversion # 基准图片目录
        self.tarpath = self.folder_name+ '/' + self.tarversion # 比较图片目录
        path = self.folder_name + "_result/" + self.oriversion+'_'+self.tarversion # 比较图片结果目录
        self.combine_path = path
        floder = os.path.exists(path)
        if not floder:
            os.makedirs(path)
        self.path_thresh = path+"_thresh" # 比较图片结果_阈值
        floder_thresh = os.path.exists(self.path_thresh)
        if not floder_thresh:
            os.makedirs(self.path_thresh)
        self.path_diff = path+ "_diff" # 比较图片结果_diff
        floder_diff = os.path.exists(self.path_diff)
        if not floder_diff:
            os.makedirs(self.path_diff)
        self.path_abnormal = path+ "_abnormal" # 比较图片结果_obnormal
        floder_abnormal = os.path.exists(self.path_abnormal)
        if not floder_abnormal:
            os.makedirs(self.path_abnormal)
        self.path_add = path+ "_add" # 新增图片结果_obnormal
        floder_add = os.path.exists(self.path_add)
        if not floder_add:
            os.makedirs(self.path_add)

    def _get_tarappname(self):        # 预处理2个版本见的可处理外观名称列表
        ori_app_files = os.listdir(self.oripath)
        tar_app_files = os.listdir(self.tarpath)
        self.eff_app_files = list(set(ori_app_files)&set(tar_app_files))
        # print(self.eff_app_files)
        self.add_app_files = list(set(tar_app_files) - set(ori_app_files))
        self.del_app_files = list(set(ori_app_files) - set(tar_app_files))
        if len(self.add_app_files) > 0:
            logging.info("本次有新增外观，请添加基准图片" + str(self.add_app_files))
        if len(self.del_app_files) > 0:
            logging.info("本次未采集到外观，请确认是否已删除 " + str(self.del_app_files))

    def _get_json_file_dir(self):
        # 拿到存储本次对比的结果json文件目录
        json_file_path = self.folder_name + '/json'
        if not os.path.exists(json_file_path):
            os.makedirs(json_file_path)
        self.json_file_name = self.folder_name + '/json/' + self.oriversion+'_'+self.tarversion + '.json'

    def get_apperance_dir(self,apperancename):
        # 根据外观名称获得对应的基准图片和对比图片目录
        self.oriappdir = self.oripath + '/' + apperancename
        #if not os.path.isfile(self.oriappdir):
        #    raise FileNotFoundError("当前外观没有基准图片: " + self.oriappdir)
        self.tarappdir = self.tarpath + '/' + apperancename

    def get_apperance_dir_save(self,apperancename):
        # 根据外观名称获得对应的存储目录
        self.save_path_thresh = self.path_thresh+ '/' + apperancename
        if not os.path.exists(self.save_path_thresh):
            os.makedirs(self.save_path_thresh)
        self.save_path_diff = self.path_diff+ '/' + apperancename
        if not os.path.exists(self.save_path_diff):
            os.makedirs(self.save_path_diff)
        self.save_path = self.combine_path+ '/' + apperancename
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # print(self.oriappdir)
        # print(self.tarappdir)
        # print(self.save_path_diff)
        # print(self.save_path_thresh)

    def copy_apperance_abnormal_dir(self,apperancename):
        # 根据外观名称复制算法结果为异常图片到一个固定的文件夹
        self.get_apperance_dir(apperancename)
        oldpath = self.save_path
        oldimg = os.listdir(oldpath)[0]
        oldpath = oldpath + "/"+ oldimg
        newpath = self.path_abnormal + "/"+ apperancename + "_" + oldimg
        shutil.copy(oldpath, newpath)

    def copy_apperance_add_dir(self):
        # 复制本次对比的版本新增的图片到一个固定的文件夹
        for i in self.add_app_files:
            addpath = self.tarpath + "/" + i
            imglist = os.listdir(addpath)
            img = imglist[0]
            addpath = addpath + "/" + img
            newpath = self.path_add + "/"+ i + "_" + img
            shutil.copy(addpath, newpath)

    def _get_template_dir(self):
        # 这几个是拿到外观类型对应的模板（已废弃不会使用到模板匹配）
        self.template_path = self.folder_name + '/template'

    def get_app_template_file(self,apperancename):
        # 这几个是拿到外观类型对应的模板（已废弃不会使用到模板匹配）
        for i in os.listdir(self.template_path):
            a = i[0:-4]
            if a in apperancename:
                self.template_file = self.template_path+ '/' +i
                # print(self.template_file)
                return self.template_file
        #print('no template!')
        self.template_file = -1

# 载入图片类
class img_process(object):
    def __init__(self):
        pass
    
    def load_file_img(self,imgDir,isTar):
        # 读取文件夹imgDir下的所有图片输出到imgs=[]中
        imgs = os.listdir(imgDir)
        imgNum = len(imgs) if not isTar else 1 # 初始图片全部加载，比较图片只加载一张
        if imgNum == 1:
            self.nowTarIndex = 1
        data = np.empty((imgNum,),dtype=list)
        label = np.empty((imgNum,),dtype=list)
        imagedata = {}
        for i in range(imgNum):
            dir = imgDir+"/"+imgs[i]
            img = cv2.imread(dir)
            """
            r'./person.png'：读取图像的路径
            cv2.IMREAD_GRAYSCALE：将图像转换为单通道灰度图像
            """
            label[i] = imgs[i]
            data[i] = img
            imagedata[imgs[i]]=img
        return imagedata,data,label

    def save_img(self,imgDir,data,label):
        # 将data中的所有图片按照label中的命名保持到文件夹imgDir中
        for i in range(len(data)):
            cv2.imwrite(imgDir+"/"+label[i],data[i])
    
    def reload_file_img(self,imgDir,isTar):
        # 这是的那个预处理过后发现当前图片不符合有效图片要求时，重新读取下一张对比图片
        # 要求必须是只能在已经load_file_img读取过一张图片之后才能使用
        # 只有用来比较的外观才需要这个函数，源外观还是全部读取的
        if not isTar:
            logging.error("only tarapperence can do reload_file_img!")
            return
        if not self.nowTarIndex:
            logging.error("reload_file_img before load_file_img!")
            return
        imgs = os.listdir(imgDir)
        #print(imgs)
        data = np.empty((1,),dtype=list)
        label = np.empty((1,),dtype=list)
        imagedata = {}
        dir = imgDir+"/"+imgs[self.nowTarIndex]
        img = cv2.imread(dir)
        label[0] = imgs[self.nowTarIndex]
        data[0] = img
        imagedata[imgs[self.nowTarIndex]]=img
        self.nowTarIndex = self.nowTarIndex +1
        return imagedata,data,label

# 对比结果上传到web后台
class ImgToWeb(object):
    def __init__(self,img_path):
        self.img_path = img_path
        self._crate_save_path()
        self.compress_rate = 0.5
        self._resize_img()
    
    def _crate_save_path(self):
        self.save_path = "G:/img_diff/project/frontend/public/images"
        folder_name = self.img_path.split('/')[-1]
        print(folder_name)
        self.save_path = self.save_path + '/' + folder_name
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
    
    def _resize_img(self):
        imgs = os.listdir(self.img_path)
        for i in  imgs:
            i_path = self.img_path + '/' + i
            # print(os.path.getsize(i_path))
            i_save_path= self.save_path + '/' + i
            img = cv2.imread(i_path)
            # 双三次插值
            img_resize = cv2.resize(img, (0,0),fx=0.5,fy=0.5,interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(i_save_path, img_resize)
            # print(os.path.getsize(i_save_path))

if __name__ == '__main__':
    oriversion = '1686550161'
    tarversion = '1688457446'
    imageprocess = ImageDir(oriversion,tarversion)
    # for i in imageprocess.eff_app_files:
    #     print(i)
    #     imageprocess.get_apperance_dir(i)

    # i = imageprocess.eff_app_files[1]
    # print(i)
    # imageprocess.get_app_template_file(i)

    # for i in imageprocess.eff_app_files:
    #     print(i)
    #     imageprocess.get_app_template_file(i)
    # imageprocess.get_apperance_dir('school7Headdress60019')
    # img_process = img_process()
    # imgs_2,data_2,label_2 = img_process.load_file_img(imageprocess.tarappdir,True)
    # print(label_2)
    # imgs_2,data_2,label_2 = img_process.reload_file_img(imageprocess.tarappdir,True)
    # print(label_2)
    # imgs_2,data_2,label_2 = img_process.reload_file_img(imageprocess.tarappdir,True)
    # print(label_2)
    #imageprocess.copy_ori_to_ssim('1682585756')
    #imageprocess.copy_apperance_abnormal_dir(i)
    # img_to_web = ImgToWeb('G:/img_diff/tools/AllImages/L32_result/1682585756_1682670398_abnormal')
    # imageprocess.copy_apperance_add_dir()
    # img_to_web = ImgToWeb('G:/img_diff/tools/AllImages/L32_result/1686550161_1688457446_add')
    print(imageprocess.json_file_name)