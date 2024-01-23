"""
A class to organize YOLO-structured data

Methods
---

get_images
    list of absolute paths of images in root/<split>/images
clone
    copy root/train and root/test to root/<folder_name>
shuffle_train_val
    shuffle self.ls_train_images and assign to
save_yaml
save_txt


Folder structure
---
root/
    train/ (required)
        images/
            img_1_13_jpg.rf.d69528304f2d10b633c6d94982185cb2.jpg
            img_2_13_jpg.rf.d69528304f2d10b633c6d94982185cb2.jpg
            ...
        labels/
            img_1_13_jpg.rf.d69528304f2d10b633c6d94982185cb2.txt
            img_2_13_jpg.rf.d69528304f2d10b633c6d94982185cb2.txt
            ...
    test/ (required)
        images/
            img_3.jpg
            img_4.jpg
            ...
        labels/
            img_3.txt
            img_4.txt

    test.txt (generated)
    train.txt (generated)
    val.txt (generated)
    data.yaml (generated)

Example YAML
---
path: /home/niche/cowsformer/data/cow200/yolov5/run3
train: "train.txt"
val: "val.txt"
test: "test.txt"
names:
  0: none
  1: cow

Example train.txt
---

/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_32_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_1_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_1_26_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_1_62_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_1_10_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_3_11_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_4_3_jpg
"""

import os
import shutil
import random


class YOLO_API:
    def __init__(
        self,
        root: str,
    ):
        self.root = root
        self.ls_train_images_all = self.get_images("train")
        self.ls_train_images = None
        self.ls_val_iamges = None
        self.ls_test_images = self.get_images("test")
        self.save_txt("test")

    def get_images(self, split):
        """
        search images names (.jpg) in root/<split>/images

        params
        ------
        split: str
            "train" or "test"

        return
        ------
        a list of aboslute paths of images
        """
        path_images = os.path.join(self.root, split, "images")
        ls_images = [f for f in os.listdir(path_images) if f.endswith(".jpg")]
        ls_images = [os.path.join(path_images, f) for f in ls_images]
        return ls_images

    def clone(self, folder_name):
        """
        copy root/train and root/test to root/<folder_name>
        """
        path_train = os.path.join(self.root, "train")
        path_test = os.path.join(self.root, "test")
        path_folder = os.path.join(self.root, folder_name)
        if os.path.exists(path_folder):
            shutil.rmtree(path_folder)
        os.mkdir(path_folder)
        shutil.copytree(path_train, os.path.join(path_folder, "train"))
        shutil.copytree(path_test, os.path.join(path_folder, "test"))

    def shuffle_train_val(self, n, fold=5):
        """
        shuffle self.ls_train_images and assign to
        self.ls_train_images and self.ls_val_images

        params
        ------
        n: int or float
            int: number of images to be included in the train/val set
            float: ratio of images to be included in the train/val set
        fold: int
            how many folds to split the train/val set
        """
        if isinstance(n, float):
            n = int(n * len(self.ls_train_images_all))
        random.shuffle(self.ls_train_images_all)
        train_images = self.ls_train_images_all[:n]
        n_val = len(train_images) // fold
        self.ls_train_images = train_images[:-n_val]
        self.ls_val_images = train_images[-n_val:]
        self.save_txt("train")
        self.save_txt("val")

    def save_yaml(self, classes, name="data.yaml"):
        """
        make data.yaml in root

        params
        ------
        classes: list
            e.g., ["cow", "none"]

        name: str
            name of the yaml file

        """
        path_yaml = os.path.join(self.root, name)
        with open(path_yaml, "w") as f:
            f.write(f"path: {self.root}\n")
            f.write(f'train: "train.txt"\n')
            f.write(f'val: "val.txt"\n')
            f.write(f'test: "test.txt"\n')
            f.write("names:\n")
            for i, c in enumerate(classes):
                f.write(f"  {i}: {c}\n")

    def save_txt(self, split):
        """
        save <split>.txt in root
        """
        path_txt = os.path.join(self.root, f"{split}.txt")
        with open(path_txt, "w") as f:
            for img in getattr(self, f"ls_{split}_images"):
                f.write(img + "\n")
