from models.parser import Parser


class TableParser(Parser):
    TABLE_MAX_ROW = 10
    TABLE_MAX_COL = 10

    def __init__(self, textract_response):
        super().__init__(textract_response)
        block_tables = self.dict_block_by_types.get('TABLE', [])
        self.tables = []
        for block_table in block_tables:
            self.tables.append(self.__get_table_from_block_table(block_table))

    
    def get_csv_lines(self):
        csv_lines = []
        for table in self.tables:
            for row in range(TableParser.TABLE_MAX_ROW):
                csv_line = ''
                for col in range(TableParser.TABLE_MAX_COL):
                    text = table[row][col]
                    if text is not None:
                        csv_line = csv_line + '"{0}", '.format(text)
                if csv_line != '':
                    csv_line = csv_line[:-2] + '\n'
                    csv_lines.append(csv_line)

        return csv_lines


    def __get_table_from_block_table(self, block_table):
        block_cell_ids = []
        relationships = block_table.get('Relationships', [])
        for relationship in relationships:
            relationship_type = relationship.get('Type', '')
            if relationship_type == 'CHILD':
                block_cell_ids = relationship.get('Ids', [])

        table = [[None for i in range(TableParser.TABLE_MAX_COL)] for y in range(TableParser.TABLE_MAX_ROW)]
        for block_cell_id in block_cell_ids:
            block_cell = self.dict_block_by_ids[block_cell_id]
            row, col = self.__get_row_col_from_block_cell(block_cell)
            text = self.__get_text_from_block_cell(block_cell)
            table[row][col] = text

        return table

    
    def __get_row_col_from_block_cell(self, block_cell):
        return block_cell.get('RowIndex', 0), block_cell.get('ColumnIndex', 0)


    def __get_text_from_block_cell(self, block_cell):
        block_word_ids = []
        relationships = block_cell.get('Relationships', [])
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
