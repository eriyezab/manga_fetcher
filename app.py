import os 
import shutil
import csv
from manga import Manga


# ONE_PIECE = "https://w10.mangafreak.net/Manga/One_Piece"
# BLACK_CLOVER = "https://w10.mangafreak.net/Manga/Black_Clover"
# ATTACK_ON_TITAN = "https://w10.mangafreak.net/Manga/Shingeki_No_Kyojin"
# ONE_PUNCH_MAN = "https://w10.mangafreak.net/Manga/Onepunch_Man"
# HUNTER_X_HUNTER = "https://w10.mangafreak.net/Manga/Hunter_X_Hunter"

EMAIL_ADDRESS = 'izer.buwembo@gmail.com'
EMAIL_PASSWORD = '12345678'

import smtplib
from email.message import EmailMessage
import imghdr

def start(data_file: str) -> list:
    """This function is to be run at the start of the execution. It will retrieve information from
    the csv file and create the Manga instances with that information and return them in a list.
    """
    with open(data_file, 'r') as csv_file1:
        csv_reader = csv.reader(csv_file1)
        next(csv_reader)
        list_of_mangas = []

        for line1 in csv_reader:
            new_manga = Manga(line1[0], line1[1], line1[2])
            list_of_mangas.append(new_manga)

        return list_of_mangas

def send_email(recipient: dict, manga: Manga) -> None:
    """ This function takes a recipient({email: (firstname, lastname)}) and the manga that had a new release and
    sends the recipient the manga chapter.
    """
    msg = EmailMessage()
    msg['Subject'] = manga.latest_chapter
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient['email']

    pages = [i for i in os.listdir(manga.folder) if os.path.isfile(os.path.join(manga.folder, i)) and '.jpg' in i]
    pages.sort()
    print(pages)
    # content = 
    # msg.set_content()
    # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    #     smtp.login(EMAIL_ADDRESS, PASSWORD)
    #     smtp.send_message(msg)


def refresh(mangas: list) -> None:
    """ Goes through every directory in './manga/' and deletes all the files.
    This gets rid of all zip files and image files of any manga chapter. It then 
    writes the values of the new latest_chapter_url's to the csv file"""
    folder = '/manga'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    MANGAS = start('data.csv')
    RECIPIENTS = {}
    with open('email_list.csv', 'r') as csv_file2:
        CSV_READER = csv.reader(csv_file2)
        next(CSV_READER)
        for line2 in CSV_READER:
            RECIPIENTS[line2[0]] = {'email' :line2[0], 'first_name' : line2[1], 'last_name': line2[2]}

    NEW_RELEASES = []
    for anime in MANGAS:
        if anime.check_new_release():
            NEW_RELEASES.append(anime)
    for recipient in RECIPIENTS:
        for new_release in NEW_RELEASES:
            send_email(RECIPIENTS[recipient], new_release)

    refresh(MANGAS)
            
    
