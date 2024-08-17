from xml.etree import ElementTree as ET
from xml.etree import ElementTree as etree
from xml.dom import minidom
import argparse
import os
import json
import cv2
import ast
import shutil

task_id = 0
task_name = "AutoAnnotator-SAM2"
segment_id = 0
url = "auto-annotator"
owner_username = "auto-annotator"
owner_email = "dummy@auto.annotate"
labels_data = [{"name": "pad", "color": "#08ff03", "type": "any"}, {"name": "stick", "color": "#00a6ff", "type": "any"}]


def pretty_print_xml_given_string(xml_root, output_xml):
    xml_string = minidom.parseString(ET.tostring(xml_root)).toprettyxml()
    xml_string = os.linesep.join([s for s in xml_string.splitlines() if s.strip()])  # remove the weird newline issue
    with open(output_xml, "w") as file_out:
        file_out.write(xml_string)


def remove_folder(folder: str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    shutil.rmtree(folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Convert labeled data to CVAT 1.1 exported data")
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

    dataset_file_name = os.path.basename(path_to_label)
    task_name = dataset_file_name
    dataset_file_name = dataset_file_name + ".json"

    label_json_file_name = os.path.join(path_to_label, dataset_file_name)
    if not os.path.exists(label_json_file_name) or not os.path.isfile(label_json_file_name):
        print(f"Error. File {dataset_file_name} not found")
        exit(3)

    with open(label_json_file_name, "r") as f:
        dataset = json.load(f)

    path_to_cvat_export = os.path.join(path_to_label, "cvat_export_temp")
    os.makedirs(path_to_cvat_export, exist_ok=True)
    os.makedirs(os.path.join(path_to_cvat_export, "images"), exist_ok=True)

    tree = ET.parse("cvat1.1_template.xml")
    root = tree.getroot()

    task = root.find("./meta/task")
    task.find('id').text = str(task_id)
    task.find('name').text = task_name

    owner = task.find("./owner")
    owner.find("username").text = owner_username
    owner.find("email").text = owner_email

    labels = task.find("./labels")
    for label_data in labels_data:
        label = etree.SubElement(labels, "label")
        etree.SubElement(label, "name").text = label_data["name"]
        etree.SubElement(label, "color").text = label_data["color"]
        etree.SubElement(label, "type").text = label_data["type"]
        etree.SubElement(label, "attributes").text = ""

    segment = task.find("./segments/segment")
    segment.find("id").text = str(segment_id)
    segment.find("start").text = str(0)
    segment.find("stop").text = str(len(dataset) - 1)

    task.find('size').text = str(len(dataset))
    task.find('start_frame').text = str(0)
    task.find('stop_frame').text = str(len(dataset) - 1)

    image_id = 0
    for image_name, image_data in dataset.items():
        print(f">>>>>>>> Process image {image_name} from {path_to_images} <<<<<<<<<")
        image = etree.SubElement(root, "image")
        image_mat = cv2.imread(os.path.join(path_to_images, image_name))
        shutil.copy2(os.path.join(path_to_images, image_name), os.path.join(path_to_cvat_export, "images"))
        (h, w) = image_mat.shape[:2]
        image.set("id", str(image_id))
        image.set("name", image_name)
        image.set("width", str(w))
        image.set("height", str(h))
        if image_data["objects"]:
            for obj in image_data["objects"]:
                for contour in obj["contours"]:
                    polygon = etree.SubElement(image, "polygon")
                    label_data = labels_data[obj["class_id"]]
                    polygon.set("label", label_data["name"])
                    polygon.set("source", "semi-auto")
                    polygon.set("occluded", "0")

                    contour_list = [float(x) for x in contour.split()]

                    points_str = ""
                    contour_pix = contour_list[1:]
                    contour_len = len(contour_pix)
                    for i, coord in enumerate(contour_pix):
                        if i % 2 == 0:
                            coord_pix = coord * w
                            points_str = points_str + '%.2f' % coord_pix + ","
                        else:
                            coord_pix = coord * h
                            points_str = points_str + '%.2f' % coord_pix + ";"
                        contour_pix[i] = coord_pix

                    points_str = points_str[:-1]

                    polygon.set("points", points_str)
                    polygon.set("z_order", "0")

        image_id += 1

    pretty_print_xml_given_string(root, os.path.join(path_to_cvat_export, "annotations.xml"))
    path_to_cvat_export_zip = os.path.join(path_to_label, "cvat_export")
    print(f"Save data for CVAT... for {task_name} to {path_to_cvat_export}/{path_to_cvat_export_zip}")
    os.makedirs(path_to_cvat_export_zip, exist_ok=True)
    shutil.make_archive(os.path.join(path_to_cvat_export_zip, task_name), 'zip', path_to_cvat_export)
    remove_folder(path_to_cvat_export)
