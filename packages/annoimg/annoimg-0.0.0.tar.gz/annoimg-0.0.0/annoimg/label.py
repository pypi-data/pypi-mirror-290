# importing the module
import argparse
import copy
import json
import os
from pathlib import Path

import cv2

path_to_images = ""
path_to_label = ""

current_class_id = 0
current_mouse_coords = []
scale_factor = 1.0
current_image_name = ""
dataset_label_path = ""
displayed_image = None

dataset = dict()


def show_image(windows_name, image, texts: list, texts_positions: list, masks: list, masks_ids: list):
    vis = copy.deepcopy(image)
    font = cv2.FONT_HERSHEY_SIMPLEX

    if len(texts) == len(texts_positions):
        for text, pos in zip(texts, texts_positions):
            cv2.putText(vis, text, (pos[0], pos[1]), font,
                        1, (255, 0, 0), 2)
    cv2.imshow(windows_name, vis)


def show_image_data(windows_name, image, image_file_name: str):
    global dataset
    global scale_factor
    vis = copy.deepcopy(image)
    font = cv2.FONT_HERSHEY_SIMPLEX

    color = (0, 0, 255)
    point_color = (0, 255, 255)

    if image_file_name in dataset.keys():
        data = dataset[image_file_name]

        alpha = 0.7

        if "mask" in data.keys():
            mask_names = data["mask"]
            for mask_name in mask_names:
                mask = cv2.imread(os.path.join(dataset_label_path, "masks_sam", mask_name))
                mask_sz = resize_aspect_ratio(mask, width=1024)
                vis = cv2.addWeighted(vis, alpha, mask_sz, 1 - alpha, 0)

        if "objects" in data.keys():
            texts = []
            texts_positions = []

            for obj in data["objects"]:
                if len(obj["point"]) < 2:
                    continue
                x = int(obj["point"][0] / scale_factor)
                y = int(obj["point"][1] / scale_factor)
                texts_positions.append([x, y])
                text = str(x) + ',' + str(y) + ' cid=' + str(obj["class_id"])
                texts.append(text)
                cv2.putText(vis, text, (x + 15, y), font, 1, point_color, 2)

                cv2.line(vis, [x - 10, y], [x + 10, y], point_color, 2)
                cv2.line(vis, [x, y - 10], [x, y + 10], point_color, 2)

            cv2.putText(vis, image_file_name, (40, 40), font,
                        1, color, 2)

    cv2.imshow(windows_name, vis)


def resize_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


# function to display the coordinates
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    global current_mouse_coords
    global current_image_name
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        image_data = dataset[current_image_name]
        if "objects" not in image_data.keys():
            image_data["objects"] = []

        x_upscaled = int(x * scale_factor)
        y_upscaled = int(y * scale_factor)

        obj_data = dict()
        obj_data["point"] = [x_upscaled, y_upscaled]
        obj_data["class_id"] = current_class_id
        obj_data["mask"] = ""
        image_data["objects"].append(obj_data)

        print(x_upscaled, ' ', y_upscaled)
        show_image_data('image', displayed_image, current_image_name)


'''
    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(displayed_image, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x, y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', displayed_image)
'''


def update_label_data(label_dict, full_images_path, image_names_list, label_images_path):
    is_modified = False
    for key in list(label_dict.keys()):
        if not os.path.exists(os.path.join(full_images_path, key)):
            del label_dict[key]
            is_modified = True

    for image_name in image_names_list:
        if not image_name in label_dict.keys():
            label_dict[image_name] = dict()
            is_modified = True

        if not "objects" in label_dict[image_name]:
            label_dict[image_name]["objects"] = []
            is_modified = True

        for obj in label_dict[image_name]["objects"]:
            if not type(obj) is dict:
                is_modified = True
                obj = dict()
                if not "point" in obj.keys():
                    obj["point"] = []

                if not "class_id" in obj.keys():
                    obj["class_id"] = -1

                if not "mask" in obj.keys():
                    obj['mask'] = str()

            if obj["class_id"] >= 0:
                file_name = os.path.splitext(os.path.basename(image_name))[0]
                file_name = file_name + "_" + str(obj["class_id"]) + ".png"

                if os.path.exists(os.path.join(label_images_path, file_name)):
                    if obj["mask"] != file_name:
                        obj["mask"] = file_name
                        is_modified = True
                else:
                    obj["mask"] = str()
                    is_modified = True

    return label_dict, is_modified


def open_folder(sub_path):
    full_images_path = os.path.join(path_to_images, sub_path)
    images_list = os.listdir(full_images_path)
    images_list = sorted(images_list)
    image_names = [f for f in images_list if os.path.isfile(os.path.join(full_images_path, f))]
    print(f"Found {len(image_names)} images in {full_images_path}")

    full_labeled_images_path = os.path.normpath(os.path.join(path_to_label, sub_path))

    Path(full_labeled_images_path).mkdir(parents=True, exist_ok=True)

    label_path = full_labeled_images_path
    label_file_name = os.path.basename(full_labeled_images_path)
    label_file_name = label_file_name + ".json"

    label_json_file_name = os.path.join(label_path, label_file_name)
    if os.path.exists(label_json_file_name):
        with open(label_json_file_name, "r") as f:
            label_data = json.load(f)
    else:
        label_data = dict()

    label_data, is_modified = update_label_data(label_data, full_images_path, image_names, full_labeled_images_path)
    if is_modified:
        with open(label_json_file_name, "w") as f:
            json.dump(label_data, f, indent=4)

    return label_data, full_images_path, full_labeled_images_path, label_json_file_name


def main(args):
    global path_to_images
    global path_to_label

    global current_class_id
    global current_mouse_coords
    global scale_factor
    global current_image_name
    global dataset_label_path
    global displayed_image

    global dataset

    parser = argparse.ArgumentParser("PreLabeling for SAM2")
    parser.add_argument("--path", help="Path to images folder for labeling", type=str)
    parser.add_argument("--class_id", help="Class id", type=int, default=0)
    args = parser.parse_args(args)

    if args.path is None:
        print("Error. Images path doesn't set")
        exit(1)

    if not os.path.exists(args.path) or not os.path.isdir(args.path):
        print("Error. Images path not found")
        exit(2)

    if args.class_id < 0:
        print(f"Error. Wrong class id={args.class_id}")
        exit(3)
    else:
        current_class_id = args.class_id

    path_to_images = os.path.normpath(args.path)
    path_to_label = path_to_images + "_labels"

    label_data, full_images_path, full_labeled_images_path, label_json_file_name = open_folder("")

    dataset = copy.deepcopy(label_data)
    dataset_label_path = full_labeled_images_path

    num_processed_images = 0
    num_skipped_images = 0
    index = 0
    for image_name, image_data in dataset.items():
        current_image_name = image_name
        img = cv2.imread(os.path.join(full_images_path, image_name), 1)
        displayed_image = resize_aspect_ratio(img, width=1024)
        (h, w) = img.shape[:2]
        scale_factor = w / 1024.0
        # displaying the image
        show_image_data('image', displayed_image, image_name)
        image_data["image_width"] = w
        image_data["image_height"] = h

        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback('image', click_event)

        # wait for a key to be pressed to exit
        pressed = cv2.waitKey(0)
        pressed_char = chr(pressed % 256)

        if pressed_char == "q":
            print(f"Skipped all images from {image_name}")
            num_skipped_images += len(label_data.items()) - num_skipped_images - num_processed_images
            break

    print(f"Processed {num_processed_images} images and {num_skipped_images} skipped")
    with open(label_json_file_name, "w") as f:
        json.dump(dataset, f, indent=4)

    # close the window
    cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
