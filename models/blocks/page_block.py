from parent_block import ParentBlock


class PageBlock(ParentBlock):
    def __init__(self, block_id, child_block_ids):
        super().__init__(block_id, -1, child_block_ids)

    @staticmethod
    def create(json_block):
        child_block_ids = []

        relationships = json_block.get('Relationships', [])
        for relationship in relationships:
            relationship_type = relationship.get('Type', '')
            if relationship_type == 'CHILD':
                child_block_ids = relationship.get('Ids', [])

        return PageBlock(
            block_id=json_block.get('Id', ''),
            child_block_ids=child_block_ids
        )
