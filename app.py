import os
import sys
import shutil
import csv
import smtplib
from email.message import EmailMessage
import imghdr
from manga import Manga


EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def start(manga_csv: str, contact_csv: str) -> list:
    """This function is to be run at the start of the execution. It will retrieve information from
    the csv file and create the Manga instances with that information and return them in a list.
    """
    with open(manga_csv, 'r') as csv_file1:
        csv_reader = csv.DictReader(csv_file1)
        list_of_mangas = []

        for line1 in csv_reader:
            new_manga = Manga(line1['name'], line1['url'], line1['latest_chapter_url'])
            list_of_mangas.append(new_manga)

    # read the recipient information from contact_csv and store it into a dictionary
    # with the recipients email as the key
    contact_dict = {}
    with open(contact_csv, 'r') as contacts:
        csv_reader = csv.DictReader(contacts)
        for contact in csv_reader:
            contact_dict[contact['email']] = {
                'email': contact['email'], 'first_name': contact['firstname'], 'last_name': contact['lastname']}
                
    return list_of_mangas, contact_dict

def send_email(person: dict, manga: Manga) -> None:
    """ This function takes a person({email: (firstname, lastname)}) and the manga that had a new release and
    sends the person the manga chapter.
    """
    receiver = person['email']
    msg = EmailMessage()
    msg['Subject'] = manga.latest_chapter
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver

    pages = [(int(i.split('_')[-1].split('.')[0]), i) for i in os.listdir(manga.folder) if os.path.isfile(os.path.join(manga.folder, i)) and '.jpg' in i]
    pages.sort(key=lambda tup: tup[0])
    
    msg.set_content(manga.latest_chapter + ' attached')
    for page in pages:
        with open(os.path.join(manga.folder, page[1]), 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name

        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=os.path.basename(file_name))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f'Sent email to {receiver} containing {manga.latest_chapter}.')


def refresh(mangas: list, data: str) -> None:
    """ Goes through every directory in './manga/' and deletes all the files.
    This gets rid of all zip files and image files of any manga chapter. It then
    writes the values of the new latest_chapter_url's to the csv file"""
    # clear all the mangas that were downloaded in the manga folder
    folder = os.path.join(sys.path[0], 'manga/')
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    # update data.csv for the new chapter urls
    with open(os.path.join(sys.path[0], data), 'w') as f:
        fieldnames = ['name', 'url', 'latest_chapter_url']

        csv_writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",")

        csv_writer.writeheader()
        for manga in mangas:
            csv_writer.writerow({fieldnames[0]: manga.name, fieldnames[1]: manga.url, fieldnames[2]: manga.latest_chapter_url})

if __name__ == "__main__":
    CURRENT_PATH = sys.path[0]
    # on the first run of the program, the manga folder needs to be created
    if not os.path.exists(os.path.join(CURRENT_PATH, 'manga/')):
        os.mkdir(os.path.join(CURRENT_PATH, 'manga/'))

    MANGA_INFO = 'data.csv'
    CONTACT_INFO = 'email_list.csv'
    
    # read the manga information stored in the csv file MANGA_INFO and the contact information in CONTACT_INFO 
    # and store the information returned into variables
    MANGAS, RECIPIENTS = start(os.path.join(
        CURRENT_PATH, MANGA_INFO), os.path.join(
        CURRENT_PATH, CONTACT_INFO))
    
    # find out whether any of the mangas have a new release and store the ones that do into
    # a list
    NEW_RELEASES = []
    for anime in MANGAS:
        if anime.check_new_release():
            NEW_RELEASES.append(anime)

    # loop through the recipients and send all new releases to each one
    for recipient in RECIPIENTS:
        if NEW_RELEASES == []:
            print('No new chapters have been released.')
            break
        for new_release in NEW_RELEASES:
            send_email(RECIPIENTS[recipient], new_release)
        
    # update 'data.cs' so that it contains the new chapters that were released if any
    # and then delete everything inside the manga folder
    refresh(MANGAS, MANGA_INFO)
