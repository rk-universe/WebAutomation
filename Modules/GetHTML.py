import time
from transformers import GPT2Tokenizer
from selenium.webdriver.common.by import By

# Initialize tokenizer globally (you can switch to a different tokenizer if needed)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Inject JS and collect DOM elements with UID
def insert_js(driver):
    elements = driver.execute_script("""
      let elements = [];
      document.querySelectorAll("a, button, input, textarea, div").forEach((el, index) => {
          const style = window.getComputedStyle(el);
          const isVisible = style.display !== 'none' && style.visibility !== 'hidden' && el.offsetHeight > 0 && el.offsetWidth > 0;

          if (isVisible) {
              if (el.tagName === 'DIV') {
                  const hasCursorPointer = el.classList.contains('cursor-pointer');
                  const hasClickListener = el.getAttribute('onclick') !== null;
                  if (!(hasCursorPointer || hasClickListener)) return;
              }

              let uniqueId = el.tagName + '_' + index;
              el.setAttribute('data-uid', uniqueId);

              elements.push({
                  uid: uniqueId,
                  tag: el.tagName,
                  text: el.innerText.trim() || null,
                  title: el.title || null,
                  placeholder: el.placeholder || null,
                  name: el.name || null,
                  href: el.href || null,
                  type: el.type || null,
                  value: el.value || null,
                  className: el.className || null
              });
          }
      });
      return elements;
    """)
    return elements

# Filter out useless or empty elements
def filter_elements(elements):
    filtered_elements = []
    for element in elements:
        filtered_element = {}
        for key, value in element.items():
            if value in [None, ''] or key == 'className':
                continue

            if key == 'tag' and value == 'A':
                if not element.get('text') or not element.get('href'):
                    filtered_element = 0
                    break

            if key == 'href' and isinstance(value, str):
                pass  # Keep full href, do not truncate
            else:
                filtered_element[key] = value

        if filtered_element:
            filtered_elements.append(filtered_element)
    return filtered_elements

# Organize elements into categories for prompting
def organize_elements(elements):
    categories = {
        "Links": [],
        "Text Areas": [],
        "Buttons": [],
    }

    max_tokens = 2000
    total_tokens = 0

    for element in elements:
        if element["tag"] == "A":
            if total_tokens < max_tokens:
                ele = [element["text"], element["uid"]]
                combined_text = " ".join(ele)
                token_count = len(tokenizer.encode(combined_text))
                total_tokens += token_count
                categories["Links"].append(ele)

        elif element["tag"] == "TEXTAREA" or (element["tag"] == "INPUT" and element.get("type") != "submit"):
            if element.get("name") or element.get("title") or element.get("value") or element.get("placeholder"):
                entry = {
                    "name": element.get("name"),
                    "uid": element.get("uid"),
                    "title": element.get("title"),
                    "value": element.get("value"),
                    "placeholder": element.get("placeholder")
                }
                filtered = {k: v for k, v in entry.items() if v is not None}
                categories["Text Areas"].append(filtered)

        elif element["tag"] == "BUTTON" or (element["tag"] == "INPUT" and element.get("type") == "submit"):
            if element.get("name") or element.get("text") or element.get("value"):
                entry = {
                    "name": element.get("name"),
                    "text": element.get("text") or element.get("value"),
                    "uid": element.get("uid")
                }
                filtered = {k: v for k, v in entry.items() if v is not None}
                categories["Buttons"].append(filtered)

        elif element["tag"] == "DIV":
            if element.get("text") or element.get("value"):
                div_entry = [
                    element.get("text") or element.get("value"),
                    element.get("uid")
                ]
                categories["Links"].append(div_entry)

    return categories

# Master function: fetch and process page content
def fetch_html_content(driver):
    elements = insert_js(driver)
    filtered = filter_elements(elements)
    organized = organize_elements(filtered)

    for category, items in organized.items():
        print(f"--- {category} ---")
        for item in items:
            print(item)
        print()

    return organized

def get_page_description(driver):
    title = driver.title
    return title
