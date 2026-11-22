from textnode import TextType, TextNode
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
def generate_site() -> None:
	# clean and recreate "public" folder
	if os.path.exists(PUBLIC_DIR_PATH):
		sh.rmtree(PUBLIC_DIR_PATH)
	os.mkdir(PUBLIC_DIR_PATH)
	# copy file from static to pulic
	print("Copying static files...")
	copy_files(STATIC_DIR_PATH,PUBLIC_DIR_PATH)

def main() -> None:
	print("Generate Site...")
	generate_site()
	print("Site generated")


if __name__ == '__main__':
	main()