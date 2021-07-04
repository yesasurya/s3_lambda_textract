import csv


class CsvBuilder():
    def __init__(self, table_csv_lines, form_csv_lines):
        self.table_csv_lines = table_csv_lines
        self.form_csv_lines = form_csv_lines


    def save_csv_to_local(self):
        with open('./tmp/table.csv', 'w') as f:
            for line in self.table_csv_lines:
                f.write(line)
            f.close()

        with open('./tmp/form.csv', 'w', newline='') as f:
            for line in self.form_csv_lines:
                f.write(line)
            f.close()


    def save_csv_to_s3(self, s3_resource, bucket_name, file_name):
        with open('/tmp/table.csv', 'w') as f:
            for line in self.table_csv_lines:
                f.write(line)
            f.close()

        with open('/tmp/form.csv', 'w') as f:
            for line in self.form_csv_lines:
                f.write(line)
            f.close()

        table_csv_filename = '{0}/table.csv'.format(file_name)
        form_csv_filename = '{0}/form.csv'.format(file_name)
        s3_resource.Bucket(bucket_name).upload_file('/tmp/table.csv', table_csv_filename)
        s3_resource.Bucket(bucket_name).upload_file('/tmp/form.csv', form_csv_filename)
