import cv2
import matplotlib.pyplot as plt
import numpy as np
import logging
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='policy_test.log')
import sys
sys.path.append("..")
from config import Config

class obrProcess(object):
    def __init__(self, img):
        self.image = img
        self.h, self.w = self.image.shape[:2]
        # print(self.h, self.w )
        self.orb = cv2.ORB_create()
        self.kps,self.desc = self.orb.detectAndCompute(self.image, None)
        self._key_point_to_point()
        self._get_key_point_average()
        # self.get_obr_imgs()

    def get_obr_imgs(self):
        img = self.image.copy()
        self.obr_img = cv2.drawKeypoints(img, self.kps, None, -1, cv2.DrawMatchesFlags_DEFAULT)

    def _key_point_to_point(self):
        # 输入参数为特征点，输出位特征点的坐标
        self.point = np.zeros(len(self.kps) * 2, np.float32)
        for i in range(len(self.kps)):
            self.point[i * 2] = self.kps[i].pt[0]
            self.point[i * 2 + 1] = self.kps[i].pt[1]
        self.point = self.point.reshape(-1, 2)

    def _get_key_point_average(self):
        x_all = 0
        y_all = 0
        for index in self.point:
            x_all += index[0]
            y_all += index[1]
        self.x_ave = x_all/len(self.point)
        self.y_ave = y_all/len(self.point)
        # logging.info("all key points average:{},{}".format(self.x_ave,self.y_ave))
        if self.x_ave < self.w*Config.EDGE_RATIO or self.x_ave > self.w*(1-Config.EDGE_RATIO):
            self.result = False
            logging.info("all key points average:{},{},is effect img:{}".format(self.x_ave,self.y_ave,self.result))
            return
        self.result = True
        logging.info("all key points average:{},{},is effect img:{}".format(self.x_ave,self.y_ave,self.result))


if __name__ == '__main__':
    #读取测试图片
    logging.info('----------------------------obrProcess--start---------------------------------------')
    headdress1 = "G:/img_diff/tools/AllImages/L32/1682585756/school7Headdress60099/tick1.jpg"
    headdress2 = "G:/img_diff/tools/AllImages/L32/1682585756/school7Headdress60019/tick1.jpg"
    dress1 = "G:/img_diff/tools/AllImages/L32/1682670398/school7Dress120093/tick1.jpg"
    dress2 = "G:/img_diff/tools/AllImages/L32/1682670398/school7Dress120126/tick1.jpg"
    dress3 = "G:/img_diff/tools/AllImages/L32/1682670398/school7Dress120144/tick1.jpg"
    dress4 = "G:/img_diff/tools/AllImages/L32/1682670398/school7Dress120145/tick1.jpg"
    

    img1=cv2.imread(headdress1)
    img11=cv2.imread(headdress2)

    img2=cv2.imread(dress1)#读取测试图片
    img21=cv2.imread(dress2)
    img22=cv2.imread(dress4)
    img31=cv2.imread(dress3)

    obr1 = obrProcess(img1)
    obr1.get_obr_imgs()
    obr2 = obrProcess(img11)
    obr3 = obrProcess(img2)
    obr3.get_obr_imgs()
    obr4 = obrProcess(img21)
    obr4.get_obr_imgs()
    obr5 = obrProcess(img22)
    obr6 = obrProcess(img31)
    obr6.get_obr_imgs()
    fig, axes =plt.subplots(nrows=2, ncols=2,dpi=120,figsize=(12,8))
    
    axes[0,0].matshow(cv2.cvtColor(obr1.obr_img,cv2.COLOR_BGR2RGB))
    axes[0,0].set_xlabel(str(int(obr1.x_ave))+' '+str(int(obr1.y_ave)))
    axes[0,1].matshow(cv2.cvtColor(obr3.obr_img,cv2.COLOR_BGR2RGB))
    axes[0,1].set_xlabel(str(int(obr3.x_ave))+' '+str(int(obr3.y_ave)))
    axes[1,0].matshow(cv2.cvtColor(obr4.obr_img,cv2.COLOR_BGR2RGB))
    axes[1,0].set_xlabel(str(int(obr4.x_ave))+' '+str(int(obr4.y_ave)))
    axes[1,1].matshow(cv2.cvtColor(obr6.obr_img,cv2.COLOR_BGR2RGB))
    axes[1,1].set_xlabel(str(int(obr6.x_ave))+' '+str(int(obr6.y_ave)))
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/obr.jpg')
    plt.show()
    plt.figure(dpi=120,figsize=(10,7))
    plt.imshow(cv2.cvtColor(obr4.obr_img,cv2.COLOR_BGR2RGB))
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/obr_dress2.jpg')
    plt.show()

    logging.info('----------------------------obrProcess--end---------------------------------------')