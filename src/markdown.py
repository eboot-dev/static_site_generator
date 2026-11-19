import re
from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> list[tuple[str,str]]:
	# images
	# r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
	return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str,str]]:
	# regular links
	# r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
	return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		text = node.text
		images = extract_markdown_images(text)
		if len(images) == 0:
			new_nodes.append(node)
			continue
		for alt_text,url in images:
			sections = text.split(f"![{alt_text}]({url})", 1)
			if len(sections) != 2:
				raise ValueError("Invalid markdown, image not closed")
			preceding_text, text = sections
			if preceding_text != "":
				new_nodes.append(TextNode(preceding_text,TextType.TEXT))	
			new_nodes.append(TextNode(alt_text,TextType.IMAGE,url))

		if text != "":
			new_nodes.append(TextNode(text,TextType.TEXT))
	return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		text = node.text
		links = extract_markdown_links(text)
		if len(links) == 0:
			new_nodes.append(node)
			continue

		for link_text,url in links:
			sections = text.split(f"[{link_text}]({url})", 1)
			if len(sections) != 2:
				raise ValueError("invalid markdown, link not closed")

			preceding_text, text = sections
			if preceding_text != "":
				new_nodes.append(TextNode(preceding_text,TextType.TEXT))	
			new_nodes.append(TextNode(link_text,TextType.LINK,url))

		if text != "":
			new_nodes.append(TextNode(text,TextType.TEXT))
	
	return new_nodes






