import eyed3
import os
import sys
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with

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
    print("Lyrics written")
    return

driver = create_driver()
with open('ignorelist.txt','r') as f:
    ignore_list = [x.strip() for x in f.readlines()]
music_list = [y for y in [x for x in os.listdir(music_dir) if '.mp3' in x] if y not in ignore_list]

# interactive mode.  asks for searching on every website and ask to write
if interactive_mode:
    for song in music_list:
        written = False
        title, artist, lyrics_exist = get_info(song)
        if overwrite_existing or not lyrics_exist:
            # run website scripts
            print('\n' + str(artist) + ' ' + str(title))
            if input('Search musixmatch?  [y/n]') == 'y':
                lyrics = musixmatch(driver, artist, title)
                if lyrics:
                    print('Lyrics found:\n' + str(lyrics))
                    if input('Overwrite?  [y/n]') == 'y':
                        write_lyrics(song, lyrics)
                        written = True

            if not written:
                if input('Search anime?  [y/n]') == 'y':
                    lyrics = animelyrics(driver, artist, title)
                    if lyrics:
                        print('Lyrics found:\n' + str(lyrics))
                        if input('Overwrite?  [y/n]') == 'y':
                            write_lyrics(song, lyrics)
                            written = True

                if not written:
                    if input('Search vocaloid?  [y/n]') == 'y':
                        lyrics = vocaloidlyrics(driver, artist, title)
                        if lyrics:
                            print('Lyrics found:\n' + str(lyrics))
                            if input('Overwrite?  [y/n]') == 'y':
                                write_lyrics(song, lyrics)
                                written = True

                    if not written:
                        if input('Search genius?  [y/n]') == 'y':
                            lyrics = genius(driver, artist, title)
                            if lyrics:
                                print('Lyrics found:\n' + str(lyrics))
                                if input('Overwrite?  [y/n]') == 'y':
                                    write_lyrics(song, lyrics)
                                    written = True

                        if not written:
                            if input('Search note?  [y/n]') == 'y':
                                lyrics = note(driver, artist, title)
                                if lyrics:
                                    print('Lyrics found:\n' + str(lyrics))
                                    if input('Overwrite?  [y/n]') == 'y':
                                        write_lyrics(song, lyrics)

else:
    for song in music_list:
        title, artist, lyrics_exist = get_info(song)
        if overwrite_existing or not lyrics_exist:
            # run website scripts
            print('\n' + str(artist) + ' ' + str(title))

            lyrics = musixmatch(driver, artist, title)
            if lyrics:
                write_lyrics(song, lyrics)
            else:

                lyrics = animelyrics(driver, artist, title)
                if lyrics:
                    write_lyrics(song, lyrics)
                else:

                    lyrics = vocaloidlyrics(driver, artist, title)
                    if lyrics:
                        write_lyrics(song, lyrics)
                    else:

                        lyrics = genius(driver, artist, title)
                        if lyrics:
                            write_lyrics(song,lyrics)
                        else:

                            lyrics = note(driver,artist,title)
                            if lyrics:
                                write_lyrics(song,lyrics)
            time.sleep(5)

driver.close()
