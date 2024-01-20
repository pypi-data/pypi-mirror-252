import json, os
from copy import deepcopy
import numpy as np
import pandas as pd
from tqdm import tqdm

from mmengine.registry import DATASETS
from typing import List, Union, Callable, Optional, Sequence

from shapely.geometry import box, Polygon, MultiPolygon

from mmengine.dataset import BaseDataset, Compose
from multiprocessing import Pool



@DATASETS.register_module()
class EngineCocoExt(BaseDataset):
    def __init__(self,
                 data_path: str,
                 raster_dir_path: str,
                 vector_dir_path: str,
                 split: str = "train",
                 class_title: str = None,
                 slice: bool = False,
                 window: tuple = None,
                 stride: tuple = None,
                 pipeline: List[Union[dict, Callable]] = [],
                 max_refetch: int = 1000,
                 ignore_index: int = 255,
                 reduce_zero_label: bool = False,
                 filter_empty: bool = False,
                 serialize_data: bool = True,
                 detect_only: bool = False,
                 lazy_init: bool = False,
                 indices: Optional[Union[int, Sequence[int]]] = None,
                 test_mode: bool = False,
                 classes: list = None):
        self.raster_data_path = f"{data_path}/{raster_dir_path}"
        self.vector_data_path = f"{data_path}/{vector_dir_path}"

        self.split = split
        self.slice = slice 
        self.window = window 
        self.stride = stride
        self.class_title = class_title
        self.ignore_index = ignore_index
        self.reduce_zero_label = reduce_zero_label
        self.filter_empty = filter_empty
        self.serialize_data = serialize_data
        self.detect_only = detect_only
        self._indices = indices
        self.test_mode = test_mode
        self.classes = classes
        
        self.pipeline = Compose(pipeline)
        self.max_refetch = max_refetch

        if not lazy_init:
            self.full_init()

    
    def _slice_annotations(self, annotations, box_poly):
        cropped_annotations = []
        for annotation in annotations:
            seg = annotation['segmentation'][0]
            seg_poly = Polygon([[seg[i], seg[i+1]] for i in range(0, len(seg), 2)])
            if seg_poly.buffer(0).intersects(box_poly):
                cropped_seg_poly = seg_poly.buffer(0).intersection(box_poly)
                x1, y1, x2, y2 = map(int, list(cropped_seg_poly.bounds))
                x1 = x1 - box_poly.bounds[0]
                y1 = y1 - box_poly.bounds[1]
                x2 = x2 - box_poly.bounds[0]
                y2 = y2 - box_poly.bounds[1]

                if x2 > x1 and y2 > y1:
                    segmentation = []
                    if isinstance(cropped_seg_poly, MultiPolygon):
                        for poly in cropped_seg_poly.geoms:
                            for coord in list(poly.exterior.coords):
                                segmentation.append(coord[0] - box_poly.bounds[0])
                                segmentation.append(coord[1] - box_poly.bounds[1])
                    elif isinstance(cropped_seg_poly, Polygon):
                        for coord in list(cropped_seg_poly.exterior.coords):
                            segmentation.append(coord[0] - box_poly.bounds[0])
                            segmentation.append(coord[1] - box_poly.bounds[1])

                    if len(annotation["properties"][self.class_title_idx]["labels"]):
                        bbox_label = annotation["properties"][self.class_title_idx]["labels"][0]
                        if self.classes:
                            lbl = self._metainfo["original_classes"][bbox_label]
                            if lbl in self._metainfo["classes"]:
                                bbox_label = self._metainfo["classes"].index(lbl)
                            else:
                                bbox_label = None
                        
                        if self.detect_only:
                            bbox_label = 0

                        if bbox_label is not None:
                            cropped_annotations.append({"area": cropped_seg_poly.area,
                                                        "bbox": [x1, y1, x2, y2],
                                                        "mask": [segmentation],
                                                        "bbox_label": bbox_label,
                                                        "ignore_flag": 0,
                                                        "extra_anns": []
                                                        })
        return cropped_annotations

    def _slice_image_info(self, vec_map, img_map):
        data_infos = []
        img_height = vec_map["images"][0]["height"]
        img_width = vec_map["images"][0]["width"]
        for slice_y in range(0, img_height, self.stride[0]):
            if (slice_y + self.window[0]) < img_height:
                for slice_x in range(0, img_width, self.stride[1]):
                    if (slice_x + self.window[1]) < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_x"] = slice_x
                        new_info["slice_y"] = slice_y
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = self.window[0]
                        box_poly = box(slice_x, slice_y, slice_x + self.window[1] - 1, slice_y + self.window[0] - 1)
                        new_info["instances"] = self._slice_annotations(vec_map["annotations"], box_poly)
                        data_infos.append(new_info)
                    elif slice_x < img_width and self.window[1] < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = img_width - self.window[1] - 1
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = self.window[0]
                        box_poly = box(slice_x, slice_y, slice_x + self.window[1] - 1, slice_y + self.window[0] - 1)
                        new_info["instances"] = self._slice_annotations(vec_map["annotations"], box_poly)
                        data_infos.append(new_info)
                    elif self.window[1] >= img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = 0
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = img_width
                        new_info["slice_h"] = self.window[0]
                        box_poly = box(slice_x, slice_y, slice_x + img_width, slice_y + self.window[0] - 1)
                        new_info["instances"] = self._slice_annotations(vec_map["annotations"], box_poly)
                        data_infos.append(new_info)
   
            elif slice_y < img_height and self.window[0] < img_height:
                slice_y = img_height - self.window[0] - 1
                for slice_x in range(0, img_width, self.stride[1]):
                    if (slice_x + self.window[1]) < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_x"] = slice_x
                        new_info["slice_y"] = slice_y
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = self.window[0]
                        box_poly = box(slice_x, slice_y, slice_x + self.window[1] - 1, slice_y + self.window[0] - 1)
                        new_info["instances"] = self._slice_annotations(vec_map["annotations"], box_poly)
                        data_infos.append(new_info)
                    elif slice_x < img_width and self.window[1] < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = img_width - self.window[1] - 1
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = self.window[0]
                        box_poly = box(slice_x, slice_y, slice_x + self.window[1] - 1, slice_y + self.window[0] - 1)
                        new_info["instances"] = self._slice_annotations(vec_map["annotations"], box_poly)
                        data_infos.append(new_info)
                    elif self.window[1] >= img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = 0
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = img_width
                        new_info["slice_h"] = self.window[0]
                        box_poly = box(slice_x, slice_y, slice_x + img_width, slice_y + self.window[0] - 1)
                        new_info["instances"] = self._slice_annotations(vec_map["annotations"], box_poly)
                        data_infos.append(new_info)

            elif self.window[0] >= img_height:
                slice_y = 0
                for slice_x in range(0, img_width, self.stride[1]):
                    if (slice_x + self.window[1]) < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_x"] = slice_x
                        new_info["slice_y"] = slice_y
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = img_height
                        box_poly = box(slice_x, slice_y, slice_x + self.window[1] - 1, slice_y + img_height)
                        new_info["instances"] = self._slice_annotations(vec_map["annotations"], box_poly)
                        data_infos.append(new_info)
                    elif slice_x < img_width and self.window[1] < img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = img_width - self.window[1] - 1
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = self.window[1]
                        new_info["slice_h"] = img_height
                        box_poly = box(slice_x, slice_y, slice_x + self.window[1] - 1, slice_y + img_height)
                        new_info["instances"] = self._slice_annotations(vec_map["annotations"], box_poly)
                        data_infos.append(new_info)
                    elif self.window[1] >= img_width:
                        new_info = deepcopy(img_map)
                        new_info["slice_y"] = slice_y
                        slice_x = 0
                        new_info["slice_x"] = slice_x
                        new_info["slice_w"] = img_width
                        new_info["slice_h"] = img_height
                        box_poly = box(slice_x, slice_y, slice_x + img_width, slice_y + img_height)
                        new_info["instances"] = self._slice_annotations(vec_map["annotations"], box_poly)
                        data_infos.append(new_info)

        return data_infos

    def _load_vector_file(self, vec_path):
        with open(vec_path, 'r') as fin:
            vec_map = json.load(fin)

        file_name = vec_map["images"][0]["file_name"].split("/")[-1]
        file_path = os.path.join(self.raster_data_path, file_name)

        img_map = {
            "img_path": file_path,
            "img_id": vec_map["info"]["id"],
            "height": vec_map["images"][0]["height"],
            "width": vec_map["images"][0]["width"],
            "instances": [],
            "seg_fields": [],
            "reduce_zero_label": self.reduce_zero_label
        }

        if self.slice:
            return self._slice_image_info(vec_map, img_map)
        else:
            img_map["slice_x"] = 0
            img_map["slice_y"] = 0
            img_map["slice_w"] = img_map["width"]
            img_map["slice_h"] = img_map["height"]

            for annotation in vec_map["annotations"]:
                try:
                    xmin, ymin, width, height = annotation["bbox"]
                    xmax,ymax = xmin+width, ymin+height
                    bbox = [xmin, ymin, xmax, ymax]
                    
                    if len(annotation["properties"][self.class_title_idx]["labels"]):
                        bbox_label = annotation["properties"][self.class_title_idx]["labels"][0]
                        if self.classes:
                            lbl = self._metainfo["original_classes"][bbox_label]
                            if lbl in self._metainfo["classes"]:
                                bbox_label = self._metainfo["classes"].index(lbl)
                            else:
                                bbox_label = None
                        
                        if self.detect_only:
                            bbox_label = 0

                        if bbox_label is not None:
                            mask = [annotation["segmentation"][0][:-2]]

                            ann_map = {
                                "bbox": bbox,
                                "bbox_label": bbox_label,
                                "mask": mask,
                                "ignore_flag": 0,
                                "extra_anns": []
                            }

                            img_map["instances"] += [ann_map]
                except:
                    continue

            return img_map

    def load_data_list(self):
        meta_path = os.path.join(self.vector_data_path, "metadata.json")
        with open(meta_path, "r") as fin:
            metadata = json.load(fin)
    
        if not self.class_title:
            if self.classes:
                for cls in self.classes:
                    assert cls in metadata["label:metadata"][0]["options"], f"{cls} provided not in response options of this question"
                self.CLASSES = self.classes
            else:
                self.CLASSES = metadata["label:metadata"][0]["options"]
            self.class_title = metadata["label:metadata"][0]["title"].replace(" ", "-").lower()
            self.class_title_idx = 0
        else:
            for idx, question in enumerate(metadata["label:metadata"]):
                if question["title"] == self.class_title:
                    if self.classes:
                        for cls in self.classes:
                            assert cls in metadata["label:metadata"][0]["options"], f"{cls} provided not in response options of this question"
                        self.CLASSES = self.classes
                    else:
                        self.CLASSES = question["options"]
                    self.class_title = self.class_title.replace(" ", "-").lower()
                    self.class_title_idx = idx 

        self._metainfo = {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata["tags"],
            "problemType": metadata["problemType"] if "problemType" in metadata else None,
            "question_title": metadata["label:metadata"][self.class_title_idx]["title"],
            "question_description": metadata["label:metadata"][self.class_title_idx]["description"],
            "original_classes": metadata["label:metadata"][self.class_title_idx]["options"],
            "classes": self.CLASSES,
            "reduce_zero_label": self.reduce_zero_label
        }

        vec_path_list = [os.path.join(self.vector_data_path, vec_file) for vec_file in metadata["dataset"][self.split]]

        pool = Pool(16)
        data_list = list(tqdm(pool.imap(self._load_vector_file, vec_path_list), total=len(vec_path_list)))

        if self.slice:
            data_list = [item for sublist in data_list for item in sublist]
        pool.close()

        tot_annotations = 0
        without_annotations = 0
        heights = []
        widths = []

        filtered_data_list = []
        for img in data_list:
            tot_annotation_this_img = len(img['instances'])
            if tot_annotation_this_img == 0:
                without_annotations += 1
            tot_annotations += tot_annotation_this_img
            heights.append(img['slice_h'])
            widths.append(img['slice_w'])
            if self.filter_empty and len(img['instances']):
                filtered_data_list.append(img)
            elif not self.filter_empty:
                filtered_data_list.append(img)
        
        print (f"Number of annotations in {self.split} : {tot_annotations}")
        print (f"Number of images without any annotations : {without_annotations}")
        print (f"Number of images used for training post filtering : {len(filtered_data_list)}")
        print (f"Minimum image size, Height : {min(heights)} Width : {min(widths)}")
        print (f"Maximum image size, Height : {max(heights)} Width : {max(widths)}")
        print (f"Average image size, Height : {np.mean(heights)} Width : {np.mean(widths)}")
    
        return filtered_data_list