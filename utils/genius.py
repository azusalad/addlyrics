from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with

import time

def genius(driver, artist, title):
    """Searches https://genius.com for lyrics"""
    # search page
    driver.get("https://genius.com/search?q=" + str(artist) + "+" + str(title))
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search_results_page-header')))
    time.sleep(3)
    items = driver.find_elements(By.CLASS_NAME, "mini_card-title")
    for x in items:
        if x.text == title:
            x.click()
            break
    else:
        # if can't find an exact match just click the top result
        items[0].click()
        print("Genius could not find an exact title match, clicking best result")

    # get lyrics
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Lyrics__Container-sc-1ynbvzw-5:nth-child(2)')))
        time.sleep(2)
        lyrics = driver.find_elements(By.XPATH, "//div[contains(@class, 'Lyrics__Container-sc-1ynbvzw-5 Dzxov')]") # genius puts ads in the middle of their lyrics :/
        lyrics = ''.join([x.text for x in lyrics])
    except:
        print("Genius was unable to find lyrics")
        return False

    # the stuff below is just to remove the stuff in the [brackets] on the genius lyrics
    # you can just comment this stuff out if you like
    lyrics_list = []
    in_bracket = False
    for letter in lyrics:
        if letter == "[":
            in_bracket = True
        elif letter == "]":
            in_bracket = False
        else:
            if not in_bracket:
                lyrics_list.append(letter)
    lyrics = "".join(x for x in lyrics_list).strip()

    return lyrics
