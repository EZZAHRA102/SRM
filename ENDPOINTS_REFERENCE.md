# 🔗 Azure Endpoints Usage Reference

## Configuration Flow

```
.env file
    ↓
config/settings.py (loads environment variables)
    ↓
services/ai_service.py (Azure OpenAI)
services/ocr_service.py (Azure Document Intelligence)
```

---

## 1. Azure OpenAI Endpoint

### **Configuration (.env)**
```env
AZURE_OPENAI_ENDPOINT=https://chikayaopenai.openai.azure.com/
AZURE_OPENAI_API_KEY=YOUR_AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

### **Used In:** `services/ai_service.py`

```python
# Line ~156-163
llm = AzureChatOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,      # ← Used here
    api_key=settings.AZURE_OPENAI_API_KEY,              # ← Used here
    api_version=settings.AZURE_OPENAI_API_VERSION,      # ← Used here
    deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,  # ← Used here
    temperature=0.7,
    max_tokens=1000
)
```

### **Purpose:**
- Powers the AI chatbot agent
- Processes user queries in Arabic
- Executes tools (check_payment, check_maintenance)
- Generates intelligent responses

---

## 2. Azure Document Intelligence Endpoint

### **Configuration (.env)**
```env
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://di-srm.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=YOUR_DOCUMENT_INTELLIGENCE_KEY
```

### **Used In:** `services/ocr_service.py`

#### **Function: extract_cil_from_image()**
```python
# Line ~25-28
client = DocumentIntelligenceClient(
    endpoint=settings.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,  # ← Used here
    credential=AzureKeyCredential(settings.AZURE_DOCUMENT_INTELLIGENCE_KEY)  # ← Used here
)
```

#### **Function: extract_text_from_image()**
```python
# Line ~70-73
client = DocumentIntelligenceClient(
    endpoint=settings.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,  # ← Used here
    credential=AzureKeyCredential(settings.AZURE_DOCUMENT_INTELLIGENCE_KEY)  # ← Used here
)
```

#### **Function: extract_bill_information()**
```python
# Line ~120-123
client = DocumentIntelligenceClient(
    endpoint=settings.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,  # ← Used here
    credential=AzureKeyCredential(settings.AZURE_DOCUMENT_INTELLIGENCE_KEY)  # ← Used here
)
```

### **Purpose:**
- Extracts text from uploaded bill images
- OCR (Optical Character Recognition)
- Identifies CIL, name, amounts, dates, etc.
- Supports Arabic and French text

---

## 3. Azure Speech Endpoint (Future Use)

### **Configuration (.env)**
```env
AZURE_SPEECH_ENDPOINT=https://eastus.api.cognitive.microsoft.com/
AZURE_SPEECH_KEY=YOUR_SPEECH_KEY
AZURE_SPEECH_REGION=eastus
```

### **Status:** Not yet implemented
### **Future Purpose:**
- Voice input (speech-to-text)
- Voice responses (text-to-speech)
- Arabic voice support

---

## Settings Loader: `config/settings.py`

```python
class Settings:
    """Application settings loaded from environment variables."""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: Optional[str] = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT: Optional[str] = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT_NAME: Optional[str] = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    
    # Azure Document Intelligence Configuration
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: Optional[str] = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    AZURE_DOCUMENT_INTELLIGENCE_KEY: Optional[str] = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
```

---

## Endpoint Validation

### **At Application Startup** (`app.py`)

```python
# Line ~27-32
# Validate configuration
is_valid, missing_keys = settings.validate()

if not is_valid:
    st.error(settings.get_error_message(missing_keys))
    st.stop()
```

### **Validation Logic** (`config/settings.py`)

```python
@classmethod
def validate(cls) -> tuple[bool, list[str]]:
    """Validate that all required settings are present."""
    missing_keys = []
    
    if not cls.AZURE_OPENAI_API_KEY:
        missing_keys.append("AZURE_OPENAI_API_KEY")
    if not cls.AZURE_OPENAI_ENDPOINT:
        missing_keys.append("AZURE_OPENAI_ENDPOINT")
    if not cls.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT:
        missing_keys.append("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    if not cls.AZURE_DOCUMENT_INTELLIGENCE_KEY:
        missing_keys.append("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    
    is_valid = len(missing_keys) == 0
    return is_valid, missing_keys
```

---

## Endpoint URLs Breakdown

### **1. Azure OpenAI Endpoint**
```
https://chikayaopenai.openai.azure.com/
```
- **Resource Name**: `chikayaopenai`
- **Service**: Azure OpenAI Service
- **Region**: (embedded in resource)
- **Deployment**: `gpt-4o`

### **2. Document Intelligence Endpoint**
```
https://di-srm.cognitiveservices.azure.com/
```
- **Resource Name**: `di-srm`
- **Service**: Azure Cognitive Services (Document Intelligence)
- **Region**: (embedded in resource)

### **3. Speech Endpoint**
```
https://eastus.api.cognitive.microsoft.com/
```
- **Region**: East US
- **Service**: Azure Cognitive Services (Speech)

---

## API Calls Made

### **Azure OpenAI API**
```
POST https://chikayaopenai.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview

Headers:
  api-key: YOUR_AZURE_OPENAI_API_KEY
  Content-Type: application/json

Body:
  {
    "messages": [...],
    "tools": [...],
    "temperature": 0.7,
    "max_tokens": 1000
  }
```

### **Document Intelligence API**
```
POST https://di-srm.cognitiveservices.azure.com/documentintelligence/documentModels/prebuilt-read:analyze?api-version=2024-02-29-preview

Headers:
  Ocp-Apim-Subscription-Key: YOUR_DOCUMENT_INTELLIGENCE_KEY
  Content-Type: application/octet-stream

Body:
  <image bytes>
```

---

## How to Change Endpoints

### **Option 1: Edit .env file**
```bash
# Open .env in editor
notepad .env

# Update values
AZURE_OPENAI_ENDPOINT=https://your-new-resource.openai.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-new-di.cognitiveservices.azure.com/
```

### **Option 2: Environment Variables (PowerShell)**
```powershell
$env:AZURE_OPENAI_ENDPOINT="https://your-new-resource.openai.azure.com/"
$env:AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="https://your-new-di.cognitiveservices.azure.com/"
```

### **Option 3: Update settings.py directly** (Not recommended)
```python
# In config/settings.py - hardcode values (not recommended for security)
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
```

---

## Testing Endpoints

### **Test Azure OpenAI Connection**
```python
python -c "from services.ai_service import initialize_agent; agent = initialize_agent(); print('✅ Azure OpenAI connected!' if agent else '❌ Connection failed')"
```

### **Test Document Intelligence Connection**
```python
python -c "from services.ocr_service import extract_text_from_image; print('✅ Document Intelligence configured!')"
```

---

## Endpoint Security

✅ **Good Practices:**
- ✅ Keys stored in `.env` file
- ✅ `.env` file in `.gitignore` (not pushed to GitHub)
- ✅ Template provided in `.env.example`
- ✅ Validation at startup

⚠️ **Important:**
- Never commit `.env` to GitHub
- Rotate keys regularly
- Use Azure Key Vault for production
- Implement IP restrictions in Azure portal

---

## Cost Monitoring

### **Azure OpenAI**
- Charged per token (input + output)
- Monitor in Azure Portal → Cost Management
- Current model: GPT-4o

### **Document Intelligence**
- Charged per page analyzed
- Free tier: 500 pages/month
- Monitor in Azure Portal → Cost Management

---

Built with Azure AI Services! 🚀
