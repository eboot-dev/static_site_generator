import unittest
from textnode import TextNode, TextType

from markdown import (
	extract_markdown_images, 
	extract_markdown_links,
	split_nodes_image,
	split_nodes_link
)

class TestMarkdownImagesAndLinkExtraction(unittest.TestCase):
	
	def test_images(self):
		text = "This is text with two images: ![of boot dev](https://www.boot.dev) and ![of youtube](https://www.youtube.com/@bootdotdev)"
		expected = [
			('of boot dev', 'https://www.boot.dev'), 
			('of youtube', 'https://www.youtube.com/@bootdotdev')
		]
		self.assertEqual(extract_markdown_images(text), expected)

	def test_images_without_alt_text(self):
		text = "This is text with two images: ![](https://www.boot.dev) and ![of youtube](https://www.youtube.com/@bootdotdev)"
		expected = [
			('', 'https://www.boot.dev'), 
			('of youtube', 'https://www.youtube.com/@bootdotdev')
		]
		self.assertEqual(extract_markdown_images(text), expected)

	def test_links(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		expected = [
			('to boot dev', 'https://www.boot.dev'), 
			('to youtube', 'https://www.youtube.com/@bootdotdev')
		]
		self.assertEqual(extract_markdown_links(text), expected)

	def test_links_mixed_with_images(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev) and an image ![to youtube](https://www.youtube.com/@bootdotdev)"
		expected = [
			('to boot dev', 'https://www.boot.dev')
		]
		self.assertEqual(extract_markdown_links(text), expected)

class TestMarkdownSplitImagesAndLink(unittest.TestCase):
	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
			],
			new_nodes,
		)
	
	def test_split_image(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
			],
			new_nodes,
		)

	def test_split_image_single(self):
		node = TextNode("![image](https://www.example.COM/IMAGE.PNG)",TextType.TEXT)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG")],
			new_nodes,
		)





if __name__ == "__main__":
	unittest.main()