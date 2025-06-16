import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_element(driver, tag=None, text=None, data_uid=None):
    try:
        if data_uid:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-uid='{data_uid}']"))
            )
        elif tag and text:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//{tag}[text()='{text}']"))
            )
        else:
            raise ValueError("Either data_uid or both tag and text must be provided.")

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", element)
        print(f"Clicked on element with tag '{tag}' or data-uid '{data_uid}'")
    except Exception as e:
        print(f"[Error] Click failed on '{tag or data_uid}': {e}")

def enter_text(driver, tag=None, text_to_enter=None, data_uid=None):
    try:
        if data_uid:
            element = driver.find_element(By.CSS_SELECTOR, f"[data-uid='{data_uid}']")
        elif tag:
            element = driver.find_element(By.TAG_NAME, tag)
        else:
            raise ValueError("Either data_uid or tag must be provided.")

        element.clear()
        element.send_keys(text_to_enter)
        element.send_keys(Keys.RETURN)
        print(f"Entered '{text_to_enter}' in element with tag '{tag}' or data-uid '{data_uid}'")
    except Exception as e:
        print(f"[Error] Text entry failed in '{tag or data_uid}': {e}")

def perform_action(driver, model_response):
    click_match = re.match(r"1,\s*([\w\d_]+)", model_response)
    enter_match = re.match(r"2,\s*(.+?),\s*([\w\d_]+)", model_response)

    if click_match:
        data_uid = click_match.group(1)
        click_element(driver, data_uid=data_uid)
    elif enter_match:
        text_to_enter = enter_match.group(1).strip()
        data_uid = enter_match.group(2)
        enter_text(driver, text_to_enter=text_to_enter, data_uid=data_uid)
    elif model_response.strip().lower() == "done":
        print("[Info] Action is marked done by model.")
    else:
        print("[Error] Invalid model response format.")
