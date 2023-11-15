import cv2
import matplotlib.pyplot as plt
import logging
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='policy_test.log')
import sys
sys.path.append("..")
from config import Config

class histProcess(object):
    def __init__(self, normal_image, compare_image):
        self.image1 = normal_image
        self.image2 = compare_image
        self.matches = self.compare_hist()
        self.get_compare_hist_result()

    def compare_hist(self):
        """直方图比较函数"""
        # 创建第一幅图的rgb三通道直方图（直方图矩阵）
        hist1 = cv2.calcHist([self.image1], [0], None, [256], [0, 255])
        # 创建第二幅图的rgb三通道直方图（直方图矩阵）
        hist2 = cv2.calcHist([self.image2], [0], None, [256], [0, 255])
        # 进行三种方式的直方图比较
        match1 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
        match2 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        match3 = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
        # logger.info("HISTCMP_BHATTACHARYYA: %s, HISTCMP_CORREL: %s, HISTCMP_CHISQR: %s" %(match1, match2, match3))
        return match1, match2, match3

    def get_compare_hist_result(self):
        self.score = self.matches[2]
        if self.matches[2] > Config.COMPARE_HIST_SCORE[2]:
            self.result = False
            return
        self.result = True


if __name__ == '__main__':
    #读取测试图片
    logging.info('----------------------------CompareHist.py--start---------------------------------------')
    first_same = "G:/img_diff/tools/AllImages/L32/1682585756/school7Headdress60099/tick1.jpg"
    second_same = 'G:/img_diff/tools/AllImages/L32/1682670398/school7Headdress60099/tick28.jpg'
    first_dif = "G:/img_diff/tools/AllImages/L32/1682585756/school7Dress120013/tick1.jpg"
    second_dif = "G:/img_diff/tools/AllImages/L32/1682670398/school7Dress120013/tick9.jpg"

    img1=cv2.imread(first_same)
    img11=cv2.imread(second_same)

    img2=cv2.imread(first_dif)#读取测试图片
    img21=cv2.imread(second_dif)

    # cv2.imshow("first_same", img1)
    # cv2.imshow("second_same", img11)
    plt.figure(dpi=120,figsize=(10,7))
    plt.subplot(2,2,1)
    plt.title("first_same")
    plt.plot(cv2.calcHist([img1], [0], None, [256], [0, 255]))
    plt.subplot(2,2,2)
    plt.title("second_same")
    plt.plot(cv2.calcHist([img11], [0], None, [256], [0, 255]))
    hp1 = histProcess(img1, img11)
    print(hp1.result)
    plt.subplot(2,2,3)
    plt.title("first_dif")
    plt.plot(cv2.calcHist([img2], [0], None, [256], [0, 255]))
    plt.subplot(2,2,4)
    plt.title("second_dif")
    plt.plot(cv2.calcHist([img21], [0], None, [256], [0, 255]))
    hp2 = histProcess(img2, img21)
    print(hp2.result)
    plt.savefig('G:/img_diff/tools/AllImages/policy_test/CompareHist.jpg')
    plt.show()
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    logging.info('----------------------------CompareHist.py--end---------------------------------------')