import sys
import utils
import os
import subprocess
import classifybypolicy
import makereport

def error(message):
    print("[Error]: " + message)
    sys.exit(1)

if __name__ == '__main__':
    mode_id = sys.argv[1]
    mode = utils.Mode(int(mode_id))
    test_mode = sys.argv[2]
    if mode == utils.Mode.FASHION :
        target_dirs,name_dirs,output_dirs = utils.getThisWeekAllReportListbyMode(mode)
        if not target_dirs:
            error('No comparative results this week, stopping report flow.')
        compare_count = 0
        dir_list_tar = utils.getAllWeekVersions(mode,"whatever")
        for tar in dir_list_tar:
            compare_count += utils.getTotalCount(tar)
        print("The total number of images in this comparison is {}.".format(compare_count))
        print("The dir_list_tar images in this comparison is {}.".format(str(dir_list_tar)))
        testmode = int(test_mode)
        exe_num = len(target_dirs)
        makereport.jekins_call_report(target_dirs,compare_count,testmode,mode,exe_num)
    elif mode == utils.Mode.HOME:
        target_dirs,name_dirs,output_dirs = utils.getThisWeekAllReportListbyMode(mode)
        if not target_dirs:
            error('No comparative results this week, stopping report flow.')
        compare_count = 0
        dir_list_tar = utils.getAllWeekVersions(mode,"whatever")
        for tar in dir_list_tar:
            path = utils.HOME_DIR_PATH+ '/' + str(tar)
            compare_count += len(os.listdir(path))
        print("The total number of images in this comparison is {}.".format(compare_count))
        diff_num, add_num = utils.getDirListImageCount(target_dirs)
        if add_num + diff_num > utils.REPORT_LIMIT:
            error("Report image exceeds {} SIZE LIMIT, please check!".format(utils.REPORT_LIMIT))
        testmode = int(test_mode)
        exe_num = len(target_dirs)
        makereport.jekins_call_report(target_dirs,compare_count,testmode,mode,exe_num)
