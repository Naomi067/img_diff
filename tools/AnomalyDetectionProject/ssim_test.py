# from img_load import img_process
from ssim import ssimProcess
import cv2
from matplotlib import pyplot as plt

first = "G:/ai_image/ai-airtest/AllImages/D90/RepeatingCrossbow/RepeatingCrossbow_WindBlast_4.jpg"
second = 'G:/ai_image/ai-airtest/AllImages/D90/RepeatingCrossbow2/RepeatingCrossbow_WindBlast_4.jpg'
first_img =  cv2.imread(first)
second_img = cv2.imread(second)

if __name__ == '__main__':
    ssimpre = ssimProcess(first_img,second_img)
    score = ssimpre.get_ssim_score()
    print(score)
    get_compare_img = ssimpre.get_compare_img()
    cv2.namedWindow('get_compare_img',0)
    cv2.imshow("get_compare_img",get_compare_img)
    get_thresh_img = ssimpre.get_thresh_img()
    cv2.namedWindow('get_thresh_img',0)
    cv2.imshow("get_thresh_img",get_thresh_img)
    get_diff_img = ssimpre.get_diff_img()
    cv2.namedWindow('get_diff_img',0)
    cv2.imshow("get_diff_img",get_diff_img)
    cv2.waitKey(0)
    # first_img = _cut_img(first_img)
    # cv2.imshow("cutimg",first_img)
    # cv2.waitKey(0)