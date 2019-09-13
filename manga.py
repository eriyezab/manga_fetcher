import urllib.request
import cfscrape #this module allows me to bypass the cloudfare anti bot page
from bs4 import BeautifulSoup
from zipfile import ZipFile


class Manga:
    """ A class that will hold all information about a Manga.

    Attributes:
    name: The Manga's name.
    url: The link to mangafreak that will let me download it.
    latest_chapter_url: The link to the latest chapter that has been released.
    """
    name: str
    url: str
    latest_chapter_url: str

    def __init__(self, name: str, url: str, latest_chapter_url: str='') -> bool:
        """Initaialize the manga with the name of the manga as name and
        the link to the mangafreak page for the manga as url. Scrape the website
        and set the latest chapter to latest chapter and return the number of the
        latest chapter. This checks for valid url's
        """
        self.name = name
        self.url = url
        if latest_chapter_url == '':
            self.latest_chapter_url = self.retrieve_latest_chapter_url()
        else:
            self.latest_chapter_url = latest_chapter_url
            print('Incorrect Manga URL.')

    def retrieve_latest_chapter_url(self) -> str:
        """retrieve the latest chapter url number from the website
        """
        scraper = cfscrape.create_scraper()
        
        website = scraper.get(self.url).content
        soup = BeautifulSoup(website, 'lxml')
        chapter = soup.find_all('tr')[-1].find_all('a')[-1].get('href')
        return chapter
    
    def check_new_release(self) -> bool:
        """Check whether there was a new release or not. If there was then
        download it into the folder dedicated to the manga.
        """
        if self.retrieve_latest_chapter_url() == self.latest_chapter_url:
            return False
        else:
            self.latest_chapter_url = self.retrieve_latest_chapter_url()
            urllib.request.urlretrieve(self.latest_chapter_url, './manga/' + self.name)
            return True



if __name__ == '__main__':
    NARUTO = Manga('Naruto', "https://w10.mangafreak.net/Manga/Naruto")
    print(NARUTO.check_new_release())
