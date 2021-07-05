from models.parser import Parser


class FormParser(Parser):
    def __init__(self, textract_response):
        super().__init__(textract_response)
        block_lines = self.dict_block_by_types.get('LINE', [])
        line_texts = []
        for block_line in block_lines:
            line_texts.append(block_line.get('Text', ''))
        
        block_key_values = self.dict_block_by_types.get('KEY_VALUE_SET', [])
        block_keys = []
        for block in block_key_values:
            entity_types = block.get('EntityTypes', [])
            if 'KEY' in entity_types:
                block_keys.append(block)

        unsorted_pairs = []
        for block_key in block_keys:
            unsorted_pairs.append(self.__get_pair_from_block_key(block_key))

        self.sorted_pairs = []

        for line_text in line_texts:
            for index, pair in enumerate(unsorted_pairs):
                key = pair.get('key', None)
                if key is not None and key in line_text:
                    self.sorted_pairs.append(pair)
                    unsorted_pairs[index] = {}
                    break
        for pair in unsorted_pairs:
            key = pair.get('key', None)
            if key is not None:
                self.sorted_pairs.append(pair)
    

    def get_csv_lines(self):
        csv_lines = []
        for pair in self.sorted_pairs:
            csv_line = '{0}, {1}\n'.format(pair['key'], pair['value'])
            csv_lines.append(csv_line)
        return csv_lines


    def __get_pair_from_block_key(self, block_key):
        text_key = self.__get_text_from_block_key(block_key)

        block_value_ids = []

        relationships = block_key.get('Relationships', [])
        for relationship in relationships:
            relationship_type = relationship.get('Type', '')
            if relationship_type == 'VALUE':
                block_value_ids = relationship.get('Ids', [])
        
        text_value = ''
        for block_value_id in block_value_ids:
            block_value = self.dict_block_by_ids[block_value_id]
            text_value = text_value + self.__get_text_from_block_value(block_value)

        return {
            'key': text_key,
            'value': text_value
        }


    def __get_text_from_block_key(self, block_key):
        block_word_ids = []

        relationships = block_key.get('Relationships', [])
        for relationship in relationships:
            relationship_type = relationship.get('Type', '')
            if relationship_type == 'CHILD':
                block_word_ids = relationship.get('Ids', [])

        text = ''
        for block_word_id in block_word_ids:
            block_word = self.dict_block_by_ids[block_word_id]
            text = text + ' ' + self.__get_text_from_block_word(block_word)
        text = text[1:]
    
        return text


    def __get_text_from_block_value(self, block_value):
        block_word_ids = []

        relationships = block_value.get('Relationships', [])
        for relationship in relationships:
            relationship_type = relationship.get('Type', '')
            if relationship_type == 'CHILD':
                block_word_ids = relationship.get('Ids', [])

        text = ''
        for block_word_id in block_word_ids:
            block_word = self.dict_block_by_ids[block_word_id]
            text = text + ' ' + self.__get_text_from_block_word(block_word)
        text = text[1:]
    
        return text


    def __get_text_from_block_word(self, block_word):
        text = block_word.get('Text', '')
        if text == '':
            text = block_word.get('SelectionStatus', '')
        return text
