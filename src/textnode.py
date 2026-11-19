from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"


class TextNode(object):
	"""TextNode class. It represents the different kinds of text blocks"""
	def __init__(self, text: str, text_type: TextType, url: str | None = None):
		super().__init__()
		self.text = text
		self.text_type = text_type
		self.url = url
		
	def __eq__(self, other: object) -> bool:
		if not isinstance(other, TextNode):
			return False
		return (
			(self.text == other.text) and 
			(self.text_type == other.text_type) and
			(self.url == other.url) 
			)

	def __repr__(self) -> str:
		"""Gives the TextNode textual representation"""
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
	"""Convert a TextNode into the corresponding LeafNode"""
	node_type: TextType = text_node.text_type
	html_node: LeafNode = None
	match node_type:
		case TextType.TEXT:
			html_node = LeafNode(None,text_node.text)
		case TextType.BOLD:
			html_node = LeafNode("b",text_node.text)
		case TextType.ITALIC:
			html_node = LeafNode("i",text_node.text)
		case TextType.CODE:
			html_node = LeafNode("code",text_node.text)
		case TextType.LINK:
			if text_node.url is None:
				raise ValueError("Invalid URL")
			if text_node.url == "":
				raise ValueError("Empty URL")
			html_node = LeafNode("a",text_node.text,props={"href":text_node.url})
		case TextType.IMAGE:
			if text_node.url is None:
				raise ValueError("Invalid URL")
			if text_node.url == "":
				raise ValueError("Empty URL")
			html_node = LeafNode("img","",props={"alt":text_node.text,"src":text_node.url})
		case _:
			raise ValueError(f"Invalid TextType: {text_node.text_type}")
	return html_node

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



