from models.blocks.child_block import ChildBlock


class WordBlock(ChildBlock):
    def __init__(self, block_id, confidence, text, text_type):
        super().__init__(block_id, confidence)
        self.text = text
        self.text_type = text_type
        self.line_block_id = ''

    @staticmethod
    def create(json_block):
        return WordBlock(
            block_id=json_block.get('Id', ''),
            confidence=json_block.get('Confidence', 0),
            text=json_block.get('Text', ''),
            text_type=json_block.get('TextType', '')
        )
