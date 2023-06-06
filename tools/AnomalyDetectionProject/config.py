class Config:
    THRESH_LIMIT_HIGH = 15            # thresh标注方框的大小限制高,为0时表示不限制（根据原图的大小设定）
    THRESH_LIMIT_WIDE = 30            # thresh标注方框的大小限制宽,为0时表示不限制
    THRESH_ALGRITHON = 100             # 灰度图像2值化的阈值大小
    SIFT = False                       # 是否使用sift进行图像对准
    SIFT_MACTH_FEATURES_MIN = 4       # SIFT最小匹配特征点数
    SIFT_RANSACREPROJTHRESHOLD = 4    # 内点的最大允许重投影错误阈值（仅用于RANSAC和RHO方法）ransacReprojThreshold
    SSIM_SCORE_JUDGE = 0.99           # 仅用分数判断是否正常时的设定值
    SSIM_WINSIZE = 7                  # SSIM计算分数的划窗大小,默认值是7,仅为奇数
    CUT_HIGH = 0                    # 图片剪裁高度,为0时不剪裁
    CUT_WIDE = 0                      # 图片剪裁宽度,为0时不剪裁
    HCONCAT_IMG = True                # 是否保存拼接图片
    DIFF_COUNT_LIMIT = 35            # 阈值判断为正常,分数判断为不正常时的特殊处理,计算所有thresh异常的数量,大于配置值则修正为tresh异常
    DIFF_MODIFY_LIMIT = 5             # 阈值判断为正常,分数判断为不正常时的特殊处理,标注图像方框的默认值,填0为所有都统计
    COMPARE_HIST_SCORE = [0.01, 0.9999, 1000] # 直方图比较方法对应的正常图片参数值>0.01 <0.9999 >1000视为不正常图片
    PHASH_VALUE = 10                  # 哈希算法的汉明距离，超过这个距离为异常图片  Hamming distance = 0  -> particular like  Hamming distance < 5  -> very like   hamming distance > 10 -> different picture
    MATCH_TEMPLATE_METHOD = 'cv2.TM_CCOEFF_NORMED' # 模板匹配的算法
    EDGE_RATIO = 0.3                  # 模板匹配的边缘比例，在这个边缘视为没匹配成功; 特征点均值左边无效区域
    HEADRESS_AREA = 500               # 头饰有效剪裁区域