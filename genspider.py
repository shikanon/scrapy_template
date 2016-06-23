#coding:utf8
import click
import shutil
import chardet
import os

#模板地址
template_path = r"G:/我的网站/微信/content/crawler_template/{{.project_name}}"

@click.command()
@click.option("--name",default="spider")
def create(name):
    new_path = os.getcwd().decode("gbk") + "/" + name
    shutil.copytree(template_path.decode("utf8"), new_path)
    temple_files = []
    for dirpath, files, file_names in os.walk(new_path):
        print(dirpath, files, file_names)
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
            if r"{{.project_name}}" in f_name:
                temple_files.append((dirpath + "/" + f_name, 
                    dirpath + "/" + f_name.replace(r"{{.project_name}}", name)))
                f_name.replace(r"{{.project_name}}", name)
    for temple_file in sorted(temple_files,reverse=True):
        print(temple_file)
        os.rename(*temple_file)
    
if __name__ == "__main__":
    create()
