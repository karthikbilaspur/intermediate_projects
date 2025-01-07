import csv

class EmailPipeline:
    def __init__(self):
        self.file = open('emails.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.emails = set()

    def process_item(self, item, spider):
        email = item['email']
        if email not in self.emails:
            self.writer.writerow([email])
            self.emails.add(email)
        return item

    def close_spider(self, spider):
        self.file.close()