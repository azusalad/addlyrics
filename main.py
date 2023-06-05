import eyed3
import os
import sys
import time
import logging
from selenium import webdriver
from tqdm import tqdm

from config import *
sys.path.insert(0, 'utils')
from musixmatch import musixmatch
from animelyrics import animelyrics
from vocaloidlyrics import vocaloidlyrics
from genius import genius
from note import note

def create_driver():
    driver = webdriver.Firefox(executable_path=driver_path)
    if ublock_path:
        driver.install_addon(os.path.join(os.getcwd(), ublock_path), temporary=True)
    return driver

def get_info(song):
    """Get song title, artist and if lyrics exist.  Returns (title, artist, lyrics_exist)"""
    audiofile = eyed3.load(os.path.join(music_dir, song))
    title = audiofile.tag.title
    artist = audiofile.tag.artist
    try:
        audiofile.tag.lyrics[0].text
    except:
        lyrics_exist = False
    else:
        if audiofile.tag.lyrics[0].text == "":
            lyrics_exist = False
        else:
            lyrics_exist = True
    return (title, artist, lyrics_exist)

def write_lyrics(song, lyrics):
    """Write lyrics to file"""
    audiofile = eyed3.load(os.path.join(music_dir,song))
    audiofile.tag.lyrics.set(lyrics)
    audiofile.tag.save()
    logging.info("Lyrics written")
    return

def interactive(driver, artist, title, func):
    """Fetches lyrics for interactive mode.  Will call function to write lyrics if lyrics found.  Returns true if lyrics written and false if not"""
    func_name = str(func).split(' ')[1]
    logging.info("Doing" + str(artist) + ' ' + str(title) + " with " + str(func_name))
    if input('Search ' + str(func_name) + '? [y/n]').lower() == 'y':
        logging.debug("Search requested with " + str(func_name))
        lyrics = func(driver, artist, title)
        if lyrics:
            print('Lyrics found:\n' + str(lyrics))
            logging.info("Lyrics found")
            if input('Write lyrics?  [y/n]').lower() == 'y':
                logging.info("Writing lyrics")
                write_lyrics(song, lyrics)
                return True
        else:
            print("Lyrics not found or artist in blacklist/not in whitelist")
            return False
    logging.debug("Search skipped")
    return False

def normal_search(driver, artist, title, func):
    lyrics = func(driver, artist, title)
    if lyrics:
        write_lyrics(song, lyrics)
        return True
    else:
        return False


logging.basicConfig(filename='myapp.log', level=logging.INFO)
logging.info("Starting program at " + str(time.time()))

driver = create_driver()
with open('ignorelist.txt','r') as f:
    ignore_list = [x.strip() for x in f.readlines()]
music_list = [y for y in [x for x in os.listdir(music_dir) if '.mp3' in x] if y not in ignore_list]

# interactive mode.  asks for searching on every website and ask to write
if interactive_mode:
    logging.info("Starting interactive mode")
    for song in music_list:
        written = False
        index = 0
        title, artist, lyrics_exist = get_info(song)
        if overwrite_existing or not lyrics_exist:
            print('\n' + str(artist) + ' ' + str(title))
            while not written and index + 1 <= len(search_order):
                written = interactive(driver, artist, title, search_order[index])
                index += 1
            if not written:
                logging.warning("No lyrics found for " + str(artist) + ' ' + str(title))
                with open("notfound.txt","a") as f:
                    f.write("\n" + str(song))
else:
    for song in tqdm(music_list):
        written = False
        index = 0
        title, artist, lyrics_exist = get_info(song)
        if overwrite_existing or not lyrics_exist:
            # run website scripts
            logging.info('\nDoing ' + str(artist) + ' ' + str(title))
            while not written and index + 1 <= len(search_order):
                written = normal_search(driver, artist, title, search_order[index])
                index += 1
            if not written:
                logging.warning("No lyrics found for " + str(artist) + ' ' + str(title))
                with open("notfound.txt","a") as f:
                    f.write("\n" + str(song))
            time.sleep(5)
driver.close()
