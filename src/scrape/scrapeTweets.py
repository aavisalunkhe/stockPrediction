import os, time, json, random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()  
USER  = os.getenv("TW_USER")
EMAIL = os.getenv("TW_EMAIL")
PASSW = os.getenv("TW_PASS")

USER = os.getenv("TW_USER")
EMAIL = os.getenv("TW_EMAIL")
PASSWD = os.getenv("TW_PASS")
opts= Options()
opts.add_argument("--headless")
opts.add_argument(f"--user-agent={random.choice([
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...'
])}")
service= Service(executable_path= "C:/path/to/chromedriver")
driver= webdriver.Chrome(service= service, options= opts)
wait= WebDriverWait(driver, 15)
driver.get("https://twitter.com/i/flow/login")
wait.until(EC.presence_of_element_located((By.NAME, "text"))).send_keys(USER)  # username
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))).click()
try:
    wait.until(EC.presence_of_element_located((By.NAME, "text"))).send_keys(EMAIL)  # email fallback
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))).click()
except:
    pass
wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(PASSWD)
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))).click()
driver.get("https://twitter.com/search?q=%24TSLA&f=live")
data= []; last_height= driver.execute_script("return document.body.scrollHeight")
for _ in range(50):
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 2))
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article div[lang]")))
    articles= driver.find_elements(By.TAG_NAME, "article")
    for art in articles:
        try:
            text= art.find_element(By.CSS_SELECTOR, "div[lang]").text
            rt_el= art.find_element(By.XPATH, ".//div[@data-testid='retweet']")
            rt= int(rt_el.text.replace("K","000")) if rt_el.text else 0
            tl= art.find_element(By.TAG_NAME, "time").get_attribute("datetime")
            url= art.find_element(By.XPATH, ".//a[@role='link']").get_attribute("href")
            data.append({"text": text, "retweets": rt, "timestamp": tl, "url": url})
        except:
            continue
    new_height= driver.execute_script("return document.body.scrollHeight")
    if new_height== last_height:
        break
    last_height= new_height
os.makedirs("data/raw", exist_ok= True)
with open("data/raw/tweets.json", "w", encoding= "utf-8") as f:
    json.dump(data, f, ensure_ascii= False, indent= 2)

driver.quit()