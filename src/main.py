from textnode import TextType, TextNode

def main():
	tn = TextNode("This is some anchor text",TextType.LINK,url="https://www.boot.dev")
	print(tn)


if __name__ == '__main__':
	main()