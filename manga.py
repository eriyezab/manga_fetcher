class Manga:
    """ A class that will hold all information about a Manga.

    Attributes:
    name: The Manga's name.
    url: The link to mangafreak that will let me download it.
    latest_chapter: The latest chapter that has been released.
    """
    name: str
    url: str
    latest_chapter: int

    def __init__(self, name: str, url: str) -> int:
        """Initaialize the manga with the name of the manga as name and 
        the link to the mangafreak page for the manga as url. Scrape the website
        and set the latest chapter to latest chapter and return the number of the
        latest chapter.
        """
        self.name = name
        self.url = url
