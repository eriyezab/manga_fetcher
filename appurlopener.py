import urllib.request


class AppURLopener(urllib.request.FancyURLopener):
    """This class is needed because urllib.request is blocked by the website so
    I can't download the manga.
    """
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"
