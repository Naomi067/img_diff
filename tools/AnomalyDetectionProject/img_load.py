import cv2
import os
import numpy as np


class ImageDir:
    # 图片路径处理 根据版本和外观名称拿到对应路径
    def __init__(self,oriversion,tarversion,tarappname):
        self.folder_name = "G:/img_diff/tools/AllImages/L32"
        self.oriversion = oriversion
        self.tarversion = tarversion
        self.tarappname = tarappname
        self.create_folder()
        self.get_apperance_dir(self.tarappname)
    
    def create_folder(self):
        self.oripath = self.folder_name+ '/' + self.oriversion # 基准图片目录
        self.tarpath = self.folder_name+ '/' + self.tarversion # 比较图片目录
        path = self.folder_name + "_result/" +self.tarversion # 比较图片结果目录
        self.save_path = path
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

    def get_apperance_dir(self,apperancename):
        self.oriappdir = self.oripath + '/' + apperancename
        self.tarappdir = self.tarpath + '/' + apperancename
        self.save_path_thresh = self.path_thresh+ '/' + apperancename
        if not os.path.exists(self.save_path_thresh):
            os.makedirs(self.save_path_thresh)
        self.save_path_diff = self.path_diff+ '/' + apperancename
        if not os.path.exists(self.save_path_diff):
            os.makedirs(self.save_path_diff)
        print(self.oriappdir)
        print(self.tarappdir)
        print(self.save_path_diff)
        print(self.save_path_thresh)
        

class img_process():
    # 读取文件夹imgDir下的所有图片输出到imgs=[]中
    def load_file_img(self,imgDir):
        imgs = os.listdir(imgDir)
        imgNum = len(imgs)
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
    imageprocess = ImageDir()