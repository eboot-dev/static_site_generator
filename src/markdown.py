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

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
	"""
		It takes a list of "old nodes", a delimiter with a matching TextNode type. It returns a new  
		list of nodes, where any "text" type nodes in the input list are (potentially) split into 
		multiple ones interleaved by nodes of the input-specified type. 
		Non "text" type nodes in the `old_nodes` list are returned as they are.
	"""
	new_nodes: list[TextNode] = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		parts = node.text.split(delimiter)
		if (len(parts) - 1) % 2 == 1:
			raise ValueError("Invalid Markdown: unmatched formatting delimiters")
		cnt: int = 0
		for part in parts:
			if cnt % 2 == 0:
				# even blocks are text nodes
				if part != "":
					new_nodes.append(TextNode(part,TextType.TEXT))
			else:
				# odd blocks are text_type nodes
				if part == "":
					raise ValueError("Invalid Markdown: empty formatted section")
				new_nodes.append(TextNode(part,text_type))
			cnt +=1

	return new_nodes

def markdown_to_textnodes(text: str) -> list[TextNode]:
	# Other parsing order:
	# BOLD (**) > ITALIC (_) > CODE (`) > IMAGE ![]() > LINK []()
	root = [TextNode(text,TextType.TEXT)]
	nodes = split_nodes_image(root)
	nodes = split_nodes_link(nodes)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
	return nodes








