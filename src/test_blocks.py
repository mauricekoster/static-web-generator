import unittest

from blocks import BlockType, block_to_block_type, markdown_to_blocks

class TestBlocks(unittest.TestCase):
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


    def test_block_types_paragraph(self):
        blocks = [
            "Just text"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.PARAGRAPH], block_types
        )

    def test_block_types_heading(self):
        blocks = [
            "### Heading 3",
            "Just text"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.HEADING, BlockType.PARAGRAPH], block_types

        )

    def test_block_types_code(self):
        blocks = [
            "```Just text\nAnother line```"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.CODE], block_types

        )

    def test_block_types_quote(self):
        blocks = [
            "> Just text"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.QUOTE], block_types

        )

    def test_block_types_quote_multiline(self):
        blocks = [
            "> Just text\n> Another line"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.QUOTE], block_types

        )

    def test_block_types_quote_not_valid(self):
        blocks = [
            "> Just text\nNot valid"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.PARAGRAPH], block_types

        )

    
    def test_block_types_ul(self):
        blocks = [
            "- Just text"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.UNORDERED_LIST], block_types

        )

    def test_block_types_ul_multiline(self):
        blocks = [
            "- Just text\n- Another line"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.UNORDERED_LIST], block_types

        )

    def test_block_types_ul_not_valid(self):
        blocks = [
            "- Just text\nNot valid"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.PARAGRAPH], block_types

        )

    
    def test_block_types_ol(self):
        blocks = [
            "1. Just text"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.ORDERED_LIST], block_types

        )

    def test_block_types_ol_multiline(self):
        blocks = [
            "1. Just text\n2. Another line"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.ORDERED_LIST], block_types

        )

    def test_block_types_ol_multiline_not_incrementing(self):
        blocks = [
            "1. Just text\n1. Another line"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.PARAGRAPH], block_types

        )

    def test_block_types_ol_not_valid(self):
        blocks = [
            "1. Just text\nNot valid"
        ]
        block_types = block_to_block_type(blocks)
        self.assertEqual(len(blocks), len(block_types))
        self.assertListEqual(
            [BlockType.PARAGRAPH], block_types

        )