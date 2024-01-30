import sys
import utils
import os
import subprocess
import classifybypolicy
import makereport

if __name__ == '__main__':
    mode_id = sys.argv[1]
    mode = utils.Mode(int(mode_id))
    if mode == utils.Mode.D21 or mode == utils.Mode.D21DJ:
        target_dirs,name_dirs,output_dirs = utils.getThisWeekAllReportListbyMode(mode)
        testmode = 0
        count = 0
        exe_num = len(target_dirs)
        makereport.jekins_call_report(target_dirs,count,testmode,mode,exe_num)