"""
统计图像分类/目标检测/分割任务的数据 tags 信息。
包含图像名称 image_name、批次 date、季节 season、时段 time、天气 weather、
    城市 city、站点 station、角度 angle、距离 distance、设备 device 和标签 label

@params dataset_path: 数据存储路径
@params task        : 任务选择
@params labels      : 目标检测任务标签
@params version     : 数据版本

@author: lily
@date: 2024/01/12
"""
import os
import json
import argparse
from tqdm import tqdm
from datetime import datetime

# TODO 获取所有文件
def all_file_re_path(path, fileType=["jpg", "jpeg", "png", "mp4"]):
    Dirlist, Filelist = [], []
    for home, dirs, files in os.walk(path):
        # 获得所有文件夹
        for dirname in dirs:
            Dirlist.append(os.path.join(home, dirname))
        # 获得所有文件
        for filename in files:
            if filename.split(".")[-1].lower() in fileType:
                Filelist.append(os.path.join(home, filename))
    return Filelist

# TODO info 结构初始化
def init_info():
    info = {"year": str(datetime.today().year), "version": opt.version, "date_created": str(datetime.today().date())}
    labels_data = {"info": info, "tags": []}
    return labels_data

# TODO tags 结构初始化
def init_tags_infos():
    tags_info = {
        "image_name": "",
        "date": str(datetime.today().date()),
        "season": "",
        "time": "",
        "weather": "",
        "city": "",
        "station": "",
        "angle": "",
        "distance": "",
        "device": "",
        "label": ""
    }
    return tags_info

# TODO 获取目标检测任务中图像的 label 信息
def get_img_label_detection(image_path):
    label_file = image_path.replace("images", "labels")[:-3] + "txt"
    label = set()
    if os.path.exists(label_file):
        with open(label_file, "r") as f:
            for _, line in enumerate(f.readlines()):
                class_num = line.strip().split(" ")[0]
                label.add(opt.labels[int(class_num)])
    return list(label)

# TODO 获取图像分类任务中图像的 label 信息
def get_img_label_classify(image_path):
    label = image_path.split(os.path.sep)[-2]  # 子文件名称即为图像分类标签
    return label

# TODO 获取语义分割任务中图像的 label 信息
def get_img_label_segmentation(image_path):
    label = []
    return label

def get_img_label(task, image_path):
    if task == "detection":
        return get_img_label_detection(image_path)
    elif task == "classify":
        return get_img_label_classify(image_path)
    elif task == "segmentation":
        return get_img_label_segmentation(image_path)

# TODO 获取 tags 相关信息
def get_file_tag_infos(opt, image_path):
    image_info = init_tags_infos()
    image_info['image_name'] = image_path.replace(opt.dataset_path,'')[1:]

    img_name_info = os.path.basename(image_path).split("_")
    if len(img_name_info) == 8:
        image_info["time"], image_info["weather"], image_info["station"] = (
            img_name_info[3],
            img_name_info[2],
            img_name_info[4],
        )
    if len(img_name_info) == 6:
        image_info["time"], image_info["weather"], image_info["station"] = (
            img_name_info[4],
            img_name_info[3],
            img_name_info[1],
        )

    # * label 获取
    image_info["label"] = get_img_label(opt.task, image_path)
    return image_info

def task_tags(opt):
    tags = []
    img_files = all_file_re_path(opt.dataset_path)
    for img_file_path in tqdm(img_files, desc="Processing files", unit="file"):
        file_tag_infos = get_file_tag_infos(opt, img_file_path)
        if file_tag_infos is not None:
            tags.append(file_tag_infos)

    labels_data = init_info()
    labels_data["tags"] = tags
    json_path = os.path.join(opt.dataset_path, f"tags.json")
    with open(json_path, "w") as f:
        json.dump(labels_data, f, indent=2)
    print(f"generate tags.json success!")
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_path",
        type=str,
        default="/media/gll/5_Dataset_Archive/HHALG0218_AnQuanMao/RenTouAnQuanMaoJianCe_detection_20240123_44640_ver001",
        help="dataset path",
    )
    parser.add_argument(
        "--task",
        type=str,
        choices=["classify", "detection", "segmentation"],
        default="detection",
        help="choose task",
    )
    parser.add_argument(
        "--labels",
        type=list,
        #! 行人和车辆检测模型标签
        # default=["person", "bicycle", "car", "motorcycle", "bus", "truck"],
        #! 抽烟识别模型标签
        # default=["hand", "call", "smoke", "head"],
        #! 人头/安全帽检测模型标签
        default=["helmet", "head"],
        help="data labels for detection",
    )  # only detection
    parser.add_argument("--version", type=str, default="ver001", help="dataset version")
    opt = parser.parse_args()

    task_tags(opt)