import csv


class CsvBuilder():
    def __init__(self, table_csv_lines, form_csv_lines, line_csv_lines):
        self.table_csv_lines = table_csv_lines
        self.form_csv_lines = form_csv_lines
        self.line_csv_lines = line_csv_lines


    def save_csv_to_local(self):
        if self.table_csv_lines is not None:
            with open('./tmp/table.csv', 'w') as f:
                for line in self.table_csv_lines:
                    f.write(line)
                f.close()

        if self.form_csv_lines is not None:
            with open('./tmp/form.csv', 'w', newline='') as f:
                for line in self.form_csv_lines:
                    f.write(line)
                f.close()

        if self.line_csv_lines is not None:
            with open('./tmp/line.csv', 'w', newline='') as f:
                for line in self.line_csv_lines:
                    f.write(line)
                f.close()


    def save_csv_to_s3(self, s3_resource, bucket_name, file_name):
        if self.table_csv_lines is not None:
            with open('/tmp/table.csv', 'w') as f:
                for line in self.table_csv_lines:
                    f.write(line)
                f.close()
                table_csv_filename = 'data_table/{0}.csv'.format(file_name)
                s3_resource.Bucket(bucket_name).upload_file('/tmp/table.csv', table_csv_filename)

        if self.form_csv_lines is not None:
            with open('/tmp/form.csv', 'w') as f:
                for line in self.form_csv_lines:
                    f.write(line)
                f.close()
                form_csv_filename = 'data_form/{0}.csv'.format(file_name)
                s3_resource.Bucket(bucket_name).upload_file('/tmp/form.csv', form_csv_filename)

        if self.line_csv_lines is not None:
            with open('/tmp/line.csv', 'w') as f:
                for line in self.line_csv_lines:
                    f.write(line)
                f.close()
                line_csv_filename = 'data_line/{0}.csv'.format(file_name)
                s3_resource.Bucket(bucket_name).upload_file('/tmp/line.csv', line_csv_filename)
