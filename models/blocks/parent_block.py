from block import Block
from selection_element_block import SelectionElementBlock
from word_block import WordBlock


class ParentBlock(Block):
    def __init__(self, block_id, confidence, child_block_ids):
        super().__init__(block_id, confidence)
        self.child_block_ids = child_block_ids
        self.child_blocks = []

    def get_text_from_children(self):
        text = ''
        for block in self.child_blocks:
            if block.__class__.__name__ == SelectionElementBlock.__name__:
                text = text + block.selection_status + ' '
            elif block.__class__.__name__ == WordBlock.__name__:
                text = text + block.text + ' '
        return text
