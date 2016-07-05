#coding:utf8
import shutil
import os
#coding:utf8
#author: shikanon <shikanon@foxmail.com>

import sys

#模板地址
template_path = sys.path[0] + "/{{.project_name}}"

def create(path, name):
    new_path = path.rstrip("/") + "/" + name
    try:
        shutil.copytree(template_path, new_path)
    except:
        pass
    print("create new project")
    #把存在文件和文件夹都加入然后改名
    temple_files = []
    for dirpath, files, file_names in os.walk(new_path):
        for f_name in files:
            if r"{{.project_name}}" in f_name:
                temple_files.append((dirpath + "/" + f_name,
                dirpath + "/" + f_name.replace(r"{{.project_name}}", name)))
        for f_name in file_names:
            print(dirpath)
            print(f_name)
            with open(dirpath + "/" + f_name, "r") as fr:
                content = fr.read()
            with open(dirpath + "/" + f_name, "w") as fw:
                if r"{{.project_name}}" in content:
                    fw.write(content.replace(r"{{.project_name}}", name.encode("utf8")))
                else:
                    fw.write(content)
            if r"{{.project_name}}" in f_name:
                temple_files.append((dirpath + "/" + f_name, 
                    dirpath + "/" + f_name.replace(r"{{.project_name}}", name)))
                f_name.replace(r"{{.project_name}}", name)
    for temple_file in sorted(temple_files, reverse=True):
        print(temple_file)
        os.rename(*temple_file)

if __name__ == "__main__":
    path = raw_input("the new projects path:")
    name = raw_input("the projects name:")
    create(path, name)
    print("finish!")
