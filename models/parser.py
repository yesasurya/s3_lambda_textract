class Parser:
    def __init__(self, textract_response):
        self.blocks = textract_response.get('Blocks', [])
        self.dict_block_by_ids = {}
        self.dict_block_by_types = {}

        for block in self.blocks:
            block_id = block.get('Id', '')
            self.dict_block_by_ids[block_id] = block

            block_type = block.get('BlockType', '')
            if block_type not in self.dict_block_by_types:
                self.dict_block_by_types[block_type] = []
            self.dict_block_by_types[block_type].append(block)
