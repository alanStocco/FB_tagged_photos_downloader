import json, re, time
from selenium.webdriver.common.by import By

from datetime import datetime, timezone
from subprocess import call

from helpers import scroll_to_bottom, get_driver, FB_USER_ID

# you will likely need to update this to something that selects 
# for the container around the photo info, timestamp, album, etc
CONTAINER_SELECTOR = ".atb"


def get_fb_id(link):
    match = re.search("fbid=([0-9]+)", link)
    if match:
        return match.group(1)
    
    return "fake_id_" + str(hash(link))

if __name__ == '__main__':
    print("-"*20 + "\nOpening Browser...")

    driver = get_driver()
    driver.get("https://m.facebook.com/{}/photos".format(FB_USER_ID))
    scroll_to_bottom(driver)
    time.sleep(15)
    photo_links = list(map(
        lambda el: el.get_attribute("href"),
        driver.find_elements(By.CSS_SELECTOR, ('.timeline.photos a'))
    ))

    pretty = dict(sort_keys=True, indent=4, separators=(',', ': '))

    photos = []
    for link in photo_links:
        driver.get(link)

        photo_id = get_fb_id(link)
        time.sleep(1)
        #full_size_url = driver.find_element(By.NAME,("View Full Size")).get_attribute("href")
        xpath = "//a[@class='sec' and text()='View full size']"
        full_size_url = driver.find_element(By.XPATH,xpath).get_attribute("href")
        time.sleep(1)
        actor = driver.find_element(By.CSS_SELECTOR, ('.actor')).text
        time.sleep(1)
        tag_elements = driver.find_elements(By.CSS_SELECTOR, '.tagName')
        people = [el.text for el in tag_elements]
        # people = list(map(
        #     lambda el: el.text,
        #     driver.find_element(By.CSS_SELECTOR, ('.tagName'))
        # ))
        time.sleep(1)
        caption = driver.find_element(By.CSS_SELECTOR, ('.msg > div')).text
        time.sleep(1)
        timestamp_json = driver.find_element(By.CSS_SELECTOR, ('{} abbr'.format(CONTAINER_SELECTOR))).get_attribute('data-store')
        time.sleep(2)
        timestamp = json.loads(timestamp_json).get("time")
        info = driver.find_element(By.CSS_SELECTOR, ('{} > div'.format(CONTAINER_SELECTOR))).text.replace('\u00b7', '-').rstrip(' -')
        date = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d")
        filename = "{}_{}.jpg".format(date, photo_id)
        
        driver.get(full_size_url)
        photo = {
            "fb_url": link,
            "cdn_url": driver.current_url,
            "actor": actor,
            "caption": caption,
            "timestamp": timestamp,
            "info": info,
            "filename": filename,
            "people": people
        }
        print(json.dumps(photo, **pretty))
        photos.append(photo)

        with open('photos/data.json', 'w') as f:
            f.write(
                json.dumps(photos, **pretty)
            )

        call(["curl", driver.current_url, "--output", "photos/{}".format(filename)])