from models.blocks.child_block import ChildBlock


class SelectionElementBlock(ChildBlock):
    def __init__(self, block_id, confidence, selection_status):
        super().__init__(block_id, confidence)
        self.selection_status = selection_status
        self.line_block_id = ''

    @staticmethod
    def create(json_block):
        return SelectionElementBlock(
            block_id=json_block.get('Id', ''),
            confidence=json_block.get('Confidence', 0),
            selection_status=json_block.get('SelectionStatus', '')
        )
