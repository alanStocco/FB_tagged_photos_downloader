## LINK GIT  https://gist.github.com/david-crespo/89baec40d680a17ebc2a4d622c5fc0cf
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

FB_USER_ID = '' # SET ME

# on mac, probably /Users/<mac username>/Library/Application Support/Google/Chrome/Default
CHROME_PROFILE_PATH = "/home/<user>/src/fb-tagged-script/chromedriver"

def get_driver():
    wd_options = Options()
    wd_options.add_argument("--disable-notifications")
    wd_options.add_argument("--disable-infobars")
    wd_options.add_argument("--mute-audio")
    wd_options.add_argument("--start-maximized")
    # wd_options.add_argument("--user-data-dir={}".format(CHROME_PROFILE_PATH))

    return webdriver.Chrome(chrome_options=wd_options)


def scroll_to_bottom(driver):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(1)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
