import argparse
import copy
import json
import os
import numpy as np

import cv2
from ultralytics import SAM
from ultralytics.data.utils import polygon2mask
from ultralytics.utils.ops import segments2boxes

def change_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def main(args):
    parser = argparse.ArgumentParser("PreLabeling for SAM2")
    parser.add_argument("--path", help="Path to images folder for labeling", type=str)
    args = parser.parse_args()

    if args.path is None:
        print("Error. Images path doesn't set")
        exit(1)

    path_to_images = os.path.normpath(args.path)
    path_to_label = path_to_images + "_labels"

    if not os.path.exists(path_to_images) or not os.path.isdir(path_to_images):
        print("Error. Images path not found")
        exit(2)

    if not os.path.exists(path_to_label) or not os.path.isdir(path_to_label):
        print("Error. Labels path not found")
        exit(3)

    model = SAM("sam2_b.pt")

    images = os.listdir(path_to_images)
    images = sorted(images)

    label_file_name = os.path.basename(path_to_label)
    label_file_name = label_file_name + ".json"

    label_json_file_name = os.path.join(path_to_label, label_file_name)
    if not os.path.exists(label_json_file_name) or not os.path.isfile(label_json_file_name):
        print(f"Error. File {label_file_name} not found")
        exit(3)

    with open(label_json_file_name, "r") as f:
        label_data = json.load(f)

    for image_file, image_data in label_data.items():
        if "mask" in image_data.keys():
            del image_data["mask"]
        if "contours" in image_data.keys():
            del image_data["contours"]

    output_dir = os.path.join(path_to_label, "masks_sam")
    example_dir = os.path.join(path_to_label, "vis_sam")
    seg_labels_dir = os.path.join(path_to_label, "labels_sam_seg")
    bbox_labels_dir = os.path.join(path_to_label, "labels_sam_bbox")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(example_dir, exist_ok=True)
    os.makedirs(seg_labels_dir, exist_ok=True)
    os.makedirs(bbox_labels_dir, exist_ok=True)



    for image_file, image_data in label_data.items():
        print(f">>>>>>>> Begin process image {image_file} from {path_to_images} <<<<<<<<<")
        image_data["vis"] = ""
        image_data["unlabeled_mask"] = []
        image_data["unlabeled_contours"] = []
        image_data["unlabeled_boxes"] = []

        points = []
        classes_ids = []
        for obj in image_data["objects"]:
            points.append(obj["point"])
            classes_ids.append(obj["class_id"])
            obj["mask"] = []
            obj["contours"] = []
            obj["boxes"] = []

        if len(points) == 0 or len(points) != len(classes_ids):
            print(f"No prelabeled info for {image_file}. Skip")
            print(f">>>>>>>> End process image {image_file} <<<<<<<<<\n")
            continue

        try:
            image = cv2.imread(os.path.join(path_to_images, image_file))
            results = model(image, points=points, labels=classes_ids, show=False, save=False,
                show_boxes=True, show_labels=True,
                show_conf=True)
        except Exception:
            print(f"Exception when call SAM2 on {image_file}: {Exception}")
            print(f">>>>>>>> End process image {image_file} <<<<<<<<<\n")
            continue

        if results is None:
            print(f"Objects not found on {image_file}")
            print(f">>>>>>>> End process image {image_file} <<<<<<<<<\n")
            continue

        result = results[0]
        print(f"SAM processed image {result.path}, found labels= {result.names}")

        filename = os.path.splitext(image_file)[0]

        vis_file_name = filename + ".jpg"
        result.save(os.path.join(example_dir, vis_file_name))

        image_data["vis"] = vis_file_name

        ori_img = result.orig_img

        object_point_corresponds = dict()
        for i, m in enumerate(result.masks.xy):
            mask_shape = m.shape
            res_mask = polygon2mask(
                (ori_img.shape[0], ori_img.shape[1]),  # tuple
                [m],  # input as list
                color=255,  # 8-bit binary
                downsample_ratio=1,
            )

            class_id = None
            for j, obj in enumerate(image_data["objects"]):
                point = obj["point"]
                pixel = res_mask[point[1], point[0]]
                if pixel == 255:
                    object_point_corresponds[i] = j

            if i in object_point_corresponds.keys():
                class_id = image_data["objects"][i]["class_id"]
            else:
                class_id = None

            mask_file_name = filename + "_" + str(class_id) + "_" + str(i) + ".png"
            cv2.imwrite(os.path.join(output_dir, mask_file_name), res_mask)

            if class_id is not None:
                image_data["objects"][object_point_corresponds[i]]["mask"].append(mask_file_name)
            else:
                image_data["unlabeled_mask"].append(mask_file_name)

        texts = []
        segments = []
        for i, m in enumerate(result.masks.xyn):
            mask_shape = m.shape
            seg = m.copy().reshape(-1)

            if i in object_point_corresponds.keys():
                class_id = image_data["objects"][i]["class_id"]
                line = (class_id, *seg)
            else:
                class_id = None
                line = (-1, *seg)

            segments.append(line)

            final_line = ("%g " * len(line)).rstrip() % line
            texts.append(final_line)

            if class_id is not None:
                image_data["objects"][object_point_corresponds[i]]["contours"].append(final_line)
            else:
                image_data["unlabeled_contours"].append(final_line)

        with open(os.path.join(seg_labels_dir, filename + ".txt"), "w") as f:
            f.writelines(text + "\n" for text in texts)

        # save bboxes
        bbox_texts = []
        segments_np = np.array(segments)
        bboxes = segments2boxes([s[1:].reshape(-1, 2) for s in segments_np])
        segments_classes = [s[0] for s in segments_np]

        for i, bbox in enumerate(bboxes):
            bbox_line = bbox.tolist()
            bbox_line = (segments_classes[i], *bbox_line)
            final_line = ("%g " * len(bbox_line)).rstrip() % bbox_line

            bbox_texts.append(final_line)
            if segments_classes[i] >= 0:
                image_data["objects"][object_point_corresponds[i]]["boxes"].append(final_line)
            else:
                image_data["unlabeled_boxes"].append(final_line)

        with open(os.path.join(bbox_labels_dir, filename + ".txt"), "w") as f:
            f.writelines(text + "\n" for text in bbox_texts)

        print(f">>>>>>>> End process image {image_file} <<<<<<<<<\n")

    with open(label_json_file_name, "w") as f:
        json.dump(label_data, f, indent=4)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])