import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
	"""Unit Tests for TextNode"""

	def test_eq(self):
		""" Test TextNode.__eq__ with two equal nodes"""
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_repr(self):
		""" Test TextNode.__repr__"""
		node = TextNode("This is a text node", TextType.BOLD,url="https://localhost:8888")
		self.assertEqual("TextNode(This is a text node, bold, https://localhost:8888)",repr(node))

	def test_repr_none_url(self):
		""" Test TextNode.__repr__ with url=None"""
		node = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual("TextNode(This is a text node, bold, None)",repr(node))

	def test_neq_text(self):
		""" Test TextNode.__eq__ with two nodes with different texts"""
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a link node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_neq_types(self):
		""" Test TextNode.__eq__ with two nodes with different Types"""
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)

	def test_neq_url(self):
		""" Test TextNode.__eq__ with two nodes with different urls"""
		node = TextNode("This is a link node", TextType.LINK,url="https://localhost:8888")
		node2 = TextNode("This is a link node", TextType.LINK,url="https://localhost:6969")
		self.assertNotEqual(node, node2)

	def test_neq_url_none(self):
		""" Test TextNode.__eq__ with two nodes with different urls of which one is None"""
		node = TextNode("This is a link node", TextType.LINK,url="https://localhost:8888")
		node2 = TextNode("This is a link node", TextType.LINK)
		self.assertNotEqual(node, node2)

	def test_text_to_html(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")
		self.assertEqual(html_node.to_html(), "This is a text node")

	def test_italic_to_html(self):
		node = TextNode("This is an italic node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is an italic node")
		self.assertEqual(html_node.to_html(), "<i>This is an italic node</i>")

	def test_bold_to_html(self):
		node = TextNode("This is a bold node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a bold node")
		self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")

	def test_code_to_html(self):
		node = TextNode("This is a code node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a code node")
		self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")

	def test_link_to_html(self):
		node = TextNode("This is a link node", TextType.LINK,"http://localhost:8888")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a link node")
		self.assertEqual(html_node.props["href"], "http://localhost:8888")
		self.assertEqual(html_node.to_html(), "<a href=\"http://localhost:8888\">This is a link node</a>")

	def test_image_to_html(self):
		node = TextNode("This is an img node", TextType.IMAGE,"http://localhost:8888")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.props["alt"], "This is an img node")
		self.assertEqual(html_node.props["src"], "http://localhost:8888")
		self.assertEqual(html_node.to_html(), "<img alt=\"This is an img node\" src=\"http://localhost:8888\"></img>")

	def test_to_html_bad_type(self):
		""" Test text_node_to_html with invalid type"""
		node = TextNode("This is an img node", None,"http://localhost:8888")
		with self.assertRaises(ValueError):
			html_node = text_node_to_html_node(node)
			

if __name__ == "__main__":
	unittest.main()