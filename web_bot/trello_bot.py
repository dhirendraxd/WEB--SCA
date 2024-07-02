from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Chrome options
OP = Options()
OP.add_argument('--headless')

# Use WebDriverManager to automatically download and manage chromedriver
DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=OP)

def main():
    try:
        DRIVER.get("https://trello.com")
        input("Bot operation completed. Press any key to continue...")
        DRIVER.close()
    except Exception as e:
        print(e)
        DRIVER.close()

if __name__ == "__main__":
    main()
