from urllib.request import urlopen
from cachetools import cached
import json

@cached(cache={})
def daily_image_url(date):
    # not actually using the date
    # it just means the function won't used the cached result on a different day
    url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-AU"
    response = urlopen(url)
    data = response.read().decode("utf-8")
    jsonobj = json.loads(data)
    return "https://www.bing.com" + jsonobj["images"][0]["url"]
