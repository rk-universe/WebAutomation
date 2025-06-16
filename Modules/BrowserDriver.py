from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def connect_to_existing_chrome_session(debugger_address="localhost:9222"):
    """
    Connects to an existing Chrome browser session with remote debugging enabled.

    Args:
        debugger_address (str): The debugger address of the Chrome instance.

    Returns:
        WebDriver: A Selenium WebDriver instance connected to the existing session.
    """
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)

    driver = webdriver.Chrome(options=chrome_options)
    print(f"[Connected] Current page title: {driver.title}")
    return driver

# 👇 Add this to run directly from terminal
if __name__ == "__main__":
    connect_to_existing_chrome_session()
