import sqlite3
from itemadapter import ItemAdapter
from utils.validators import validate_item

class TechscoutPipeline:
    def __init__(self):
        self.conn = sqlite3.connect('techcrunch.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles
            (title TEXT, link TEXT, description TEXT)
        ''')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if validate_item(adapter.asdict()):
            self.cursor.execute('''
                INSERT OR IGNORE INTO articles (title, link, description)
                VALUES (?, ?, ?)
            ''', (adapter['title'], adapter['link'], adapter['description']))
            self.conn.commit()
        return item