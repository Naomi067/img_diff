from skimage.metrics import structural_similarity as sk_cpt_ssim
import imutils
import cv2
import numpy as np
from config import Config
import logging
import time
DATEFMT ="[%Y-%m-%d %H:%M:%S]"
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT,datefmt=DATEFMT,filename='policy_test.log')

class ssimThreshProcess(object):
    def __init__(self, normal_image, compare_image):
        self.normal_image = normal_image
        self.grayA = cv2.cvtColor(self.normal_image, cv2.COLOR_BGR2GRAY)
        self.compare_image = compare_image
        self.grayB = self._alignImages()
        self.diff,self.score,h,w= self.compare()
        self.thresh_image,self.thresh_same = self._thresh_classify()
        self.score_same = self._score_judge()
        self.thresh_image,self.thresh_same = self._tresh_classify_modify()
        self.result = self.thresh_same and self.score_same
    

    def compare(self):
        (score, diff) = sk_cpt_ssim(self.grayA, self.grayB, data_range=500,full=True,win_size=Config.SSIM_WINSIZE)
        h, w = self.grayA.shape[:2]
        # (score, diff) = sk_cpt_ssim(grayA, grayB,win_size=7,data_range = 10000,full=True)
        # (score, diff) = sk_cpt_ssim(grayA, grayB, full=True)
        return diff,score,h, w

    def _thresh_classify(self):
        # 阈值图片处理
        self.diff = (self.diff * 255).astype("uint8")
        thresh = cv2.threshold(self.diff, Config.THRESH_ALGRITHON, 255,
                                cv2.THRESH_TOZERO_INV)[1]
        thresh_image = thresh
        self.result_image = self.compare_image.copy()
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        diffcount = 0
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if w < Config.THRESH_LIMIT_WIDE or h< Config.THRESH_LIMIT_HIGH:
                continue
            else:
                diffcount = diffcount + 1
                cv2.rectangle(self.result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if diffcount > 0:
            return thresh_image,False
        else:
            return thresh_image,True

    def _tresh_classify_modify(self):
        # 通过计次对阈值结果进行修正
        if self.score_same or not self.thresh_same:
            return self.thresh_image,self.thresh_same
        thresh = cv2.threshold(self.diff, Config.THRESH_ALGRITHON, 255,
                                cv2.THRESH_TOZERO_INV)[1]
        thresh_image = thresh
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        diffcount = 0
        # hcount = 0
        # wcount = 0
        # count = 0
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            # hcount += h
            # wcount += w
            # count += 1
            if w <= Config.DIFF_MODIFY_LIMIT or h<= Config.DIFF_MODIFY_LIMIT:
                continue
            else:
                diffcount = diffcount + 1
                cv2.rectangle(self.result_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        print("diffcount: ",diffcount)
        # print("wcount: ",wcount)
        # print("w平均: ",wcount/count)
        # print("hcount: ",hcount)
        # print("h平均: ",hcount/count)
        if diffcount >= Config.DIFF_COUNT_LIMIT:
            return thresh_image,False
        else:
            return thresh_image,True


    def _score_judge(self):
        # 通过ssim分数判断图片是否异常
        if self.score < Config.SSIM_SCORE_JUDGE:
            self.reult = False
            return False
        else:
            self.reult = True
            return True

    def get_score_classify(self):
        # ssim分数异常
        return self.score_same

    def get_compare_img(self):
        # 比较的图片
        return self.compare_image
    
    def get_result_img(self):
        # 画框后的结果图片
        return self.result_image
    
    def get_normal_img(self):
        # 比较的原图
        return self.normal_image

    def get_diff_img(self):
        # diff图
        diff = (self.diff * 255).astype("uint8")
        diff_color = cv2.applyColorMap(diff, cv2.COLORMAP_HOT)
        return diff_color

    def get_thresh_img(self):
        # 阈值图片
        return self.thresh_image

    def get_ssim_score(self):
        # 分数
        return self.score

    def get_thresh_classify(self):
        # 阈值结果
        return self.thresh_same

    def _get_good_match(self,des1,des2):
        # 特征值匹配knnMatch算法
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = []
        # 特征点匹配参数大小0.75
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)
        return good

    def _alignImages(self):
        # shift对图片进行角度修正
        grayB = cv2.cvtColor(self.compare_image, cv2.COLOR_BGR2GRAY)
        if not Config.SIFT:
            return grayB
        # sift
        MAX_FEATURES = 500
        GOOD_MATCH_PERCENT = 0.15

        sift = cv2.xfeatures2d.SIFT_create()
        kp1, dp1 = sift.detectAndCompute(self.grayA, None)
        kp2, dp2 = sift.detectAndCompute(grayB, None)
        goodmatch = self._get_good_match(dp1,dp2)
        
        # 特征点匹配个数 4 至少需要4个匹配成功的特征点
        if len(goodmatch) > Config.SIFT_MACTH_FEATURES_MIN:
            ptsA = np.float32([kp1[m.queryIdx].pt for m in goodmatch]).reshape(-1, 1, 2)
            ptsB = np.float32([kp2[m.trainIdx].pt for m in goodmatch]).reshape(-1, 1, 2)
            # 通过关键点找到透视转换矩阵H
            H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, Config.SIFT_RANSACREPROJTHRESHOLD);
            # 对grayB进行透视转换
            result = cv2.warpPerspective(grayB, H, (self.grayA.shape[1], self.grayA.shape[0]),
                                        flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
            return result
    
    # def _cut_img(self,img):
    #     # 对图片无效区域进行剪裁
    #     if Config.CUT_HIGH or Config.CUT_WIDE:
    #         orih,oriw = img.shape[:2]
    #         cropImg = img[Config.CUT_HIGH:orih, Config.CUT_WIDE:oriw]
    #         return cropImg
    #     return img
    
if __name__ == '__main__':
    #读取测试图片
    logging.info('----------------------------PixelVariance.py--start---------------------------------------')
    first_same = "G:/img_diff/tools/AllImages/L32/1682585756/school7Headdress60099/tick1.jpg"
    second_same = 'G:/img_diff/tools/AllImages/L32/1682670398/school7Headdress60099/tick28.jpg'
    first_dif = "G:/img_diff/tools/AllImages/L32/1682585756/school7Dress120013/tick1.jpg"
    second_dif = "G:/img_diff/tools/AllImages/L32/1682670398/school7Dress120013/tick9.jpg"

    img1=cv2.imread(first_same)
    
    #读取测试图片
    img11=cv2.imread(second_same)