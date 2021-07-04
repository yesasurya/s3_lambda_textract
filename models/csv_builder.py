import csv


class CsvBuilder():
    def __init__(self, page_block, key_blocks):
        self.page_block = page_block
        self.key_blocks = key_blocks
        self.csv_content = {}

        page_block_children_ids = self.page_block.child_block_ids

        unsorted_csv_context = {}
        for _, key_block in self.key_blocks.items():
            line_block_id = key_block.child_blocks[0].line_block_id
            line_block_id_index = page_block_children_ids.index(line_block_id)

            key_text = key_block.get_text_from_children()
            value_text = ''
            for value_block in key_block.value_blocks:
                value_part = value_block.get_text_from_children()
                value_text = value_text + value_part
            
            unsorted_csv_context[line_block_id_index] = {
                key_text: value_text
            }

        sorted_indexes = sorted(unsorted_csv_context)
        for index in sorted_indexes:
            key_value_pair = unsorted_csv_context[index]
            self.csv_content.update(key_value_pair)

    def save_csv_to_local(self):
        pass

    @staticmethod
    def save_csv_to_s3(csv_content, s3_client, bucket_name, file_name):
        temp_csv_file = csv.writer(open("/tmp/csv_file.csv", "w+"))
        temp_csv_file.writerow(["KEY", "VALUE"])
        for key, value in csv_content.items():
            temp_csv_file.writerow([key, value])
        
        s3_client.upload_file('/tmp/csv_file.csv', bucket_name, file_name)
