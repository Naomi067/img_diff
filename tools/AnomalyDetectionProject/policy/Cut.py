import cv2
import matplotlib.pyplot as plt
import numpy as np
import logging
import utils
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='policy_test.log')
import sys
sys.path.append("..")
from config import Config

class cutProcess(object):
    def __init__(self, apperancename):
        # self.image = img
        # self.h, self.w = self.image.shape[:2]
        self.apperancename = apperancename
        # self.get_cut_imgs()

    def get_cut_imgs(self, img, mode):
        if img is None:
            return None
        h, w = img.shape[:2]
        #cut_img = img.copy()
        if mode == utils.Mode.HOME:
            img = img[0:h-Config.HOME_AREA_H_L,Config.HOME_AREA_W:w-Config.HOME_AREA_W]
            return img
        img = img[0:h,Config.HEADRESS_AREA:w-Config.HEADRESS_AREA]
        return img


if __name__ == '__main__':
    #读取测试图片
    logging.info('----------------------------obrProcess--start---------------------------------------')
    headdress1 = "G:/img_diff/tools/AllImages/homeImages/1699936298/11298012/1.jpg"
    headdress2 = "G:/img_diff/tools/AllImages/L32/1682585756/school7Headdress60019/tick1.jpg"
    

    img1=cv2.imread(headdress1)
    img11=cv2.imread(headdress2)

    obr1 = cutProcess('school7Headdress60099')
    obr1_cut_img = obr1.get_cut_imgs(img1,utils.Mode.HOME)
    plt.figure(dpi=120,figsize=(10,7))
    plt.imshow(cv2.cvtColor(obr1_cut_img,cv2.COLOR_BGR2RGB))
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/cut_home.jpg')
    plt.show()

    logging.info('----------------------------obrProcess--end---------------------------------------')