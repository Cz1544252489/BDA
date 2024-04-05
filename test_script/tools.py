import pickle
import json
import numpy as np
import argparse
from scipy.io import savemat
import matplotlib.pyplot as plt
import matplotlib as mpl

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--method', type=str, default='pic2json', metavar='STRING',
                    help='pic2json, pic2mat or plot.')
parser.add_argument('-fi', '--filename_input', type=str, default='Notes.pickle', metavar='STRING',
                    help='filename of input.')
parser.add_argument('-fo', '--filename_output', type=str, default='file.json', metavar='STRING',
                    help='filename of output.')
parser.add_argument('-px', '--plot_x', type=str, default='iterations', metavar='STRING',
                    help='plot for x.')
parser.add_argument('-py', '--plot_y', type=str, default='test_test', metavar='STRING',
                    help='plot for y, including train_train, train_test, test_test, valid_test, inner_losses, outer_losses, F1_score_micro etc.')
args = parser.parse_args()


# 定义一个函数，用于处理不可直接序列化的类型
def default(obj):
    if isinstance(obj, np.float32):
        return float(obj)
    raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")

if args.method=='pic2json':
# 步骤1: 从Pickle文件读取数据
    with open(args.filename_input, 'rb') as pickle_file:
        data = pickle.load(pickle_file)

# 步骤2: 将数据转换为JSON格式
# 使用default函数来处理float32等不可直接序列化的类型
    json_data = json.dumps(data, indent=4, default=default)

# 步骤3: 将JSON数据写入到文件
    with open(args.filename_output, 'w') as json_file:
        json_file.write(json_data)

    print(f"已将Pickle数据转换为JSON格式，并保存到 '{args.filename_output}'")

if args.method=='pic2mat':
    with open(args.filename_input, 'rb') as pickle_file:
        data = pickle.load(pickle_file)

    mat_data = {'data': data}

    savemat(args.filename_output, mat_data)

    print(f"已将Pickle数据转换为MATLAB的.mat格式，并保存到 '{args.filename_output}'")

if args.method=='plot':
    with open(args.filename_input,'r') as file:
        data = json.load(file)

    x = np.array(data[args.plot_x])
    y = np.array(data[args.plot_y])
    plt.plot(x, y)
    plt.savefig(args.filename_output)
    
    print(f"已将'{args.filename_input}'中数据{args.plot_x}(x)-{args.plot_y}(y)的线图，并保存到 '{args.filename_output}'")