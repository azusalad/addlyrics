from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with

import time

def note(driver, artist, title):
    """Searches https://note.com"""

    whitelist = ["Nyarons"]

    if artist in whitelist:
        # load search page and click on first result
        driver.get("https://note.com/search?q=" + str(artist) + "+" + str(title) + "&context=note&mode=search")
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.o-searchResultNote__nav')))
            driver.find_element(By.CLASS_NAME, "m-timelineItemWrapper__itemWrapper").click()
        except:
            print("Note was unable to find lyrics")
            return False
        # get lyrics
        time.sleep(3)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.o-noteContentHeader__title')))
        lyrics = driver.find_element(By.CLASS_NAME, "note-common-styles__textnote-body").text
        return lyrics
    else:
        print("Artist is not in the whitelist for note")
        return False
