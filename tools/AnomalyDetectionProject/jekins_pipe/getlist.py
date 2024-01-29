## 这里准备实现下根据目录自动生成需要比较的文件列表
import sys
sys.path.append('..')
import utils
import os

if __name__ == '__main__':
    mode_id = sys.argv[1]
    # mode_id = 2
    mode = utils.Mode(mode_id)
    print(f"The project mode is: {mode}")
    # mode
    dir_list_ori = utils.getOriVersion(mode)
    dir_list_tar = utils.getAllWeekVersions(mode)
    print(f"The dir list ori is: {dir_list_ori}")
    print(f"The dir list tar is: {dir_list_tar}")
    if mode == utils.Mode.D21:
        compare_parameter = [[dir_list_ori[0], x, mode_id] for x in dir_list_tar]
        for index, item in enumerate(compare_parameter):
            os.environ[f"COMPARE_PARAMETER_{index}"] = ','.join(item)

        # 将每个列表作为一个参数组的环境变量传递给 Jenkins
        for index, item in enumerate(compare_parameter):
            os.environ[f"COMPARE_PARAMETER_{index}"] = ','.join(item)
            print(f"COMPARE_PARAMETER_{index}={os.environ[f'COMPARE_PARAMETER_{index}']}")