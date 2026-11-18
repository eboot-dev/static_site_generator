import unittest
from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
	"""Unit Tests for TextNode"""

	def test_to_html(self):
		""" Test ParentNode.to_html"""
		node = ParentNode(
				"p",
				[
					LeafNode("b", "Bold text"),
					LeafNode(None, "Normal text"),
					LeafNode("i", "italic text"),
					LeafNode(None, "Normal text"),
				],
		)
		self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", node.to_html())

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual("<div><span>child</span></div>",parent_node.to_html())


	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
				"<div><span><b>grandchild</b></span></div>",
				parent_node.to_html()
				)

	def test_to_html_empty_children(self):
		""" Test ParentNode.to_html with empty children"""
		node = ParentNode("p",[])
		with self.assertRaises(ValueError):
			node.to_html()


	def test_to_html_None_children(self):
		""" Test ParentNode.to_html with children set to None"""
		with self.assertRaises(ValueError):
			node = ParentNode("p",None)
			node.to_html()

if __name__ == "__main__":
    unittest.main()			