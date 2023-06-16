import time

def file_to_version(filename):
    ori_ver = filename.split('_')[0]
    tar_ver = filename.split('_')[1]
    ori_st = time.localtime(int(ori_ver))
    tar_st = time.localtime(int(tar_ver))
    ori_ft = time.strftime('%Y-%m-%d %H:%M:%S', ori_st)
    tar_ft = time.strftime('%Y-%m-%d %H:%M:%S', tar_st)
    ori_ft = ori_ver+' ['+ ori_ft+']'
    tar_ft = tar_ver+' ['+ tar_ft+']'
    return ori_ver,tar_ver,ori_ft, tar_ft
