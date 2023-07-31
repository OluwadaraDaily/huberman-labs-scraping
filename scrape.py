import re
import time
import random
import warnings
import pandas as pd
import os, json
from typing import List
from lxml import etree as et
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

def scrape(url, file_name):
  # file_name = "output.json"


  # instantiate options 
  options = webdriver.ChromeOptions()

  # run browser in headless mode 
  options.add_argument('--headless')
  
  # instantiate driver 
  driver = webdriver.Chrome(service=ChromeService( 
    ChromeDriverManager().install()), options=options)

  # load website 
  # url = "https://steno.ai/huberman-lab/science-supported-tools-to-accelerate-your-fitness-goals"

  # get the entire website content
  driver.get(url)

  # Wait for the main content to be visible
  wait = WebDriverWait(driver, 5)
  wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'aside')))

  # Pseudocode
  """
  - Initialise the JSON object
  - Loop through divs with class 'group flex flex-col space-y-4'
  - For every div, click on the transcript button
  - Then, locate the inner divs with the text
  - Concatenate the text to form a sentence 
  - Add said sentence with its key (ID of the DIV) to the JSON object
  - Rinse and repeate (Actually, it's more of a for loop)
    
  """
  json_output = {
    "title": "",
    "url": "",
    "description": "",
    "date": "",
    "transcripts": {}
  }

  title = driver.find_element(By.XPATH, "//h1[@class='text-[15px] font-semibold leading-5 tracking-[0.37px] text-black']").get_attribute("innerHTML")

  about_div = driver.find_element(By.XPATH, "//div[@class='flex flex-col gap-y-3 text-[14px] leading-[19px] tracking-[0.44px]']")
  about_div_children = about_div.find_elements(By.XPATH, "*")
  description = about_div_children[-1].get_attribute("innerHTML")

  date = ""

  main_element = driver.find_element(By.XPATH, "//div[@class='mb-4 space-y-6 px-2 pt-4 md:px-6']")

  section_elements = main_element.find_elements(By.XPATH, "*")

  transcript_btn_count = 0

  json_output["title"] = title
  json_output["url"] = url
  json_output["description"] = description
  json_output["date"] = date

  for section in section_elements:
    id_value = section.get_attribute("id")
    print("\nID ->", id_value)

    nav_tabs_section = section.find_element(By.XPATH, "//nav[@class='-mb-px flex justify-between md:space-x-8 md:justify-normal']")
    
    transcript_button = nav_tabs_section.find_elements(By.XPATH, "//button[span[text()='Transcript']]")[transcript_btn_count]

    # Click on transcript button
    ActionChains(driver)\
      .click(transcript_button)\
      .perform()

    sentence = ""

    section_children = section.find_elements(By.XPATH, "*")
    section_without_play_button = section_children[1]

    section_without_play_button_children = section_without_play_button.find_elements(By.XPATH, "*")
    
    text_sections_with_play_btns = section_without_play_button_children[1:-1]

    for text_section_with_play_btn in text_sections_with_play_btns:
      text_section_with_play_btn_children = text_section_with_play_btn.find_elements(By.XPATH, "*")

      text_div = text_section_with_play_btn_children[1]

      text_div_children = text_div.find_elements(By.XPATH, "*")

      for text_div_child in text_div_children:
        text_div_child_children = text_div_child.find_elements(By.XPATH, "*")

        # text = text_paragraph.get_attribute("innerText")
        sentence += "".join(text.get_attribute("innerHTML") for text in text_div_child_children)
    json_output["transcripts"][id_value] = sentence.strip()
    transcript_btn_count += 1



  with open(file_name, "w") as file:
    file.write(json.dumps(json_output))

  driver.quit()