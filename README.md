# SRM - Customer Service AI Assistant

💧 **نظام خدمة العملاء - SRM** (Water & Electricity Utility Customer Service AI)

Hada wa7ed l-assistant AI intelligent dial service client pour les sociétés ta3 l-ma w dow (Water & Electricity), mbni b **FastAPI**, **Streamlit**, w **Azure OpenAI**.

Had l-système kay3awen les clients yfhmou 3lach t9t3at service, y-checkiw status dial l-khlass (payment), w yakhdou des infos 3la l-maintenance, w hadchi kaml b conversation tabi3iya b l-3arbiya (Natural Language).

## 🎯 Key Features 

- **🤖 AI-Powered Chat Interface**: Chat katzwi b l-3arbiya b 7orya (Natural Language) grâce l **Azure OpenAI GPT-4**.
- **📄 OCR Bill Processing**: Kay-extracté l-numéro CIL w les infos mn tsawer dial l-facture b **Azure Document Intelligence**.
- **💳 Payment Status Check**: Vérification wach l-client mkhlless wla ba9i ki tsal chi montant (outstanding balances).
- **🔧 Maintenance Information**: Kay-checké wach kayna chi travaux de maintenance awla service outage f zone dial l-client.
- **🌐 RTL Arabic UI**: Interface fully localized l l-3arbiya w supportée RTL (Right-to-Left).
- **🔄 Tool-Based AI Agent**: Agent mbni b **LangChain** li 9ader ykhddem des "tools" bach yjib l-information en temps réel.

## 🏗️ Architecture Overview
L'archi de base hiya normalement f had refonte dayrin sepration total mabin back o front 

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Chat   │  │   OCR    │  │ Sidebar  │  │  Header  │  │
│  │ Component│  │ Component│  │Component │  │Component │  │
│  └────┬─────┘  └────┬─────┘  └──────────┘  └──────────┘  │
│       │             │                                        │
│       └──────┬──────┘                                        │
│              │                                               │
│       ┌──────▼──────┐                                        │
│       │ API Client  │                                        │
│       └──────┬──────┘                                        │
└──────────────┼───────────────────────────────────────────────┘
               │ HTTP/REST
               │
