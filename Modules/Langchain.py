from langchain.prompts import PromptTemplate
# Define the prompt template
prompt_template = """
**Context:** 
You are a human using a computer. By seeing the HTML content like links, buttons, and text areas present on the page provided below, you can perform actions to achieve the goal.

**Goal:** 
Navigate to: {user_prompt}

**Memory:** 
Previously visited pages and actions performed by you (avoid repetition):
{memory_data}

**Current Page:** 
Page title: {current_page}

**Html content:** 
---- Links ----
{links}

---- Text Areas ----
{text}

---- Buttons ----
{buttons}


HTML Content format:
- Links: (text, uid)
- Text Areas: (field, uid)
- Buttons: (field, uid)

**Instructions:** 
Based on the goal and HTML content, guide navigation or interaction by responding in the **exact format below**.

- To click a button or link: `"1, (uid)"`
- To enter text in a text area: `"2, (text to enter), (uid)"`
- If the goal is achieved or no further actions are required: `"done"`

**Response Rules:** 
1. Always include `uid` in the response.
2. Look into Memory and **never repeat** an action; just output `"done"` if already done.
3. Respond with **only one action** per reply.
4. ❗ Do NOT provide explanations, reasoning, or text outside the required format.

**Reminder:**  
Do not repeat steps already done in memory.
"""

# Create PromptTemplate
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["user_prompt", "links", "text", "buttons", "current_page", "memory_data"]
)

# Format prompt using content from the current page
def format_prompt(user_prompt, stored_results, current_page, memory_data=""):
    return prompt.format(
        user_prompt=user_prompt,
        links=stored_results.get("Links", ""),
        text=stored_results.get("Text Areas", ""),
        buttons=stored_results.get("Buttons", ""),
        current_page=current_page,
        memory_data=memory_data
    )

