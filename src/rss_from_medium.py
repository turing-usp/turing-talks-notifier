import os
import re
import json
import boto3
import feedparser
from time import mktime

def update_feed(feed):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('turing-talks')
    url = feed
    feed = feedparser.parse(url)

    for entry in feed.entries:
        entry_id = entry.get('id').split('/')[-1]
        title = entry.get('title')

        description = entry.get('summary')
        description = re.match('<h4>(.*?)</h4>', description)
        if description is not None:
            description = description[1]
            description = description.replace(r'\xa0', ' ')
        else:
            description = ''

        entry_link = entry.get('link')
        date = entry.get('published_parsed')
        date = round(mktime(date))
        authors = [author.get('name', None) for author in entry.get('authors', [])]
        tags = [tag.get('term', None) for tag in entry.get('tags', [])]

        table_item = {
            'id': entry_id,
            'title': title,
            'description': description,
            'link': entry_link,
            'date': date,
            'authors': authors,
            'tags': tags
        }
        print(table_item)
        table.put_item(Item=table_item)

def lambda_handler(event, context):
    feed = os.getenv('RSS_FEED')
    update_feed(feed)
    return {
        'statusCode': 200
    }
