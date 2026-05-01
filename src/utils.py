from pathlib import Path
import re
import shutil
from typing import List

from blocks import BlockType, get_block_type, markdown_to_blocks
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

REGEX_IMAGES = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
REGEX_LINKS = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, value=text_node.text)
        
        case TextType.BOLD:
            return LeafNode("b", value=text_node.text)
        
        case TextType.ITALIC:
            return LeafNode("i", value=text_node.text)
        
        case TextType.CODE:
            return LeafNode("code", value=text_node.text)
        
        case TextType.LINK:
            return LeafNode("a", value=text_node.text, props={'href': text_node.url})
        
        case TextType.IMAGE:
            return LeafNode("img", value=text_node.text, props={'alt': text_node.text, 'src': text_node.url})
        
        case _:
            raise Exception("Unknown TextType")


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            # if number of part is even, a delimeter is missing
            raise ValueError("Invalid Markdown. Unbalanced delimiter")
        
        
        #print(parts)
        inside = False
        for part in parts:
            
            if part.strip() == '':
                inside = not inside
                continue

            if inside:
                node = TextNode(part, text_type)
            else:
                node = TextNode(part, TextType.TEXT)

            inside = not inside
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(REGEX_IMAGES, text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(REGEX_LINKS, text)
    return matches


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = re.split(REGEX_IMAGES, text)

        inside = False
        while matches:
            if inside:
                text = matches.pop(0)
                link = matches.pop(0)
                node = TextNode(text, TextType.IMAGE, url=link)

            else:
                m = matches.pop(0)
                if m.strip() == '':
                    inside = not inside
                    continue

                node = TextNode(m, TextType.TEXT)

            new_nodes.append(node)
            inside = not inside

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes: List[TextNode] = []
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = re.split(REGEX_LINKS, text)

        inside = False
        while matches:
            if inside:
                text = matches.pop(0)
                link = matches.pop(0)
                node = TextNode(text, TextType.LINK, url=link)

            else:
                m = matches.pop(0)
                if m.strip() == '':
                    inside = not inside
                    continue
                
                node = TextNode(m, TextType.TEXT)

            new_nodes.append(node)
            inside = not inside

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def block_to_html_node(block):
    block_type = get_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            nodes = text_to_textnodes(text)
            html_nodes = [text_node_to_html_node(n) for n in nodes]
            return ParentNode("p", html_nodes)
            
        case BlockType.HEADING:
            matches = re.findall(r"(#{1,6})\s+(.*)", block)
            hashes, text = matches[0]
            level = len(hashes)
            tag = f"h{level}"
            return LeafNode(tag, text)
        

        case BlockType.CODE:
            lines = block.split("\n")
            lines = lines[1:-1]
            code = "\n".join(lines) + "\n"
            return ParentNode("pre",children=[LeafNode("code", code)])

        case BlockType.QUOTE:
            lines = []
            for line in block.split("\n"):
                line = line.lstrip(">")
                line = line.strip()
                lines.append(line)
            
            return LeafNode("blockquote", "\n".join(lines))
        
        case BlockType.UNORDERED_LIST:
            list_items = []
            for line in block.split("\n"):
                line = line.lstrip("-")
                line = line.strip()

                nodes = text_to_textnodes(line)
                html_nodes = [text_node_to_html_node(n) for n in nodes]
                list_items.append(ParentNode("li", children=html_nodes))

            return ParentNode("ul", children=list_items)

            

        case BlockType.ORDERED_LIST:
            list_items = []
            for line in block.split("\n"):
                matches = re.findall(r"(\d+\.)\s+(.*)", line)
                _, text = matches[0]

                nodes = text_to_textnodes(text.strip())
                html_nodes = [text_node_to_html_node(n) for n in nodes]
                list_items.append(ParentNode("li", children=html_nodes))

            return ParentNode("ol", children=list_items)

        case _:
            return LeafNode("p", f"NOT YET IMPLEMENTED TYPE: {block_type}")


def markdown_to_html_node(markdown): 
    blocks = markdown_to_blocks(markdown)

    nodes = []
    for block in blocks:
        
        html_node = block_to_html_node(block)
        nodes.append(html_node)

    div = ParentNode("div", children=nodes)
    return div


def copytree(src: Path, dst: Path):
    for file in src.glob("*"):
        if file.is_dir():
            p = dst / file.name
            p.mkdir()
            print(f"Copy folder: {src / file.name}")
            copytree(src / file.name, p)
        else:
            print(f"Copy file: {src / file.name} -> {dst / file.name}")
            shutil.copy(src/ file.name, dst / file.name)



def copy_static_assets():
    public_path = Path.cwd() / 'public'
    static_path = Path.cwd() / 'static'

    shutil.rmtree(public_path)
    public_path.mkdir(exist_ok=True)

    copytree(static_path, public_path)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    h1_blocks = list(filter(lambda b: b.startswith('# '), blocks))
    if not h1_blocks:
        raise Exception("Invalid markdown. No title found.")
    
    matches = re.findall(r"(#{1,6})\s+(.*)", h1_blocks[0])
    _, title = matches[0]
    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown)
    content = node.to_html()

    title = extract_title(markdown)

    html = template.replace('{{ Title }}', title)
    html = html.replace('{{ Content }}', content)

    dp = Path(dest_path)
    dp.parent.mkdir(parents=True, exist_ok=True)
    with open(dp, "w") as f:
        f.write(html)



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    p = Path(dir_path_content)

    for file in p.glob('*'):
        f = Path(file)

        if f.is_dir():

            generate_pages_recursive(f, template_path, Path(dest_dir_path) / file.name)

        else:
            
            generate_page(f, template_path, Path(dest_dir_path) / (file.stem + '.html'))