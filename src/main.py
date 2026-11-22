from markdown import markdown_to_html_node, extract_title
import shutil as sh
import os

PUBLIC_DIR_PATH = "public"
STATIC_DIR_PATH = "static"

def copy_files(src_path: str,dst_path: str) -> None:
	dir_content = os.listdir(path=src_path)
	for elem in dir_content:
		dst_elem_path = os.path.join(dst_path,elem)
		src_elem_path = os.path.join(src_path,elem)
		if os.path.isfile(src_elem_path):
			print(f"COPY '{src_elem_path}' => '{dst_elem_path}'")
			sh.copy(src_elem_path, dst_elem_path,follow_symlinks=True)
		elif os.path.isdir(src_elem_path):
			os.mkdir(dst_elem_path)
			print(f"MKDIR '{dst_elem_path}'")
			copy_files(src_elem_path, dst_elem_path)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
	print(f"Generating page from '{from_path}' to '{dest_path}' using template '{template_path}'")
	with open(from_path,"r") as f:
		md_file_content = f.read()

	with open(template_path,"r") as f:
		template = f.read()

	html_node = markdown_to_html_node(md_file_content)
	html_code = html_node.to_html()
	title = extract_title(md_file_content)
	page = template.replace("{{ Title }}",title).replace("{{ Content }}",html_code)
	
	dest_dir_path = os.path.dirname(dest_path)
	if dest_dir_path != "":
		os.makedirs(dest_dir_path, exist_ok=True)
	# if not os.path.exists(os.path.dirname(dest_path)):
	# 	os.makedirs(os.path.dirname(dest_path))
	with open(dest_path,"w") as f:
		f.write(page)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
	dir_content = os.listdir(path=dir_path_content)
	for elem in dir_content:
		src_elem_path = os.path.join(dir_path_content,elem)
		if os.path.isfile(src_elem_path) and elem.endswith(".md"):
			generate_page(src_elem_path, template_path, 
				os.path.join(dest_dir_path,elem.replace(".md",".html")) )
		elif os.path.isdir(src_elem_path):
			dst_elem_path = os.path.join(dest_dir_path,elem)
			os.mkdir(dst_elem_path)
			print(f"MKDIR '{dst_elem_path}'")
			generate_pages_recursive(src_elem_path, template_path, dst_elem_path)

def generate_site() -> None:
	# clean and recreate "public" folder
	if os.path.exists(PUBLIC_DIR_PATH):
		sh.rmtree(PUBLIC_DIR_PATH)
	os.mkdir(PUBLIC_DIR_PATH)
	# copy file from static to pulic
	print("Copying static files...")
	copy_files(STATIC_DIR_PATH,PUBLIC_DIR_PATH)
	generate_pages_recursive("content", "template.html", "public")

def main() -> None:
	print("Generate Site...")
	generate_site()
	print("Site generated")


if __name__ == '__main__':
	main()