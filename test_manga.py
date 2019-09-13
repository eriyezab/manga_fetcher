import unittest
from manga import Manga

# This file test the Manga class using the page for Naruto, as the Naruto manga is
# finished so Manga.retrieve_latest_chapter should always return the same integer,
# which is 700.

class TestManga(unittest.TestCase):
    """A class to test the methods of the Manga Module"""

    def test_retrieve_latest_chapter_url(self):
        """make sure that the method retrieves the correct url
        """
        NARUTO = Manga('Naruto', "https://w10.mangafreak.net/Manga/Naruto")
        chapter = int(NARUTO.retrieve_latest_chapter_url()[-3:])
        self.assertEqual(chapter, 700)

    def test_check_new_release(self):
        """make sure that the method returns false
        """
        NARUTO = Manga('Naruto', "https://w10.mangafreak.net/Manga/Naruto")
        self.assertFalse(NARUTO.check_new_release())


if __name__ == "__main__":
    unittest.main()
