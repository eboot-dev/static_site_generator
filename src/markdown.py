from enum import Enum
import re
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode, HTMLNode

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

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

def markdown_to_blocks(markdown: str) -> list[str]:
	"""
		It takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings.
		Blocks are separated by a single blank line.
		Leading or trailing whitespaces are stripped out from each block.
	"""
	blocks = markdown.split("\n\n")
	processed_blocks = []
	for block in blocks:
		clean_block  = block.strip() # this strips also newlines and tabs
		if clean_block == "":
			continue
		processed_blocks.append(clean_block) 
	return processed_blocks

def block_to_block_type(block: str) -> BlockType:
	
	def is_quote(text: str):
		return text[0] == ">"
	
	def is_ul(text: str):
		return text.startswith("- ")
	
	def is_ol(text: str,position: int = 1):
		return text.startswith(f"{position}. ")
	
	def is_heading(text: str):
		return text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))

	lines = block.split("\n")
	if is_heading(block):
		return BlockType.HEADING if len(lines) == 1 else BlockType.PARAGRAPH
	
	if block.startswith("```\n") and block.endswith("```"):
		return BlockType.CODE
		
	if is_quote(block):
		for line in lines:
			if not is_quote(line):
				return BlockType.PARAGRAPH
		return BlockType.QUOTE
	
	if is_ul(block):
		for line in lines:
			if not is_ul(line):
				return BlockType.PARAGRAPH
		return BlockType.UNORDERED_LIST
	
	if is_ol(block):
		list_pos = 1
		for line in lines:
			if not is_ol(line,list_pos):
				return BlockType.PARAGRAPH
			list_pos += 1
		return BlockType.ORDERED_LIST
		
	return BlockType.PARAGRAPH


def text_to_nodes(text: str) -> list[LeafNode]:
	text_nodes = markdown_to_textnodes(text)
	return [text_node_to_html_node(text_node) for text_node in text_nodes ]

def markdown_to_html_node(markdown: str) -> ParentNode:
	root: ParentNode = ParentNode("div",[])
	blocks = markdown_to_blocks(markdown)
	for block in blocks:
		block_type: BlockType = block_to_block_type(block)
		match block_type:
			case BlockType.PARAGRAPH:
				children = text_to_nodes(block)
				root.children.append(ParentNode("p",children))
			case BlockType.HEADING:
				prefix,line = block.split(" ",1)
				children = text_to_nodes(line)
				head_node = ParentNode(f"h{len(prefix)}",children)
				root.children.append(head_node)
			case BlockType.CODE:
				code_block = block[4:-3]
				code_text_node = LeafNode(None,code_block)
				root.children.append(ParentNode("pre",[
					ParentNode("code",[code_text_node])
					]
					)
				)
			case BlockType.QUOTE:
				quote_text = "\n".join([line[1:].strip() for line in block.split("\n")]) 
				p_children = text_to_nodes(quote_text)
				blockquote_node = ParentNode("blockquote",p_children)
				# quote_node = ParentNode("p",p_children)
				# blockquote_node = ParentNode("blockquote",[quote_node])
				root.children.append(blockquote_node)
			case BlockType.UNORDERED_LIST:
				ul_node_children = []
				for line in block.split("\n"):
					li_children = text_to_nodes(line)
					ul_node_children.append(ParentNode("li",li_children))

				ul_node = ParentNode("ul",ul_node_children)
				root.children.append(ul_node)
			case BlockType.ORDERED_LIST:
				ol_node_children = []
				for line in block.split("\n"):
					li_children = text_to_nodes(line.split(". ",1)[1])
					ol_node_children.append(ParentNode("li",li_children))
				ol_node = ParentNode("ol",ol_node_children)
				root.children.append(ol_node)
			case _:
				raise ValueError("Invalid block type")

	return root

