import schema

article_schema = schema.Schema({
    'title': str,
    'link': str,
    'description': str
})

def validate_item(item):
    return article_schema.is_valid(item)