import os
import requests
import json
from dynamodb_json import json_util


def lambda_handler(event, context):
    print("Event:", event)

    webhook_url = os.getenv('DISCORD_WEBHOOK')

    records = event.get("Records")
    ok = True
    for record in records:
        if record.get("eventName") == "INSERT":
            post = record.get("dynamodb").get("NewImage")
            post = json_util.loads(post)
            params = {
                "content": "<@770781335307419718>\n**{title}**\n\n*Escrito por {authors}*\nLeia o texto completo: {link}".format(
                    title=post.get("title"), authors=", ".join(post.get("authors")), link=post.get("link"))
            }

            print("Params:", params)
            r = requests.post(webhook_url, data=params)

    return {
        'statusCode': 200,
        'body': json.dumps(records)
    }
