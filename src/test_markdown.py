import unittest
from textnode import TextNode, TextType

from markdown import (	
	extract_markdown_images, 
	extract_markdown_links,
	split_nodes_delimiter,
	split_nodes_image,
	split_nodes_link,
	markdown_to_textnodes
)		

class TestMarkdownSplitDelimiter(unittest.TestCase):
	def test_split_code(self):
		node = TextNode("This is a `code` node", TextType.TEXT)
		expected = [ 
			TextNode("This is a ", TextType.TEXT),
			TextNode("code", TextType.CODE),
			TextNode(" node", TextType.TEXT)
		]
		observed = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(observed, expected)

	def test_split_bold(self):
		node = TextNode("This is a **bold** node", TextType.TEXT)
		expected = [ 
			TextNode("This is a ", TextType.TEXT),
			TextNode("bold", TextType.BOLD),
			TextNode(" node", TextType.TEXT)
		]
		observed = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(observed, expected)

	def test_split_italics(self):
		node = TextNode("This is a *italics* node", TextType.TEXT)
		expected = [ 
			TextNode("This is a ", TextType.TEXT),
			TextNode("italics", TextType.ITALIC),
			TextNode(" node", TextType.TEXT)
		]
		observed = split_nodes_delimiter([node], "*", TextType.ITALIC)
		self.assertEqual(observed, expected)

	def test_split_single(self):
		node = TextNode("`This is a single code node`", TextType.TEXT)
		expected = [ 
			TextNode("This is a single code node", TextType.CODE)
		]
		observed = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(observed, expected)

	def test_split_nothing_found(self):
		node = TextNode("This is just a text node", TextType.TEXT)
		expected = [ 
			node
		]
		observed = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(observed, expected)

	def test_split_bad_node(self):
		node = TextNode("This is a **italics** node", TextType.TEXT)
		with self.assertRaises(ValueError):
			observed = split_nodes_delimiter([node], "*", TextType.ITALIC)
		
	def test_split_unmatched_delimiters(self):
		node = TextNode("This is a *italics node", TextType.TEXT)
		with self.assertRaises(ValueError):
			observed = split_nodes_delimiter([node], "*", TextType.ITALIC)

	
	def test_delim_bold_and_italic(self):
		node = TextNode("**bold** and _italic_", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
		self.assertListEqual(
			[
				TextNode("bold", TextType.BOLD),
				TextNode(" and ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
			],
			new_nodes,
		)

	def test_delim_bold_multiword(self):
		node = TextNode(
			"This is text with a **bolded word** and **another**", TextType.TEXT
		)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("bolded word", TextType.BOLD),
				TextNode(" and ", TextType.TEXT),
				TextNode("another", TextType.BOLD),
			],
			new_nodes,
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

class TestMarkdownToTextNodes(unittest.TestCase):

	def test_markdown_to_textnodes(self):
		text ="This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		expected = [
			TextNode("This is ", TextType.TEXT),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.TEXT),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ", TextType.TEXT),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.TEXT),
			TextNode("link", TextType.LINK, "https://boot.dev"),
		]
		self.assertListEqual(markdown_to_textnodes(text),expected )

if __name__ == "__main__":
	unittest.main()