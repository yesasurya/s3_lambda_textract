from models.parser import Parser


class LineParser(Parser):
    def __init__(self, textract_response):
        super().__init__(textract_response)
        block_lines = self.dict_block_by_types.get('LINE', [])
        self.line_texts = []
        for block_line in block_lines:
            self.line_texts.append(block_line.get('Text', ''))
        
    
    def get_csv_lines(self):
        csv_lines = []
        for text in self.line_texts:
            csv_line = text + '\n'
            csv_lines.append(csv_line)
        return csv_lines
