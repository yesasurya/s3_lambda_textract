from models.blocks.parent_block import ParentBlock


class ValueBlock(ParentBlock):
    def __init__(self, block_id, confidence, child_block_ids):
        super().__init__(block_id, confidence, child_block_ids)

    @staticmethod
    def create(json_block):
        child_block_ids = []

        relationships = json_block.get('Relationships', [])
        for relationship in relationships:
            relationship_type = relationship.get('Type', '')
            if relationship_type == 'CHILD':
                child_block_ids = relationship.get('Ids', [])

        return ValueBlock(
            block_id=json_block.get('Id', ''),
            confidence=json_block.get('Confidence', 0),
            child_block_ids=child_block_ids
        )
