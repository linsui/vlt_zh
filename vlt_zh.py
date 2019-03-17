"""A small code to change all fonts in vlc theme for Chinese
arg: dir font
dir: The director where the vlt file is in or the vlt file path
font: The font file path"""
import os
import shutil
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
import zipfile


def totgz(file_in, file_out):
    "Compress a directory into a tgz file"
    with tarfile.open(file_out, "w:gz") as tar:
        for file in os.listdir(file_in):
            tar.add(f"{file_in}/{file}", arcname=file)


def untgz(file_in, file_out):
    "Unzip a directory from a tgz file"
    with tarfile.open(file_in, "r:gz") as tar:
        tar.extractall(file_out)


def tozip(file_in, file_out):
    "Compress a directory into a zip file"
    shutil.make_archive(file_out, 'zip', file_in)
    shutil.move(f"{file_out}.zip", file_out)


def unzip(file_in, file_out):
    "Unzip a directory from a zip file"
    with zipfile.ZipFile(file_in, "r") as zipf:
        zipf.extractall(file_out)


def change_theme(temp_dir, font):
    "Move the font file and change the font field"
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file == "theme.xml":
                shutil.copy(font, f"{root}/{os.path.basename(font)}")
                theme_file = f"{root}/{file}"
                break
    theme_tree = ET.parse(theme_file)
    for font_ele in theme_tree.iter(tag='Font'):
        font_ele.set('file', f"{os.path.basename(font)}")
    theme_tree.write(theme_file)


def main(argv):
    "Read all vlt file in the directory and creat new file"
    vlt_path = argv[1]
    font = argv[2]

    if os.path.isfile(vlt_path):
        vlt_dir = [(f"{vlt_path}", f"{vlt_path}_zh.vlt")]
    else:
        vlt_dir = [(f"{vlt_path}/{vlt_file}",
                    f"{vlt_path}/{vlt_file[:-4]}_zh.vlt")
                   for vlt_file in os.listdir(vlt_path)
                   if vlt_file.endswith(".vlt")
                   if os.path.isfile(f"{vlt_path}/{vlt_file}")]

    for vlt_file, zh_vlt_file in vlt_dir:
        with tempfile.TemporaryDirectory() as temp_dir:
            if tarfile.is_tarfile(vlt_file):
                untgz(vlt_file, temp_dir)
                change_theme(temp_dir, font)
                totgz(temp_dir, zh_vlt_file)
            elif zipfile.is_zipfile(vlt_file):
                unzip(vlt_file, temp_dir)
                change_theme(temp_dir, font)
                tozip(temp_dir, zh_vlt_file)
            else:
                print("Unsupport format")


if __name__ == "__main__":
    main(sys.argv)
