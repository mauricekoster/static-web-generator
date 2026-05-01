from functools import reduce
import re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class BlockNode:
    ...



def markdown_to_blocks(markdown):
    blocks = re.split("\n\n", markdown)
    blocks = list(map(lambda b: b.strip(), blocks))
    blocks = list(filter(None, blocks))
    return blocks


def get_block_type(block):
    if block.startswith('#'):
            matches = re.findall(r"(#{1,6})\s+(.*)", block)
            if matches:
                return BlockType.HEADING
            else:
                return BlockType.PARAGRAPH

    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    elif block.startswith(">"):
        lines = block.split("\n")
        ok = True
        for l in lines:
            ok = ok and l.startswith('>')
        if ok:
            return BlockType.QUOTE
        else:
            return BlockType.PARAGRAPH

    elif block.startswith("-"):
        lines = block.split("\n")
        ok = True
        for l in lines:
            ok = ok and l.startswith('- ')
        if ok:
            return BlockType.UNORDERED_LIST
        else:
            return BlockType.PARAGRAPH

    elif re.match(r"\d+.", block):
        lines = block.split("\n")
        ok = True
        counter = 1
        for l in lines:
            m = re.findall(r"([\d]+).", l)
            if m:
                ok = ok and int(m[0]) == counter
            else:
                ok = False
            counter += 1
        if ok:
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH

    else:
        return BlockType.PARAGRAPH


def block_to_block_type(blocks):
    block_types = []
    for block in blocks:
        block_types.append(get_block_type(block))

    return block_types