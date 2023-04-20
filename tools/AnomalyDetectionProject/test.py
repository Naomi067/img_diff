# from img_load import img_process
from skimage.metrics import structural_similarity as sk_cpt_ssim
# import
import numpy as np
import cv2
first = "G:/ai_image/ai-airtest/AllImages/D90/RepeatingCrossbow/RepeatingCrossbow_MidnightShriek_4.jpg"
second = 'G:/ai_image/ai-airtest/AllImages/D90/RepeatingCrossbow2/RepeatingCrossbow_MidnightShriek_4.jpg'
first_img =  cv2.imread(first)
second_img = cv2.imread(second)
grayA = cv2.cvtColor(first_img, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(second_img, cv2.COLOR_BGR2GRAY)
def get_good_match(des1,des2):
    # 特征值匹配knnMatch算法
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
    # 特征点匹配参数大小0.75
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)
    return good
def alignImages(gray_normal,gray_compare ):
    # sift
    MAX_FEATURES = 500
    GOOD_MATCH_PERCENT = 0.15

    sift = cv2.xfeatures2d.SIFT_create()
    kp1, dp1 = sift.detectAndCompute(gray_normal, None)
    kp2, dp2 = sift.detectAndCompute(gray_compare, None)
    goodmatch = get_good_match(dp1,dp2)
    

    # 特征点匹配个数 4 至少需要4个匹配成功的特征点
    if len(goodmatch) > 4:
        ptsA = np.float32([kp1[m.queryIdx].pt for m in goodmatch]).reshape(-1, 1, 2)
        ptsB = np.float32([kp2[m.trainIdx].pt for m in goodmatch]).reshape(-1, 1, 2)
        ransacReprojThreshold = 1
        # 通过关键点找到透视转换矩阵H
        H, status = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, ransacReprojThreshold);
        # 对gray_compare进行透视转换
        result = cv2.warpPerspective(gray_compare, H, (gray_normal.shape[1], gray_normal.shape[0]),
                                     flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

        return result

# #sift
# MAX_FEATURES = 500
# GOOD_MATCH_PERCENT = 0.15
#
# sift = cv2.xfeatures2d.SIFT_create()
# kp1,dp1 = sift.detectAndCompute(grayA,None)
# kp2,dp2 = sift.detectAndCompute(grayB,None)
#
# # matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
# # matches = matcher.match(dp1,dp2,None)
#
# FLANN_INDEX_KDTREE = 0
# index_params = dict(algorithm=FLANN_INDEX_KDTREE,trees=5)
# search_params = dict(checks=50)
#
# flann = cv2.FlannBasedMatcher(index_params,search_params)
#
# matches = flann.knnMatch(dp1,dp2,k=2)
# matchesMask = [[0,0] for i in range(len(matches))]
#
# coff=0.3
# good=[]
#
# for i,(m,n) in enumerate(matches):
#     if m.distance < coff * n.distance:
#         matchesMask[i] = [1,0]
#         good.append(m)
#
# draw_params = dict(matchColor=(0,255,0),singlePointColor=(0,0,255),matchesMask=matchesMask,flags=0)
#
# result1 = cv2.drawMatchesKnn(first_img,kp1,second_img,kp2,matches,None,**draw_params)
# result2 = cv2.drawMatchesKnn(grayA,kp1,grayB,kp2,matches,None,**draw_params)
#
# if len(good) >3:
#     src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
#     dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
#     h,mask = cv2.findHomography(src_pts,dst_pts,cv2.RANSAC,5.0)
#
# height,width,channels = second_img.shape
# result = cv2.warpPerspective(first_img,h,(width,height))
# grayC = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
result = alignImages(grayA,grayB )
cv2.namedWindow('result',0)
cv2.imshow("result",result)
# cv2.namedWindow('result1',0)
# cv2.imshow("result1",result1)
# cv2.namedWindow('result2',0)
# cv2.imshow("result2",result2)





# retA, threshA = cv2.threshold(grayA,0,255,0)
# retB, threshB = cv2.threshold(grayB,0,255,0)
# thresh1 = cv2.threshold(grayA, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# thresh2 = cv2.threshold(grayB, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# contours1,hierarchy1 = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# contours2,hierarchy2 = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# epsilon = 0.1*cv2.arcLength(contours1[1],True)
# approx = cv2.approxPolyDP(contours1[1],epsilon,True)
# cv2.polylines(first_img,[approx],True,(0,255,0),3)
#
#
# cv2.drawContours(threshA,contours1,-1,(200,0,150),2)
# cv2.drawContours(threshB,contours2,-1,(200,0,150),2)
# (score, diff) = sk_cpt_ssim(thresh1, thresh2, full=True)
# print(score)
(score1, diff1) = sk_cpt_ssim(grayA, grayB, full=True)
print(score1)
diff_1 = (diff1* 255).astype("uint8")
# for i in diff_1:
#     print(i)
# thresh1 = cv2.threshold(diff_1, 100, 255,
# cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
thresh1 = cv2.threshold(diff_1, 50, 255,
cv2.THRESH_TOZERO_INV)[1]
print("////////////////")
# for i in thresh1:
#     print(i)
im_color = cv2.applyColorMap(thresh1,cv2.COLORMAP_HOT)
im_color2 = cv2.applyColorMap(diff_1,cv2.COLORMAP_HOT)
(score2, diff2) = sk_cpt_ssim(grayA, result, full=True)

print(score2)
diff_2 = (diff2* 255).astype("uint8")
im_color3 = cv2.applyColorMap(diff_2,cv2.COLORMAP_HOT)

thresh2 = cv2.threshold(diff_2, 255, 255,
cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# (score2, diff2) = sk_cpt_ssim(grayA, grayB, data_range=50000,full=True)
# print(score2)
cv2.namedWindow('COLORMAP',0)
cv2.imshow("COLORMAP", im_color)
cv2.namedWindow('diff1',0)
cv2.imshow("diff1", im_color2)
# cv2.namedWindow('diff2',0)
# cv2.imshow("diff2", diff2)
#
# cv2.namedWindow('thresh1',0)
# cv2.imshow("thresh1", thresh1)
cv2.namedWindow('thresh2',0)
cv2.imshow("thresh2", im_color3)
#
# cv2.namedWindow('Diff',0)
# cv2.imshow("Diff", threshB)
# cv2.namedWindow('Modified1',0)
# cv2.imshow("Modified1", thresh1)
# cv2.namedWindow('Modified2',0)
# cv2.imshow("Modified2", thresh2)
# cv2.namedWindow('first',0)
# cv2.imshow("first", first_img)
# cv2.namedWindow('second',0)
# cv2.imshow("second", second_img)

cv2.waitKey(0)