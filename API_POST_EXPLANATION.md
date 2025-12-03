# 🔍 Azure OpenAI API - How It Actually Works

## The Confusion: Where's the POST?

You're correct - Azure OpenAI **does use HTTP POST**, but in this project, you don't see it explicitly because **LangChain abstracts it away**.

---

## What Happens Behind the Scenes

### **Your Code** (`services/ai_service.py`)
```python
from langchain_openai import AzureChatOpenAI

# This looks simple...
llm = AzureChatOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_version=settings.AZURE_OPENAI_API_VERSION,
    deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
    temperature=0.7,
    max_tokens=1000
)

# And you just call invoke()
response = llm.invoke(messages)
```

### **What LangChain Does Under the Hood**

When you call `llm.invoke()`, LangChain internally makes this HTTP POST request:

```http
POST https://chikayaopenai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview
Content-Type: application/json
api-key: YOUR_AZURE_OPENAI_API_KEY

{
  "messages": [
    {"role": "system", "content": "أنت مساعد خدمة العملاء..."},
    {"role": "user", "content": "رقم CIL الخاص بي هو: 1071324-101"}
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "check_payment",
        "description": "يستخدم للتحقق من حالة الدفع...",
        "parameters": {...}
      }
    },
    {
      "type": "function", 
      "function": {
        "name": "check_maintenance",
        "description": "يستخدم للتحقق من أعمال الصيانة...",
        "parameters": {...}
      }
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### **Response from Azure**
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "created": 1733241600,
  "model": "gpt-4o",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_abc123",
            "type": "function",
            "function": {
              "name": "check_payment",
              "arguments": "{\"cil\": \"1071324-101\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ],
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 25,
    "total_tokens": 175
  }
}
```

---

## If You Want to See the Raw POST Request

### **Option 1: Enable Verbose Logging**

Add this to see what LangChain sends:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now run your agent
response = llm.invoke(messages)
# You'll see the HTTP requests in console
```

### **Option 2: Use Raw Azure OpenAI Client** (Without LangChain)

```python
from openai import AzureOpenAI

# Direct client (no LangChain abstraction)
client = AzureOpenAI(
    api_key="YOUR_AZURE_OPENAI_API_KEY",
    api_version="2024-08-01-preview",
    azure_endpoint="https://chikayaopenai.openai.azure.com/"
)

# Explicit POST request
response = client.chat.completions.create(
    model="gpt-4o",  # deployment name
    messages=[
        {"role": "system", "content": "أنت مساعد..."},
        {"role": "user", "content": "مرحبا"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

This also uses POST internally, but now you have more control.

### **Option 3: Use `requests` Library Directly** (Raw HTTP)

```python
import requests
import json

url = "https://chikayaopenai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"

headers = {
    "Content-Type": "application/json",
    "api-key": "YOUR_AZURE_OPENAI_API_KEY"
}

data = {
    "messages": [
        {"role": "system", "content": "أنت مساعد خدمة العملاء"},
        {"role": "user", "content": "مرحبا"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
}

# Explicit POST request
response = requests.post(url, headers=headers, json=data)
result = response.json()

print(result['choices'][0]['message']['content'])
```

---

## The Full Request Flow in Your App

```
User types message in Streamlit UI
    ↓
ui/chat_interface.py: render_chat_interface()
    ↓
services/ai_service.py: run_agent(agent, user_input, chat_history)
    ↓
llm.invoke(messages)  ← This is where the magic happens
    ↓
LangChain internally does:
    ↓
    HTTP POST to Azure OpenAI API
    URL: https://chikayaopenai.openai.azure.com/openai/deployments/gpt-4o/chat/completions
    Headers: api-key, Content-Type
    Body: JSON with messages, tools, temperature, etc.
    ↓
Azure OpenAI processes request
    ↓
Returns JSON response
    ↓
LangChain parses response
    ↓
If tool_calls present → Execute tools → Send results back (another POST)
    ↓
Return final response to your code
    ↓
Display in Streamlit UI
```

---

## Why LangChain Abstracts the POST?

**Benefits:**
✅ Cleaner code - no manual HTTP handling
✅ Automatic retry logic
✅ Built-in tool/function calling support
✅ Message history management
✅ Streaming support
✅ Error handling

**Trade-off:**
❌ Less visibility into actual HTTP requests
❌ Harder to debug network issues
❌ Dependency on LangChain library

---

## Document Intelligence Also Uses POST

Similarly, in `services/ocr_service.py`:

```python
from azure.ai.documentintelligence import DocumentIntelligenceClient

client = DocumentIntelligenceClient(
    endpoint=settings.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
    credential=AzureKeyCredential(settings.AZURE_DOCUMENT_INTELLIGENCE_KEY)
)

# This looks simple...
poller = client.begin_analyze_document(
    "prebuilt-read",
    analyze_request=image_bytes,
    content_type="application/octet-stream"
)
```

**But internally it does:**
```http
POST https://di-srm.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-read:analyze?api-version=2024-02-29-preview
Content-Type: application/octet-stream
Ocp-Apim-Subscription-Key: YOUR_DOCUMENT_INTELLIGENCE_KEY

<binary image data>
```

---

## Summary

**Question:** "Where's the POST method?"

**Answer:** It's **hidden inside the LangChain and Azure SDK libraries**. They handle all the HTTP POST requests for you.

**If you want to see/control the POST:**
1. Enable debug logging
2. Use raw `openai` SDK instead of LangChain
3. Use `requests` library directly
4. Monitor network traffic with tools like Fiddler/Wireshark

**Current setup:** ✅ Works perfectly, POST is handled automatically!

---

Built with abstraction layers for cleaner code! 🚀
