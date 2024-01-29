import sys
sys.path.append('..')
import utils
import os

if __name__ == '__main__':
    # mode_id = os.getenv('mode')
    mode_id = 2
    mode = utils.Mode(mode_id)
    print(f"The project mode is: {mode}")
    target_dirs,name_dirs,output_dirs = utils.getThisWeekAllReportListbyMode(mode)
    print(f"The target dirs is: {target_dirs}")
    print(f"The name dirs is: {name_dirs}")
    # 设置环境变量
    os.environ["NAME_DIRS"] = name_dirs