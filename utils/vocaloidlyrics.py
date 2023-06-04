from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.relative_locator import locate_with

def vocaloidlyrics(driver, artist, title):
    """Search https://vocaloidlyrics.fandom.com"""
    # first load search page and click first item
    driver.get("https://vocaloidlyrics.fandom.com/wiki/Special:Search?query=" + str(artist) + "+" + str(title) + "&scope=internal&navigationSearch=true")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#firstHeading')))
    try:
        driver.find_element(By.CLASS_NAME, "unified-search__result__title").click()
    except:
        print('Unable to find lyrics on vocaloid lyrics')
        return False
    # fetch lyrics.  it is a table.  https://stackoverflow.com/questions/37090653/iterating-through-table-rows-in-selenium-python
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#firstHeading')))
    try:
        table = driver.find_element(locate_with(By.TAG_NAME, "table").below({By.ID: "Lyrics"}))
    except:
        print('Unable to find lyrics on vocaloid lyrics')
        return False
    original = []
    roumaji = []
    translated = []
    for row in table.find_elements(By.CSS_SELECTOR,'tr'):
        column = 0
        for cell in row.find_elements(By.TAG_NAME,'td'):
            if column == 0:
                if len(original) == 0:
                    original.append(str(cell.text))
                else:
                    original.append("\n" + str(cell.text))
            elif column == 1:
                if len(roumaji) == 0:
                    roumaji.append(str(cell.text))
                else:
                    roumaji.append("\n" + str(cell.text))
            elif column == 2:
                if len(translated) == 0:
                    translated.append(str(cell.text))
                else:
                    translated.append("\n" + str(cell.text))
            column += 1
    # Am choosing to add original lyrics first then translated lyrics after.  You can change to what you want
    lyrics = original + ['\n'] + translated
    return ''.join(str(x) for x in lyrics)
