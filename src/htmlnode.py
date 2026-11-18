
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
					children: list["HTMLNode"] = [], # The children nodes	
					props: dict[str,str] | None = None):	# Tag's poperties
		super().__init__()
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props
		

	def to_html(self) -> str:
		"""Turn a HTMLNode object into a formatted string contining the corresponding HTML code"""
		raise NotImplementedError

	def props_to_html(self) -> str:
		"""Turn the `prop` dictionary into a formatted string representing the HTML attributes for the node"""
		if self.props is None:
			return ""
		return " " + " ".join([ f"{key}=\"{self.props[key]}\"" for key in self.props ])

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
		for c in self.children:
			c_strs: list[str] = repr(c).split("\n")
			for c_str in c_strs:
				repr_str += f"\n\t{c_str}"
		return repr_str



		