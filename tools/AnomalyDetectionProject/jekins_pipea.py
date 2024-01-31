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
    exe_name = sys.argv[2]
    mode = utils.Mode(int(mode_id))
    print(f"The project mode is: {mode}")
    print(f"The ori exe_name is: {exe_name}")
    dir_list_ori = utils.getOriVersion(mode,exe_name)
    dir_list_tar = utils.getAllWeekVersions(mode,exe_name)
    print(f"The dir list ori is: {dir_list_ori}")
    print(f"The dir list tar is: {dir_list_tar}")
    if not dir_list_ori or not dir_list_tar:
        error("No original images or target images this week, stopping compare flow.")
    if mode == utils.Mode.D21 or mode == utils.Mode.D21DJ:
        compare_parameter = [[dir_list_ori[0], x] for x in dir_list_tar]
        for param in compare_parameter:
            oriversion = param[0]
            tarversion = param[1]
            classifybypolicy.jekins_call_class(oriversion,tarversion,mode)
        target_dirs,name_dirs,output_dirs = utils.getThisWeekAllReportListbyMode(mode)
        if not target_dirs:
            error("No report generated for the current week, stopping makereport flow.")
        testmode = 1
        count = 0
        exe_num = len(target_dirs)
        makereport.jekins_call_report(target_dirs,count,testmode,mode,exe_num)
    elif mode == utils.Mode.FASHION:
        compare_parameter = []
        for ori_dir in dir_list_ori:
            for tar_dir in dir_list_tar:
                if utils.getSchoolIncludes(ori_dir) == utils.getSchoolIncludes(tar_dir):
                    compare_parameter.append([ori_dir,tar_dir])
        for param in compare_parameter:
            oriversion = param[0]
            tarversion = param[1]
            classifybypolicy.jekins_call_class(oriversion,tarversion,mode)
        target_dirs,name_dirs,output_dirs = utils.getThisWeekAllReportListbyMode(mode)
        diff_num = 0
        add_num = 0
        for result_dir in target_dirs:
            includes = os.listdir(result_dir)
            if result_dir.endswith(('_abnormal')):
                diff_num += len(includes)
            elif result_dir.endswith(('_add')):
                add_num += len(includes)
        print("Number of ABNORMAL images is {}, number of ADD images is {}.".format(diff_num, add_num))
        if add_num + diff_num > 15:
            print("[WARNING] Report image exceeds SIZE LIMIT, please check!")
        elif add_num + diff_num > 20:
            error("Report image exceeds 20 SIZE LIMIT, please check!")
    elif mode == utils.Mode.HOME:
        compare_parameter = dir_list_ori + dir_list_tar
        classifybypolicy.jekins_call_class(compare_parameter[0],compare_parameter[1],mode)
        target_dirs,name_dirs,output_dirs = utils.getThisWeekAllReportListbyMode(mode)
        diff_num, add_num = utils.getDirListImageCount(target_dirs)
        print("Number of ABNORMAL images is {}, number of ADD images is {}.".format(diff_num, add_num))
        if add_num + diff_num > utils.REPORT_LIMIT:
            error("Report image exceeds {} SIZE LIMIT, please check!".format(utils.REPORT_LIMIT))