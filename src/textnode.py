from enum import Enum

class TextType(Enum):
	PLAIN = "plain"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"


class TextNode(object):
	"""TextNode class. It represents the different kinds of text blocks"""
	def __init__(self, text, text_type, url=None):
		super(TextNode, self).__init__()
		self.text = text
		self.text_type = text_type
		self.url = url
		
	def __eq__(self, other):

		return (
			(self.text == other.text) and 
			(self.text_type == other.text_type) and
			(self.url == other.url) 
			)

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"