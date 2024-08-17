# Semi-auto annotator based on SAM2

1. First run label.py --path "path to the folder with images for markup"--class_id=id_class_number
it will create a folder with the same name_labels next to it
On each image you need to left-click on the object point, then press space to go to the next one.
You can just press space, then the image will remain without markup (the previous markup will be saved if there was one).
You can press q and skip the entire folder to the end.

2. Then run annotate.py --path "path to the folder with images for markup" (the same path to the original images)
and it supplements the markup with masks and other things.