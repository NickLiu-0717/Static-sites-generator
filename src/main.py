import shutil
import os
from markdown_block import *
from markdown_to_htmlnode import markdown_to_html_node

template_html = "/home/capybrella/workspace/github.com/NickLiu-0717/Static-sites-generator/template.html"
src = '/home/capybrella/workspace/github.com/NickLiu-0717/Static-sites-generator/static/'
dst = '/home/capybrella/workspace/github.com/NickLiu-0717/Static-sites-generator/public/'
ct = '/home/capybrella/workspace/github.com/NickLiu-0717/Static-sites-generator/content/'
html_file_name = "index.html"

def generate_page(from_path, template_path, dest_path):
    print(f"Generating paging from {from_path} to {dest_path} using {template_path}")
    # md_filename = os.listdir(from_path)
    # full_md_file_path = os.path.join(from_path, md_filename)
    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()
    with open(template_path, "r") as temp_file:
        template = temp_file.read()
    htmlnode = markdown_to_html_node(markdown)
    htmlstring = htmlnode.to_html()
    title = extract_title(markdown)
    re_template = template.replace('{{ Title }}', title).replace("{{ Content }}", htmlstring)
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    with open(dest_path + html_file_name, "w") as html:
        html.write(re_template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # print(f"Generating paging from {dir_path_content} to {dest_dir_path} using {template_path}")
    with open(template_path, "r") as temp_file:
        template = temp_file.read()
    for file in os.listdir(dir_path_content):
        # print(file)
        full_md_file_path = os.path.join(dir_path_content, file)
        if os.path.isfile(full_md_file_path):
            filename = file.split(".")
            html_filename = filename[0] + ".html"
            with open(full_md_file_path, "r") as markdown_file:
                markdown = markdown_file.read()
            htmlnode = markdown_to_html_node(markdown)
            htmlstring = htmlnode.to_html()
            title = extract_title(markdown)
            re_template = template.replace('{{ Title }}', title).replace("{{ Content }}", htmlstring)
            if not os.path.exists(dest_dir_path):
                os.mkdir(dest_dir_path)
            with open(os.path.join(dest_dir_path, html_filename), "w") as html:
                html.write(re_template)
        else:
            subdst = os.path.join(dest_dir_path, file)
            # print(full_md_file_path)
            os.mkdir(subdst)
            generate_pages_recursive(full_md_file_path, template_path, subdst)

def copy_from_src_to_dst(src_directory, dst_directory):   
    if not os.path.exists(src_directory):
        raise ValueError("ERROR: Source directory doesn't exist")
    for filename in os.listdir(src_directory):
        full_file_name = os.path.join(src_directory, filename)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dst_directory)
        else:
            subdst = os.path.join(dst_directory, filename)
            os.mkdir(subdst)
            copy_from_src_to_dst(full_file_name, subdst)
            
def main():
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    copy_from_src_to_dst(src, dst)
    generate_pages_recursive(ct, template_html, dst)
    
main()