﻿import os
import zipfile

VERSION = "0.2.0"

def main():
    """Build Blender Plugin"""

    print("Building plugin ...")

    package_dir = os.path.abspath("build")
    print("package_dir: " + package_dir)

    if not os.path.isdir(package_dir):
        try:
            os.mkdir(package_dir)
        except:
            print("Cannot create build dir at path: {0}".format(package_dir))
            return

    package = os.path.join(package_dir, "batched-blender-{0}.zip".format(VERSION))
    source = os.path.abspath("batched_blender")

    with zipfile.ZipFile(package, mode='w') as blend_zip:
        for root, dirs, files in os.walk(source):
            if root.endswith("__pycache__"):
                continue

            for file in files:
                blend_zip.write(os.path.relpath(os.path.join(root, file)))

    print("Package complete!")

if __name__ == '__main__':
    main()