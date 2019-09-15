import os
from zipfile import ZipFile
import cfscrape  # this module allows me to bypass the cloudfare anti bot page
from bs4 import BeautifulSoup



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
    latest_chapter: str
    folder: str

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
        self.latest_chapter = self.latest_chapter_url.split('/')[-1]
        self.folder = os.getcwd() + '/manga/' + self.name + '/'

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
        download it into the folder dedicated to the manga. After downloading it,
        unpack the zip file.
        """
        if self.retrieve_latest_chapter_url() == self.latest_chapter_url:
            return False

        self.latest_chapter_url = self.retrieve_latest_chapter_url()
        file_path = self.folder + self.latest_chapter + '.zip'
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        scraper = cfscrape.create_scraper()
        chapter = scraper.get(self.latest_chapter_url)
        open(file_path, 'wb').write(chapter.content)
        current_path = os.getcwd()
        os.chdir(self.folder)
        with ZipFile(file_path, 'r') as zip_obj:
            zip_obj.extractall()
        os.chdir(current_path)
        print(f'There was a new release for {self.name}. Retrieved {self.latest_chapter}')
        return True

    def __str__(self) -> str:
        """ The string representation of the Manga class.
        """
        return self.name



# if __name__ == '__main__':
#     NARUTO = Manga('Naruto', "https://w10.mangafreak.net/Manga/Naruto",
#                    "http://images.mangafreak.net:8080/download/Naruto_699")
#     print(NARUTO.check_new_release())
