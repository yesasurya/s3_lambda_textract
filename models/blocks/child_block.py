from models.blocks.block import Block


class ChildBlock(Block):
    def __init__(self, block_id, confidence):
        super().__init__(block_id, confidence)
