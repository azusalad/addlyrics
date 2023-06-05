from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with
import time
import logging

def musixmatch(driver, artist, title):
    """Muxixmatch script.  Searches https://www.musixmatch.com.  Should use vpn since this site likes to ban you"""
    # load search page and click on first result
    logging.info("Running musixmatch")
    driver.get('https://www.musixmatch.com/search/' + str(artist) + '%20' + str(title) + '/tracks')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-results')))
    time.sleep(2)
    if not driver.find_elements(By.CLASS_NAME, "media-card-title"):
        logging.info('Unable to find lyrics on musixmatch')
        return False
    else:
        driver.find_element(By.CLASS_NAME, "media-card-title").click()

        # find lyrics on song page.  check if lyrics are restricted first
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mxm-track-title')))
        if driver.find_elements(By.CLASS_NAME, "mxm-lyrics-not-available"):
            logging.info('Unable to find lyrics on musixmatch')
            return False
        else:
            try:
                # this only gets the actual lyrics between the "tranlated into..." and "report a problem"
                lyrics = driver.find_element(By.CLASS_NAME, 'mxm-lyrics').text.split('\nReport a problem')[0].split(' languages\n')[1]
            except:
                # if there is only 1 language
                lyrics = '\n'.join(x for x in driver.find_element(By.CLASS_NAME, 'mxm-lyrics').text.split('\nReport a problem')[0].split('\n')[1:])
            time.sleep(5)
            return lyrics
