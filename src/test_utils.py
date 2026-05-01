import unittest

from textnode import TextNode, TextType
from utils import extract_markdown_links, extract_title, split_nodes_image, split_nodes_link, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, text_to_textnodes

class TestUtils(unittest.TestCase):
    def test_text(self):
        text = "Hello world!"
        node = TextNode(text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, text)

    def test_bold(self):
        text = "Hello world!"
        node = TextNode(text, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, text)

    def test_italic(self):
        text = "Hello world!"
        node = TextNode(text, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, text)


    def test_code(self):
        text = "Hello world!"
        node = TextNode(text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, text)


    def test_link(self):
        text = "Hello world!"
        url = "https://www.google.com"
        node = TextNode(text, TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, text)
        self.assertEqual(html_node.props['href'], url)

    def test_image(self):
        text = "Hello world!"
        url = "https://www.google.com"
        node = TextNode(text, TextType.IMAGE, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.props['alt'], text)
        self.assertEqual(html_node.props['src'], url)


    def test_split_empty(self):
        nodes = []
        new_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertListEqual(new_nodes, [])

    def test_split_plain_text(self):
        nodes = [TextNode('Test mij', TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode('Test mij', TextType.TEXT)])

    def test_split_no_text(self):
        nodes = [TextNode('Test mij', TextType.CODE)]
        new_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode('Test mij', TextType.CODE)])

    def test_split_only_bold(self):
        nodes = [TextNode('**Test**', TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode('Test', TextType.BOLD)])

    def test_split_two_bold(self):
        nodes = [TextNode('**Test****MIJ**', TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode('Test', TextType.BOLD), TextNode('MIJ', TextType.BOLD)])

    def test_split_two_bold_between(self):
        nodes = [TextNode('**Test** ook **MIJ**', TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode('Test', TextType.BOLD), TextNode(' ook ', TextType.TEXT), TextNode('MIJ', TextType.BOLD)])

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        values = extract_markdown_images(text)
        self.assertListEqual(values, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        values = extract_markdown_links(text)
        self.assertListEqual(values, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    
    def test_split_just_an_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )


    def test_split_image_but_it_is_a_link(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("[link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            ],
            new_nodes,
        )


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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ], new_nodes)
        

    def test_inline_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
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
            ], nodes
        )

    def test_extract_title(self):
        md = """
# Title

## Sub title

# Another title?
"""
        title = extract_title(md)

        self.assertEqual("Title", title)


    def test_extract_title_not_found(self):
        md = """
## Sub title

Text
"""
        with self.assertRaises(Exception):
            title = extract_title(md)
