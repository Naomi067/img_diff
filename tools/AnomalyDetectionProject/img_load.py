import cv2
import os
import numpy as np
import logging
import shutil
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='ssim_test.log')
import configparser

class ImageDir:
    # 图片路径处理 根据版本和外观名称拿到对应路径
    def __init__(self,oriversion,tarversion):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.copy_ori_to_ssim(oriversion)
        self.copy_ori_to_ssim(tarversion)
        self.folder_name = self.config.get('images', 'folder_name')
        self.oriversion = oriversion
        self.tarversion = tarversion
        #self.tarappname = tarappname
        self._create_folder()
        self._get_tarappname()
        #self.get_apperance_dir(self.tarappname)
    
    def _create_folder(self):
        self.oripath = self.folder_name+ '/' + self.oriversion # 基准图片目录
        self.tarpath = self.folder_name+ '/' + self.tarversion # 比较图片目录
        path = self.folder_name + "_result/" +self.tarversion # 比较图片结果目录
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

    def get_apperance_dir(self,apperancename):
        # 根据外观名称获得对应的目录
        self.oriappdir = self.oripath + '/' + apperancename
        #if not os.path.isfile(self.oriappdir):
        #    raise FileNotFoundError("当前外观没有基准图片: " + self.oriappdir)
        self.tarappdir = self.tarpath + '/' + apperancename
        self.save_path_thresh = self.path_thresh+ '/' + apperancename
        if not os.path.exists(self.save_path_thresh):
            os.makedirs(self.save_path_thresh)
        self.save_path_diff = self.path_diff+ '/' + apperancename
        if not os.path.exists(self.save_path_diff):
            os.makedirs(self.save_path_diff)
        self.save_path = self.combine_path+ '/' + apperancename
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        print(self.oriappdir)
        print(self.tarappdir)
        print(self.save_path_diff)
        print(self.save_path_thresh)

    def _get_tarappname(self):
        # 拿到本次可以比较的外观名称,以list返回
        # tarversion oriversion 的并
        # 在 tarversion 但不在 oriversion，新增外观需要加ori图片
        # 在 oriversion 单不在 tarversion，删除图片 确认误删
        ori_app_files = os.listdir(self.oripath)
        tar_app_files = os.listdir(self.tarpath)
        self.eff_app_files = list(set(ori_app_files)&set(tar_app_files))
        # print(self.eff_app_files)
        self.add_app_files = list(set(tar_app_files) - set(ori_app_files))
        self.del_app_files = list(set(ori_app_files) - set(tar_app_files))
        if len(self.add_app_files) > 0:
            print("本次有新增外观，请添加基准图片")
            logging.info("本次有新增外观，请添加基准图片")
            print(self.add_app_files)
            logging.info(str(self.add_app_files))
        if len(self.del_app_files) > 0:
            print("本次未采集到外观，请确认是否已删除")
            logging.info("本次未采集到外观，请确认是否已删除")
            print(self.del_app_files)
            logging.info(str(self.del_app_files))

    def copy_apperance_abnormal_dir(self,apperancename):
        # 复制不正常图片到一个固定的文件夹
        self.get_apperance_dir(apperancename)
        oldpath = self.save_path
        oldimg = os.listdir(oldpath)[0]
        oldpath = oldpath + "/"+ oldimg
        newpath = self.path_abnormal + "/"+ apperancename + "_" + oldimg
        shutil.copy(oldpath, newpath)

    def copy_ori_to_ssim(self,version):
        # 当autotest采集和ssim计算在同一台机器上时可以这样
        ssimori = self.config.get('images', 'folder_name') + '/' + version
        autotest_ori = self.config.get('common', 'qc_save_path')+ '/' + version
        if not os.path.exists(ssimori):
            os.makedirs(ssimori)
        if not os.path.exists(autotest_ori):
            logging.error("version:{}  autotest_ori images not exist!".format(version))
            return
        for root, dirs, files in os.walk(autotest_ori):
            dir = str(root).replace(str(autotest_ori),"").replace("\\","/") + '/'
            if not os.path.exists(ssimori + dir):
                os.makedirs(ssimori + dir)
                for file in files:
                    src_file = os.path.join(root, file)
                    shutil.copy(src_file, ssimori + dir)
        logging.info("version:{} images copy done!".format(version))
        pass

class img_process():
    # 读取文件夹imgDir下的所有图片输出到imgs=[]中
    def load_file_img(self,imgDir,isTar):
        imgs = os.listdir(imgDir)
        imgNum = len(imgs) if not isTar else 1 # 初始图片全部加载，比较图片只加载一张
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
    # 将data中的所有图片按照label中的命名保持到文件夹imgDir中
    def save_img(self,imgDir,data,label):
        for i in range(len(data)):
            cv2.imwrite(imgDir+"/"+label[i],data[i])


if __name__ == '__main__':
    oriversion = '1682585756'
    tarversion = '1682650225'
    imageprocess = ImageDir(oriversion,tarversion)
    # for i in imageprocess.eff_app_files:
    #     print(i)
    #     imageprocess.get_apperance_dir(i)
    i = imageprocess.eff_app_files[1]
    print(i)
    #imageprocess.copy_ori_to_ssim('1682585756')
    #imageprocess.copy_apperance_abnormal_dir(i)