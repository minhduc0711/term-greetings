import scrapy
import os
import json
import re

data_dir = "../data"

headers = {'content-type': 'application/json'}
body = {
    "typ": "topic",
    "langc": "en",
    "v": "9.5.1:3437908",
    "ab": "a",
    "pg": 2,
    "id": "t:132672",
    "vid": "4f9596ef2d009a670f2088e4266c8e25",
    "fdd": "d",
    "m": 0
}
reversed_topic = {
    ('t:132672', '4f9596ef2d009a670f2088e4266c8e25'): 'morning',
    ('t:132618', 'cce3d71d4c26da61c7112dcfeb63cccc'): 'inspirational',
    ('t:132622', '7b363d749b4c7c684ace871c8a75f8e6'): 'motivational',
    ('t:132635', '8a8f8168ab0a593b60788deaca4a144b'): 'happiness',
    ('t:132659', '79c908c909d16b9b23b3ee012bb6a0a8'): 'moving_on',
    ('t:132671', '5b5cfcffaba42f2426bc04d3bcb69897'): 'thankful',
    ('t:132594', '72641a52a49f9cc6e5a6b1ae11a66e0b'): 'science'
}


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        for (id, vid) in reversed_topic:
            for pg in range(1, 26):
                body["pg"] = pg
                body["id"] = id
                body["vid"] = vid
                yield scrapy.FormRequest(url="https://www.brainyquote.com/api/inf",
                                         method='POST',
                                         body=json.dumps(body),
                                         headers=headers)

    def parse(self, response):
        # Get rid of escape characters
        cleaned_html = re.sub("\r*\n*\t*", "",
                              json.loads(response.body)["content"])
        cleaned_html = re.sub("\'", "'", cleaned_html)
        cleaned_html = re.sub('\"', '"', cleaned_html)
        response = response.replace(body=cleaned_html)

        # Extract data
        quotes = response.css(".b-qt::text").getall()
        authors = response.css(".bq-aut::text").getall()
        filenames = []
        for classes in response.css(".b-qt::attr(class)").extract():
            for c in classes.split():
                if str.startswith(c, "qt"):
                    filenames.append(c)

        # Identify the current topic
        req_body = json.loads(response.request.body)
        topic = reversed_topic[(req_body["id"],
                                req_body["vid"])]
        topic_dir = os.path.join(data_dir, topic)
        print(topic_dir)
        if not os.path.exists(topic_dir):
            os.makedirs(topic_dir)

        # Save crawled data to textfiles
        for quote, author, filename in zip(quotes, authors, filenames):
            file_path = os.path.join(topic_dir, filename + ".txt")
            with open(file_path, "w+") as f:
                f.write(quote + " - " + author)
