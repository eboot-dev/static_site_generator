
class HTMLNode(object):
	"""HTMLNode class. It represents the different kinds of HTML tags"""
	
	# To fix list[HTMLNode] forward reference problem, 
	# use postponed evaluation of annotations (recommended):
	# 	from __future__ import annotations
	# otherwise use a string forward reference:
	# 	list["HTMLNode"]
	# See: https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class
	def __init__(self, 
					tag: str | None = None,  				# Kind of tag: p,h1,a,...
					value: str | None = None, 				# The value of/inside the tag
					children: list["HTMLNode"] = None, # The children nodes	
					props: dict[str,str] | None = None) -> None:	# Tag's poperties
		super().__init__()
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props
		

	def to_html(self) -> str:
		"""Turn a HTMLNode object into a formatted string contining the corresponding HTML code"""
		raise NotImplementedError("to_html method not implemented")

	def props_to_html(self) -> str:
		"""Turn the `prop` dictionary into a formatted string representing the HTML attributes for the node"""
		if self.props is None:
			return ""

		return " " + " ".join([ f"{k}=\"{v}\"" for k, v in sorted(self.props.items(), key=lambda item: item[0])])

	def __repr__(self) -> str:
		"""Gives the HTMLNode textual representation:
			HTMLNode(tag,value,props_to_html)
				child(1)
				child(2)
				....
			if tag, value or props are None use * instead
		"""
		tag_str: str = "*" if self.tag is None else self.tag
		value_str: str = "*" if self.value is None else self.value
		props_str: str = "*" if self.props is None else self.props_to_html()
		repr_str: str = f"HTMLNode({tag_str},{value_str},{props_str})"
		if self.children is None:
			return repr_str
				
		for c in self.children:
			c_strs: list[str] = repr(c).split("\n")
			for c_str in c_strs:
				repr_str += f"\n\t{c_str}"
		return repr_str



class LeafNode(HTMLNode):
	"""LeafNode: subclass of HTMLNode representing a leaf tag"""
	def __init__(self, tag: str | None, value: str, props: dict[str,str] | None = None) -> None:
		super().__init__(tag,value,None,props)

	def to_html(self) -> str:
		if self.value is None:
			raise ValueError("LeafNode.value can't be None")
		if self.tag is None:
			return self.value
		html_str = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
		return html_str

	def __repr__(self) -> str:
		"""Gives the LeafNode textual representation:
			LeafNode(tag,value,props_to_html)
			if tag or props are None use * instead
		"""
		tag_str: str = "*" if self.tag is None else self.tag
		props_str: str = "*" if self.props is None else self.props_to_html()
		return f"LeafNode({tag_str},{self.value},{props_str})"


class ParentNode(HTMLNode):
	"""LeafNode: subclass of HTMLNode representing a leaf tag"""
	def __init__(self, tag: str, children: list[HTMLNode], props: dict[str,str] | None = None) -> None:
		super().__init__(tag,None,children,props)

	def to_html(self) -> str:
		if self.tag is None:
			raise ValueError("LeafNode.tag can't be None")
		if self.children is None:
			raise ValueError("LeafNode.children can't be None")
		if len(self.children) == 0:
			raise ValueError("LeafNode.children can't be empty")
		
		html_str = f"<{self.tag}{self.props_to_html()}>"
		for child in self.children:
			html_str += child.to_html()
		return html_str + f"</{self.tag}>"

