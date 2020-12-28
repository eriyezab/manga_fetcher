import os
import sys
from zipfile import ZipFile
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests


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
        # set up the webdriver for scraping
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        # options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        self.name = name
        self.url = url
        if latest_chapter_url == '':
            self.latest_chapter_url = self.retrieve_latest_chapter_url()
        else:
            self.latest_chapter_url = latest_chapter_url
        self.latest_chapter = self.latest_chapter_url.split('/')[-1]
        self.folder = os.path.join(sys.path[0], 'manga/' + self.name + '/')

    def retrieve_latest_chapter_url(self) -> str:
        """retrieve the latest chapter url number from the website
        """
        self.driver.get(self.url)
        time.sleep(10)
        website = self.driver.page_source
        soup = BeautifulSoup(website, 'lxml')
        chapter = soup.find_all('tr')[-1].find_all('a')[-1].get('href')
        self.driver.quit()
        return chapter

    def check_new_release(self) -> bool:
        """Check whether there was a new release or not. If there was then
        download it into the folder dedicated to the manga. After downloading it,
        unpack the zip file.
        """
        if self.retrieve_latest_chapter_url() == self.latest_chapter_url:
            return False

        self.latest_chapter_url = self.retrieve_latest_chapter_url()
        self.latest_chapter = self.latest_chapter_url.split('/')[-1]
        file_path = self.folder + self.latest_chapter + '.zip'
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        chapter = requests.get(self.latest_chapter_url)
        open(file_path, 'wb').write(chapter.content)
        current_path = sys.path[0]
        os.chdir(self.folder)
        with ZipFile(file_path, 'r') as zip_obj:
            zip_obj.extractall()
        os.chdir(current_path)
        print(f'There was a new release for {self}. Retrieved {self.latest_chapter}')
        return True

    def __str__(self) -> str:
        """ The string representation of the Manga class.
        """
        return ' '.join(self.name.split('_'))



# if __name__ == '__main__':
#     NARUTO = Manga('Naruto', "https://w10.mangafreak.net/Manga/Naruto",
#                    "http://images.mangafreak.net:8080/download/Naruto_699")
#     print(NARUTO.check_new_release())
