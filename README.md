# labelmecircle2polygon
Convert your labelme circles to polygons for coco converter
compatibility. The original files are backed up just in case
you want to go back to them later. There is absolutely no 
warranty. 

# Usage
To convert circles to polygons: 
```sh
labelmecircle2polygon <dir> 
```

To recover backed up circles
```sh
labelmecircle2polygon <dir> -r
```

# Notice
It may be necessary to extract the backed up files from the
directory before you convert to the coco annotation format. 

It is important to note that while labelme may allow you to 
draw circles outside the image these are trouble.

# License
[MIT](./LICENSE.md)


