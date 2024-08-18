# Semi-auto annotator based on SAM2

Run from pip package:

install tool: pip install annoimg

1. First run annoimg-label --path "path to the folder with images for markup"--class_id=id_class_number
it will create a folder with the same name_labels next to it
On each image you need to left-click on the object point, then press space to go to the next one.
You can just press space, then the image will remain without markup (the previous markup will be saved if there was one).
You can press q and skip the entire folder to the end.

2. Then run annoimg-annotate --path "path to the folder with images for markup" (the same path to the original images)
and it supplements the markup with masks and other things.


3. If you need convert data to CVAT v1.1 export format run annoimg-convert_cvat --path "path to the folder with images for markup" (the same path to the original images).



If you want call from sources then use correspondence files in annoimg folder:
label.py
annotate.py
convert_cvat.py
