from blocks.page_block import PageBlock
from blocks.line_block import LineBlock
from blocks.key_block import KeyBlock
from blocks.value_block import ValueBlock
from blocks.selection_element_block import SelectionElementBlock
from blocks.word_block import WordBlock


class BlockFactory:
    WANTED_BLOCK_TYPES = [
        'PAGE',
        'LINE',
        'KEY_VALUE_SET',
        'SELECTION_ELEMENT',
        'WORD',
    ]


    def __init__(self, api_response):
        self.api_response = api_response
        self.page_block = None
        self.line_blocks = {}
        self.key_blocks = {}
        self.value_blocks = {}
        self.other_blocks = {}

        self.__parse_blocks_from_response()
        self.__build_block_relationships()


    def __parse_blocks_from_response(self):
        json_blocks = self.api_response.get('Blocks', [])
        for json_block in json_blocks:
            block_type = json_block.get('BlockType', '')
            block_id = json_block.get('Id', '')
            if block_type in BlockFactory.WANTED_BLOCK_TYPES:
                if block_type == 'PAGE':
                    block = PageBlock.create(json_block)
                    self.page_block = block
                elif block_type == 'LINE':
                    block = LineBlock.create(json_block)
                    self.line_blocks[block_id] = block
                elif block_type == 'KEY_VALUE_SET':
                    entity_type = json_block['EntityTypes']
                    if 'KEY' in entity_type:
                        block = KeyBlock.create(json_block)
                        self.key_blocks[block_id] = block
                    elif 'VALUE' in entity_type:
                        block = ValueBlock.create(json_block)
                        self.value_blocks[block_id] = block
                    else:
                        print('[INFO]: Unable to determine the entity type of block {0}'.format(block_id))
                else:
                    if block_type == 'SELECTION_ELEMENT':
                        block = SelectionElementBlock.create(json_block)
                    elif block_type == 'WORD':
                        block = WordBlock.create(json_block)
                    self.other_blocks[block_id] = block
            else:
                print('[INFO]: Skipping block {0} because the type is {1}'.format(block_id, block_type))

    
    def __build_block_relationships(self):
        for other_block_id, other_block in self.other_blocks.items():
            for line_block_id, line_block in self.line_blocks.items():
                if other_block_id in line_block.child_block_ids:
                    other_block.line_block_id = line_block_id

        for _, key_block in self.key_blocks.items():
            for child_block_id in key_block.child_block_ids:
                key_block.child_blocks.append(self.other_blocks[child_block_id])
            for value_block_id in key_block.value_block_ids:
                key_block.value_blocks.append(self.value_blocks[value_block_id])

        for _, value_block in self.value_blocks.items():
            for child_block_id in value_block.child_block_ids:
                value_block.child_blocks.append(self.other_blocks[child_block_id])
