from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with
import time

def musixmatch(driver, artist, title):
    """Muxixmatch script.  Should use vpn since this site likes to ban you"""
    # load search page and click on first result
    driver.get('https://www.musixmatch.com/search/' + str(artist) + '%20' + str(title) + '/tracks')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-results')))
    time.sleep(1)
    if not driver.find_elements(By.CLASS_NAME, "media-card-title"):
        print('Unable to find lyrics on musixmatch')
        return False
    else:
        driver.find_element(By.CLASS_NAME, "media-card-title").click()

        # find lyrics on song page.  check if lyrics are restricted first
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mxm-track-title')))
        if driver.find_elements(By.CLASS_NAME, "mxm-lyrics-not-available"):
            print('Unable to find lyrics on musixmatch')
            return False
        else:
            lyrics = driver.find_element(By.CLASS_NAME, 'mxm-lyrics').text.split('\nReport a problem')[0].split(' languages\n')[1]
            return lyrics
