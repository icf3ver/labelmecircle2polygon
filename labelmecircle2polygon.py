# labelmecircle2polygon
# By littleTitan
#
# Convert your labelme circles to polygons for coco converter
# compatibility. The original files are backed up just in case
# you want to go back to them later. There is absolutely no
# warranty.

import json
import numpy
import math
import sys
import os

if len(sys.argv) == 1:
   print("please specify a labelme directory")
   exit(1)
if os.path.isdir(sys.argv[1]) == "-h" or os.path.isdir(sys.argv[1]) == "--help" :
   print("Command: python labelme2python.py <labelme_dir> <args>")
   print("Arguments:")
   print(" -h or --help    displays this message")
   print(" -r              restores the .old files")
   exit(0)
elif len(sys.argv) > 3 or len(sys.argv) == 3 and sys.argv[2] != '-r':
   print("Unsupported arguments passed")
   exit(1)
elif not os.path.isdir(sys.argv[1]):
   print("There is no directory at", sys.argv[1])

labelme_dir = sys.argv[1]
restore = (len(sys.argv) == 3)

def convert_circle(center, radial):
   vec = [0, 0] # radial - center
   vec[0] = radial[0] - center[0]
   vec[1] = radial[1] - center[1]

   sides = 10
   angle = (2 * math.pi) / sides

   polygon = [0] * sides
   for i in range(0, sides):
      new_vec = [0, 0]
      # standard rotation matrix
      new_vec[0] = vec[0] * math.cos(angle * i) - vec[1] * math.sin(angle * i)
      new_vec[1] = vec[0] * math.sin(angle * i) + vec[1] * math.cos(angle * i)

      new_vec[0] = center[0] + new_vec[0]
      new_vec[1] = center[1] + new_vec[1]

      polygon[i] = new_vec

   return polygon

def convert_annotation(annotation):
   shapes = annotation['shapes']
   change = False
   for shape in shapes:
      if shape['shape_type'] == 'circle':
         change = True
         center, radial = shape['points']
         shape['points'] = convert_circle(center, radial)
         shape['shape_type'] = 'polygon'

   return change

# Note edgecases do exist:
# Please don't name your images to something containing .old

def backup (file_path, ext):
   backup_path = file_path.replace(ext, ".old" + ext);
   if os.path.isfile(backup_path):
      backup(backup_path, ".old" + ext)
   os.rename(file_path, backup_path);

def restore_backup(backup_path, ext):
   original_path = backup_path.replace(".old" + ext, ext)
   if os.path.isfile(original_path):
      if ".old" + ext in original_path:
         restore_backup(original_path, ext)
      else:
         os.remove(original_path) # cross platform solution
   os.rename(backup_path, original_path)

if __name__ == '__main__':
   if restore:
      proceed = input("You are about to restore all the old labels [y?]: ").lower();
      if proceed != "y":
         print("Exiting")
         exit(0)
      for file_name in os.listdir(labelme_dir):
         # Nothing fancy
         file_path = os.path.join(labelme_dir, file_name);

         if ".json" in file_path and not ".old" in file_path:
            backup_path = file_path
            while os.path.isfile(backup_path.replace(".json", ".old.json")):
               backup_path = backup_path.replace(".json", ".old.json")
            if file_path != backup_path:
               restore_backup(backup_path, ".json")
   else:
      for file_name in os.listdir(labelme_dir):
         # Nothing fancy
         file_path = os.path.join(labelme_dir, file_name);

         if ".json" in file_path and not ".old" in file_path:
            # No version check I personally use labelme 3.16.7
            annotation = json.load(open(file_path))
            if convert_annotation(annotation):
               backup(file_path, ".json")

               new_file = open(os.path.join(labelme_dir, file_name), 'w+')
               new_file.write(json.dumps(annotation))
               new_file.close()