┌──────────────▼───────────────────────────────────────────────┐
│              Backend (FastAPI)                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Routes                              │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐   │   │
│  │  │ /chat  │  │ /ocr/*  │  │/health │  │  ...   │   │   │
│  │  └───┬────┘  └───┬────┘  └────────┘  └────────┘   │   │
│  └──────┼────────────┼──────────────────────────────────┘   │
│         │            │                                        │
│  ┌──────▼────────────▼──────┐                               │
│  │      SRM AI Agent         │                               │
│  │  (LangChain + Azure GPT)  │                               │
│  │  ┌─────────────────────┐  │                               │
│  │  │  Tools:             │  │                               │
│  │  │  - check_payment    │  │                               │
│  │  │  - check_maintenance│  │                               │
│  │  └──────────┬──────────┘  │                               │
│  └─────────────┼─────────────┘                               │
│                │                                               │
│  ┌─────────────▼─────────────┐                               │
│  │      Services Layer        │                               │
│  │  ┌──────────┐ ┌─────────┐│                               │
│  │  │   User   │ │Maintenance││                               │
│  │  │ Service  │ │ Service  ││                               │
│  │  └────┬─────┘ └────┬─────┘│                               │
│  │       │            │        │                               │
│  │  ┌────▼────────────▼─────┐│                               │
│  │  │   OCR Service          ││                               │
│  │  │  (Azure Doc Intel)    ││                               │
│  │  └───────────────────────┘│                               │
│  └─────────────┬─────────────┘                               │
│                │                                               │
│  ┌─────────────▼─────────────┐                               │
│  │   Repository Layer         │                               │
│  │  (MockRepository/Pandas)   │                               │
│  └────────────────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Li Khass Ykon 3ndk

- **Python 3.9+** (Mzyana tkon 3.10 wla 3.11).
- **Azure OpenAI Account** m3a GPT-4 deployment.
- **Azure Document Intelligence** service (bach tkhddem l-OCR).
- **Git** (bach t-cloné l-repo).
- **Windows PowerShell** (ila bghiti tsta3ml l-setup script) awla setup manuel.

## 🚀 Quick Start (Kifach Tbda)

### 1. Clone the Repository

Awl 7aja, cloné l-repo f machine dialek:

```bash
git clone <repository-url>
cd SRM
```

### 2. Run Setup Script (Windows PowerShell)

Ila knti f Windows, l-script wajed bach y-installé lik koulchi:

```powershell
.\setup.ps1
```

Had l-script ghadi ydir hadchi:
- Y-checké l-installation dial Python.
- Y-créé l-environnement virtuel (`venv`).
- Y-installé les dépendances (dependencies) kamlin.
- Y-créé l-fichier `.env` mn template (ila makanch deja kayn).

### 3. Manual Setup (Alternative)

Ila knti f Linux/Mac, wla bghiti t-installé b yeddek:

```bash
# Créé virtual environment
python -m venv venv

# Activé l'environnement
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Installé les requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Khass t-créé fichier `.env` f racine dial projet w t7et fih les credentials Azure dialek:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-08-01-preview

# Azure Document Intelligence Configuration
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_document_intelligence_key

# Optional: API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### 5. Run the Application

#### Option A: Run Both Services Together (Recommandé)

B commande we7da t-lancé backend w frontend d9a we7da:

```bash
python run.py
```

Hadchi ghaykhddem:
- **Backend API** f `http://localhost:8000`
- **Frontend UI** f `http://localhost:8501`

#### Option B: Run Services Separately

**Terminal 1 - Backend:**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend/app.py --server.port 8501
```

### 6. Access the Application

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc

## 🧪 Testing

### Run All Tests

Bach t-lancé les tests kamlin:

```bash
pytest
```

### Run Tests with Coverage

Ila bghiti tchouf coverage report:

```bash
pytest --cov=backend --cov=frontend
```

### Run Specific Test Files

```bash
# Test dial services
pytest tests/backend/test_services.py

# Test dial API endpoints
pytest tests/backend/test_api/

# Test dial AI agent
pytest tests/backend/test_ai_agent.py
```

## 📡 API Endpoints

### Health Check
- `GET /api/health` - Bach tchouf wach l-API khddama mzyan.

### Chat
- `POST /api/chat` - Sift message l l-AI agent.
  ```json
  {
    "message": "رقم CIL الخاص بي هو: 1071324-101",
    "history": []
  }
  ```

### OCR
- `POST /api/ocr/extract-cil` - Jbed l-CIL number mn tswira.
- `POST /api/ocr/extract-bill` - Jbed les infos dial l-facture kamlin mn tswira.

Chouf documentation kamla f `http://localhost:8000/docs` mli tkon l-backend khddama.

## 📁 Project Structure

Structure dial les dossiers kifach dayra:

```
SRM/
├── backend/                 # Backend FastAPI application
│   ├── ai/                  # AI agent w tools
│   │   ├── agent.py        # SRM AI Agent (LangChain)
│   │   ├── tools.py        # Définition dial LangChain tools
│   │   └── prompts.py      # AI prompts (b l-3arbiya)
│   ├── api/                 # API routes w dependencies
│   │   ├── routes/         # Handlers dial API endpoints
│   │   │   ├── chat.py     # Chat endpoint
│   │   │   ├── ocr.py      # OCR endpoints
│   │   │   └── health.py   # Health check
│   │   └── deps.py         # Dependency injection
│   ├── models/             # Pydantic data models
│   ├── repositories/       # Data access layer (Mock DB)
│   ├── services/           # Business logic layer (User, Maintenance, OCR)
│   ├── config.py           # Config management
│   └── main.py             # FastAPI entry point
├── frontend/               # Streamlit frontend
│   ├── components/        # UI components (Chat, Sidebar, etc.)
│   ├── styles/            # CSS Styles (RTL support)
│   ├── api_client.py      # Client li kaydwi m3a Backend
│   └── app.py             # Streamlit entry point
├── tests/                  # Test suite
├── requirements.txt       # Les librairies Python
├── setup.ps1             # Script setup Windows
├── run.py                # Script bach t-lancé kolchi
└── GUIDE.md              # Guide détaillé pour les développeurs
```

## 🔧 Configuration

### Environment Variables

Had les variables darouri t-configurihom:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AZURE_OPENAI_API_KEY` | Key dial Azure OpenAI | Yes | - |
| `AZURE_OPENAI_ENDPOINT` | Endpoint URL dial Azure OpenAI | Yes | - |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Smya dial GPT-4 deployment | No | `gpt-4o` |
| `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` | Endpoint dial Doc Intelligence | Yes | - |
| `AZURE_DOCUMENT_INTELLIGENCE_KEY` | Key dial Doc Intelligence | Yes | - |
| `API_HOST` | Backend host | No | `0.0.0.0` |
| `API_PORT` | Backend port | No | `8000` |

## 🧩 Key Components (Les Éléments MOHIMIINNNEEE hhhh)

### AI Agent (`backend/ai/agent.py`)
- Agent mbni b LangChain (yaa3 mais 3gzt ndero from scratch ) w Azure OpenAI GPT-4.
- Architecture "Tool-based" bach y-exécuté la logique métier (check solde, etc.).
- Prompts m9adin b l-3arbiya bach ykon l-jawab fniwen ozwiwen o nwidee hhhhh

### OCR Service (`backend/services/ocr_service.py`)
- Intégration m3a Azure Document Intelligence.
- Kaysta3ml Regex patterns bach yjbed CIL.
- Kay-extracté l-montant, date, w type de service mn l-facture.

### Mock Repository (`backend/repositories/mock_repository.py`)
- Data store "In-memory" b Pandas.
- Kay-simulé base de données Azure SQL.
- Sahla tbddelha b implémentation réelle mli t-connecté m3a DB dial bss7.

## 📚 Documentation

- **[GUIDE.md](GUIDE.md)** - Guide complet fih les détails dial architecture, flows, w kifach t-modifié l-code.

## 🤝 Contributing

1. Tb3 l-architecture patterns li kaynin f l-code.
2.kteb tests l ay feature jdida.
3. Mise à jour l-documentation ila bddelti chi 7aja.
4. Tbe3 les standards PEP 8 dial Python.

## 🆘 Troubleshooting (7ll l-machakil)

### Backend won't start (Backend mabghach ykhdm)
- Vérifié wach environment variables kamlin m7totin f `.env`.
- Chof wach Azure credentials s7a7.
- T2aked anna port 8000 ma-mst3mlch mn jiha khra.

### Frontend can't connect to backend
- T2aked anna Backend running f `http://localhost:8000`.
- Chof `API_URL` ila knti mkhddem custom URL.
- Vérifié CORS settings f `backend/main.py`.

### OCR extraction fails
- T2aked mn Azure Document Intelligence credentials.
- Chof format dial l-image (PNG, JPG, JPEG, PDF).
- T2aked anna l-image fiha ktba bayna (readable text).

### AI agent not responding
- Vérifié Azure OpenAI credentials w deployment name.
- T2aked mn API version wach compatible m3a subscription dialek.
- Chof les logs dial backend bach t3rf l-erreur exact.