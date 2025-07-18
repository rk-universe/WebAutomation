Here’s a sample **description** you can use for your Docker image `rahulkumawat9729/webautomation:v1.0` on Docker Hub:

---

## 🧠 Streamlit Browser Automation with LLM (LangChain + NVIDIA AI)

This Docker image powers a **Streamlit web application** that automates browser navigation and interaction using a large language model (LLM). It connects to a Chrome browser (running in **remote debugging mode**) and makes decisions based on the page's HTML content — guided by user prompts.

---
## Demo Videos
https://drive.google.com/file/d/1joNQB8rqH4cvLmUKHECn4ch8Km8dhyUw/view?usp=sharing
https://drive.google.com/file/d/1NiId-IrKFBwNn1iAZY17D1X7blQldd3U/view?usp=sharing

### ✅ Features

* Streamlit-based web UI to input navigation goals
* Automates browser interaction using LangChain and NVIDIA LLM
* Uses your existing Chrome (running on host machine at `localhost:9222`)
* Tracks past actions via memory to avoid repetition
* Uses a LangChain prompt template to interact with the model

---

### 🔧 Requirements

This image expects a `.env` file (you must provide at runtime) with the following keys:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=<your_langchain_key>
NVIDIA_API_KEY=<your_nvidia_key>
BROWSER=localhost:9222
```

> ⚠️ Make sure your Chrome browser is launched in remote debugging mode like this:

```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome_profile"
```

---

### 🚀 Run the Container

```bash
docker run -p 8501:8501 \
  --shm-size=2g \
  --env-file .env \
  rahulkumawat9729/webautomation:v1.0
```

Then open your browser and go to:

```
http://localhost:8501
```

---

Let me know if you also want to support Chrome inside Docker or a remote Chrome container.
