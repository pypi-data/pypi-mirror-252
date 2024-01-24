import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os

class ChatBot:
    def __init__(self):
        # Set up Chrome options
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--log-level=3')  # Add this line
        warnings.simplefilter("ignore")
        # Initialize WebDriver
        self.driver = webdriver.Chrome(options=options)

        self.HelpingAI = "https://chat-app-b8c333.zapier.app/"
        # Navigate to the target URL
        self.driver.get(self.HelpingAI)
        time.sleep(7)

        # Security Bypass: Refresh the page if the title contains 'just a moment'
        while 'just a moment' in self.driver.title.lower():
            self.driver.refresh()

        # Initialize Chat_Num
        self.Chat_Num = 2

    # Function to increment Chat_Num
    def increment_chat_num(self):
        self.Chat_Num = str(int(self.Chat_Num) + 1)

    # Function to send a query and retrieve response
    def send_query(self, query):
        text_box_xpath = "/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div/form/fieldset/textarea"
        send_button_xpath = "/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div/form/fieldset/button"
        response_xpath = f"/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div/div/div/div[{self.Chat_Num}]/div[2]"
        button_xpath = f"/html/body/div[1]/main/div[1]/div/div/div/div/div/div/div/div/div/div[{self.Chat_Num}]/div[1]/div/form/div/div[1]/button"

        # Find the text box, enter query, and click send
        text_box = self.driver.find_element(by=By.XPATH, value=text_box_xpath)
        text_box.clear()
        text_box.send_keys(query)
        time.sleep(0.25)  # Pause for 1 second after typing query

        send_button = self.driver.find_element(by=By.XPATH, value=send_button_xpath)
        send_button.click()

        # Continuously check for the presence of the button every second
        while True:
            try:
                button = self.driver.find_element(by=By.XPATH, value=button_xpath)
                # If the button is found, retrieve and print the response
                response = self.driver.find_element(by=By.XPATH, value=response_xpath).text
                print("🤖:", response)
                break
            except NoSuchElementException:
                time.sleep(0.25)  # If the button is not found, wait for 1 second before checking again

        self.increment_chat_num()

    # Function to ask the user for a query, send it, and print the response
    def query_chat(self):
        while True:
            query = input("🧑: ")
            if query.lower() == 'exit':
                break

            self.send_query(query)
            time.sleep(0.25)  # Pause for 1 second before asking for the next query

    # Close the browser window
    def close(self):
        self.driver.quit()
