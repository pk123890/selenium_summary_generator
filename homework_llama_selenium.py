# imports

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager



driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def selenium_scrape_data():
    val = input("Enter a url: ")
    wait = WebDriverWait(driver,30)
    driver.get(val)

    get_url = driver.current_url
    page_source = driver.page_source

    soup = BeautifulSoup(page_source,features="html.parser")
    for irrelevant in soup.body(["script", "style", "img", "input"]):
        irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    text = soup.body.get_text(separator="\n", strip=True)
    return text

def llm_summary_generation(text: str):
    OLLAMA_API = "http://localhost:11434/api/chat"
    HEADERS = {"Content-Type": "application/json"}
    MODEL = "llama3.2"

    messages = [
        {"role": "user", "content": f"The contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too. {text}"}
    ]

    payload = {
            "model": MODEL,
            "messages": messages,
            "stream": False
        }


    response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
    print(response.json()['message']['content'])


llm_summary_generation(selenium_scrape_data())




