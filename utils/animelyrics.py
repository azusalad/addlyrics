from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with

import romkan
import time
import logging

def animelyrics(driver, artist, title):
    """Searches https://www.animelyrics.com/"""
    logging.info("Running animelyrics")

    blacklist = ["Nyarons", "ツユ", "K/DA"]

    if artist not in blacklist:
        # load search page and click on first item
        driver.get("https://cse.google.com/cse?cx=partner-pub-9427451883938449%3Agd93bg-c1sx&q=" + str(artist) + "%20" + str(title) + "#gsc.tab=0&gsc.q=" + str(artist) + "%20" + str(title) + "&gsc.page=1")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cse-hosted')))
        if driver.find_element(By.CSS_SELECTOR, "div.gs-webResult:nth-child(1)").text == "No Results":
            # no results so try to romanize the title
            title = romkan.to_roma(title)
            driver.get("https://cse.google.com/cse?cx=partner-pub-9427451883938449%3Agd93bg-c1sx&q=" + str(artist) + "%20" + str(title) + "#gsc.tab=0&gsc.q=" + str(artist) + "%20" + str(title) + "&gsc.page=1")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cse-hosted')))
            time.sleep(2)
            if driver.find_element(By.CSS_SELECTOR, "div.gs-webResult:nth-child(1)").text == "No Results":
                logging.info('Unable to find lyrics on animelyrics')
                return False

        results = driver.find_elements(By.CLASS_NAME, "gs-title")
        for x in results:
            if x.get_attribute('href'):
                driver.get(x.get_attribute('href').split('.htm')[0] + '.jis')
                break
        # get lyrics
        lyrics = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'kanji'))).text
        return lyrics
    else:
        logging.info("Artist is in the blacklist for animelyrics")
