import unittest
from textnode import TextNode, TextType

from markdown import (	
	extract_markdown_images, 
	extract_markdown_links,
	split_nodes_delimiter,
	split_nodes_image,
	split_nodes_link,
	markdown_to_textnodes,
	markdown_to_blocks,
	markdown_to_html_node,
	BlockType,
	block_to_block_type
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

	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)


		def test_markdown_to_blocks_newlines(self):
			md = """
This is **bolded** paragraph






	This is another paragraph with _italic_ text and `code` here
	This is the same paragraph on a new line

- This is a list
- with items
"""
			blocks = markdown_to_blocks(md)
			self.assertEqual(
				blocks,
				[
					"This is **bolded** paragraph",
					"This is another paragraph with _italic_ text and `code` here\n\tThis is the same paragraph on a new line",
					"- This is a list\n- with items",
				],
			)

class TestMarkdownBlockToBlockTypes(unittest.TestCase):
	def test_block_to_block_type_paragraph(self):
		text="""This is **bolded** paragraph
with multiple 
lines....
......
""" 
		self.assertEqual(block_to_block_type(text.strip()),BlockType.PARAGRAPH)

	def test_block_to_block_type_ul(self):
		text="""- line1
- line2
- line3
- line3.5
-  
- 
- line4
""" 
		self.assertEqual(block_to_block_type(text.strip()),BlockType.UNORDERED_LIST)

	def test_block_to_block_type_ol(self):
		text="""1. line1
2. line2
3. line3
4. line3.5
5. line4
""" 
		self.assertEqual(block_to_block_type(text.strip()),BlockType.ORDERED_LIST)

	def test_block_to_block_type_code(self):
		text="""```
some code
28912198392.line4
```
""" 
		self.assertEqual(block_to_block_type(text.strip()),BlockType.CODE)

	def test_block_to_block_type_quote(self):
		text=""">line1
>line2
> line3
> line3.5
>  
>
>line4
""" 
		self.assertEqual(block_to_block_type(text.strip()),BlockType.QUOTE)

	def test_block_to_block_type_heading1(self):
		text="# ciao"
		self.assertEqual(block_to_block_type(text.strip()),BlockType.HEADING)

	def test_block_to_block_type_heading2(self):
		text="## ciao"
		self.assertEqual(block_to_block_type(text.strip()),BlockType.HEADING)

	def test_block_to_block_type_heading5(self):
		text="##### ciao"
		self.assertEqual(block_to_block_type(text.strip()),BlockType.HEADING)

	def test_block_to_block_type_heading6(self):
		text="###### ciao"
		self.assertEqual(block_to_block_type(text.strip()),BlockType.HEADING)

	def test_block_to_block_type_heading_too_long(self):
		text="####### ciao "
		self.assertEqual(block_to_block_type(text.strip()),BlockType.PARAGRAPH)

	def test_block_to_block_type_bad(self):
		text=""">line1
-line2
1. line3
> line3.5
>  
>
>line4
""" 
		self.assertEqual(block_to_block_type(text.strip()),BlockType.PARAGRAPH)

class TestMarkdownToHTMLNode(unittest.TestCase):
	def test_markdown_to_html_node(self):
		md = """
# heading1

This is **bolded** and *italic* paragraph
text in a p
tag here image ![image here](http://localhost)

##### heading 5 with *italic* and **bold** and [link](http://localhost)

This is another paragraph with _italic_ text and `code` here

```
codeblock
adad
adsdas
```

Unordered List

- ul1 **bold**
- ul2 *italic*
- ul3 `code`

Ordered List

1. ol1 **bold**
2. ol2 *italic*
3. ol3
4. ol4 image ![image here](http://localhost)
5. ol5
6. ol6  [link here](http://localhost)
7. ol7
8. ol8
9. ol9
10. ol10

> This is
> a
>quote that keeps style **bold**
>initial spaces *italic*
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = """<div><h1>heading1</h1><p>This is <b>bolded</b> and <i>italic</i> paragraph
text in a p
tag here image <img alt="image here" src="http://localhost"></img></p><h5>heading 5 with <i>italic</i> and <b>bold</b> and <a href="http://localhost">link</a></h5><p>This is another paragraph with _italic_ text and <code>code</code> here</p><pre><code>codeblock
adad
adsdas
</code></pre><p>Unordered List</p><ul><li>- ul1 <b>bold</b></li><li>- ul2 <i>italic</i></li><li>- ul3 <code>code</code></li></ul><p>Ordered List</p><ol><li>ol1 <b>bold</b></li><li>ol2 <i>italic</i></li><li>ol3</li><li>ol4 image <img alt="image here" src="http://localhost"></img></li><li>ol5</li><li>ol6  <a href="http://localhost">link here</a></li><li>ol7</li><li>ol8</li><li>ol9</li><li>ol10</li></ol><blockquote><p> This is
 a
quote that keeps style <b>bold</b>
initial spaces <i>italic</i></p></blockquote></div>"""
		self.assertEqual(expected,html)

	
if __name__ == "__main__":
	unittest.main()