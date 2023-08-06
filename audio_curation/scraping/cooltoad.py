import json
import time
import logging
import os
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (InvalidArgumentException,
                                        JavascriptException,
                                        WebDriverException,
                                        NoSuchCookieException,
                                        NoSuchElementException, TimeoutException)

from curation_utils import scraping

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s:%(asctime)s:%(module)s:%(lineno)d %(message)s")

configuration = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local_config.json'), 'r') as handle:
  configuration = json.load(handle)

site_configuration = configuration['cooltoad']


def get_logged_in_browser(headless=True):
  browser = scraping.get_selenium_chrome(headless=headless)
  browser.get("https://cooltoad.com/")
  username = browser.find_element_by_name("username")
  username.send_keys(site_configuration["user"])
  browser.find_element_by_name("password").send_keys(site_configuration["pass"])
  browser.find_element_by_css_selector("input.smallLeftButton").click()
  return browser


def get_song(browser, url, download_time=6):
  for i in range(0, 3):
    browser.get(url)
    try:
      WebDriverWait(browser, 20).until(presence_of_element_located((By.CSS_SELECTOR, "#bbContent")))
      break
    except TimeoutException:
      continue
  song_details = browser.find_element_by_css_selector("#bbContent").get_attribute('innerText')
  logging.info(f"From {url}: \n{song_details}")
  try:
    download_button = browser.find_element_by_css_selector("img.dlButton")
    download_button.click()
    time.sleep(download_time)
  except NoSuchElementException:
    logging.warning("Could not download this!")


def get_all(start_url, start_item_url=None, browser=None, download_time=5):
  if browser is None:
    browser = get_logged_in_browser(headless=False)
  browser.get(start_url)
  song_anchors_box = WebDriverWait(browser, 20).until(
    presence_of_element_located((By.CSS_SELECTOR, "#songsBox"))
  )
  song_anchors = browser.find_elements(by=By.CSS_SELECTOR, value="#songsBox a")
  urls = [urljoin("https://cooltoad.com/", song_anchor.get_attribute("href")) for song_anchor in song_anchors]
  logging.info(f"{len(urls)} urls in {start_url}")
  
  # We get the next url before navigating away to individual songs.
  try:
    next_page_link = browser.find_element_by_link_text(">")
    next_url = next_page_link.get_attribute("href")
  except NoSuchElementException:
    next_url = None
    logging.info("No further pages.")

  if start_item_url is not None and start_item_url in urls:
    from itertools import dropwhile
    urls = list(dropwhile(lambda x: x!=start_item_url, urls))
  logging.info(f"Getting {len(urls)} urls in {start_url}")
  for url in urls:
    get_song(browser=browser, url=url, download_time=download_time)
  if next_url is not None:
    get_all(start_url=next_url, browser=browser)
  else:
    input("Check if all downloads are done. Press key to close browser")

