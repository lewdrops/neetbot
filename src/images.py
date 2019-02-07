import json
import random
from datetime import datetime

random.seed(datetime.now)

from google_images_download import google_images_download
response = google_images_download.googleimagesdownload()  # class instantiation


async def image_link_of(keyword, limit=100):
    try:
        arguments = {"keywords": keyword,
                     "limit": limit,
                     "safe_search": True,
                     # "print_urls": True,
                     "extract_metadata": True,
                     "no_download": True}

        paths = response.download(arguments=arguments)
        # print(paths)
        log_path = f"./logs/{keyword}.json"
        with open(log_path) as f:
            data = json.load(f)
            # print(data)
            link = data[random.randint(0, limit - 1)]["image_link"]
            while not link[-3:] in ["jpg", "png", "gif", "tif"]:  # todo: valid image links that don't have img extensions?
                link = data[random.randint(0, limit - 1)]["image_link"]
                print("bad image")
            return link
    except Exception as e:
        print("error", e)
        return


async def word_cloud_of(client, channel):
    logs = client.logs_from(channel)
    print(logs)

