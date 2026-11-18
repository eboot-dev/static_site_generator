import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
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


if __name__ == "__main__":
	unittest.main()