# todo: combine / simplify logic in gif & pic
# todo: check to see if gif actually moves
import json
import random
from datetime import datetime

import discord
from discord.ext import commands
from google_images_download import google_images_download

# setup
response = google_images_download.googleimagesdownload()  # class instantiation
random.seed(datetime.now)


async def image_link_of(keyword, format=None, limit=25):
    try:
        arguments = {"keywords": keyword,
                     "limit": limit,
                     "safe_search": True,
                     # "print_urls": True,
                     "extract_metadata": True,
                     "no_download": True}

        if format:
            arguments["format"] = format

        paths = response.download(arguments=arguments)
        # print(paths)
        log_path = f"./logs/{keyword}.json"
        with open(log_path) as f:
            data = json.load(f)
            # print(data)
            link = data[random.randint(0, limit - 1)]["image_link"]
            while not link[-3:] in ["jpg", "png", "gif", "tif"]:  # todo: valid image links that don't have img extensions?
                link = random.choice(data)["image_link"]
                print("bad image")
            return link
    except Exception as e:
        print("error", e)
        return


async def word_cloud_of(client, channel):
    logs = client.logs_from(channel)
    print(logs)


class ImagesCog:
    """testing cogs"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["picture", "pic-of"])
    async def pic(self, ctx, *keywords):
        """embed a pic from google images for the keyword"""

        e = discord.Embed()
        e.set_image(url=await image_link_of(' '.join(keywords)))
        await ctx.send(embed=e)

    @commands.command(aliases=["gif-of"])
    async def gif(self, ctx, *keywords):
        """embed a gif from google images for the keyword"""

        e = discord.Embed()
        e.set_image(url=await image_link_of(' '.join(keywords), format="gif"))
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(ImagesCog(bot))
