

import zipfile, os, re


## RUN TESTS PRIOR

script_dir = os.path.join("io_extended_scene_vrm")
m = None

with open(os.path.join(script_dir,"__init__.py")) as vs_init:
	m = re.search("\"version\": \((.*)?\)\,",vs_init.read(),re.MULTILINE)

zip = zipfile.ZipFile(os.path.join("..","io_extended_scene_vrm_{}.zip".format(m.group(1).replace(", ",".").replace(".0.0",".0"))),'w',zipfile.ZIP_BZIP2)

for path, dirnames, filenames in os.walk(script_dir):
	if path.endswith("__pycache__"): continue
	for f in filenames:
		f = os.path.join(path,f)
		zip.write(os.path.realpath(f),f)

zip.close()
print("Packaged into Projects Folder")