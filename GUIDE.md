# SRM Developer Guide (Guide dial les Développeurs)

Hada wa7ed l-guide technique complet pour les développeurs li khddamin 3la l-système **SRM Customer Service AI**. Hada fih l-architecture, détails d'implémentation, workflows, w kifach t-modifié l-code étape par étape.

## Table of Contents

1. [Architecture Deep Dive](#architecture-deep-dive)
2. [Backend Architecture](#backend-architecture)
3. [Frontend Architecture](#frontend-architecture)
4. [Core Flows](#core-flows)
5. [How to Modify/Extend](#how-to-modifyextend)
6. [Testing Guide](#testing-guide)
7. [Deployment Considerations](#deployment-considerations)

---

## Architecture Deep Dive

### System Architecture

L-système SRM mtabe3 wa7ed **layered architecture** mferrqa mzyan (separation of concerns):

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│                    (Streamlit Frontend)                     │
│  - User Interface Components                                 │
│  - RTL/Arabic Styling                                        │
│  - API Client (HTTP)                                         │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP REST API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Application Layer                          │
│                    (FastAPI Backend)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Routes (REST Endpoints)             │   │
│  └───────────────────────┬──────────────────────────────┘   │
│                          │                                    │
│  ┌───────────────────────▼──────────────────────────────┐   │
│  │              AI Agent Layer                           │   │
│  │  - LangChain Agent (Azure OpenAI GPT-4)              │   │
│  │  - Tool Execution Engine                              │   │
│  │  - Message History Management                         │   │
│  └───────────────────────┬──────────────────────────────┘   │
│                          │                                    │
│  ┌───────────────────────▼──────────────────────────────┐   │
│  │              Business Logic Layer                     │   │
│  │  - UserService (Payment checks)                       │   │
│  │  - MaintenanceService (Outage checks)                 │   │
│  │  - OCRService (Bill extraction)                       │   │
│  └───────────────────────┬──────────────────────────────┘   │
│                          │                                    │
│  ┌───────────────────────▼──────────────────────────────┐   │
│  │              Data Access Layer                        │   │
│  │  - Repository Pattern (Abstract Interface)            │   │
│  │  - MockRepository (Pandas/In-Memory)                 │   │
│  │  - [Future: SQLRepository, Azure SQL]                │   │
│  └───────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

### Component Interactions (Kifach les composants kayhdrou binathom)

**Request Flow:**
1. L-Utilisateur kay-interagie m3a **Streamlit UI**.
2. Frontend component kay-3eyet 3la `SRMAPIClient`.
3. HTTP request katsifet l **FastAPI backend**.
4. Route handler kay-reçevoir l-request.
5. Dependency injection kat-fournir les services w l-agent.
6. Agent kay-traité l-message, w kay-exécuté les tools ila 7tajhom.
7. Tools kay-3eytou l services, w services kay-3eytou l repository.
8. Response katrje3 bl-3eks 3ber les layers.
9. Frontend kay-affiché l-résultat l l-user.

**Data Flow:**
- **User Input** → Chat Component → API Client → FastAPI Route → AI Agent
- **AI Agent** → Tool Execution → Service Layer → Repository → Data
- **Data** → Repository → Service → Tool Result → AI Agent → Response → Frontend

### Technology Stack

**Backend:**
- **FastAPI** (0.109.0) - Framework web Python moderne.
- **LangChain** (0.3.13) - Framework d'orchestration LLM.
- **LangChain OpenAI** (0.2.14) - Intégration Azure OpenAI.
- **Pydantic** (via pydantic-settings) - Data validation w settings.
- **Azure AI Document Intelligence** (1.0.0b1) - Service OCR.
- **Uvicorn** (0.27.0) - Serveur ASGI.

**Frontend:**
- **Streamlit** (1.29.0) - Framework UI web b Python.
- **HTTPX** (0.26.0) - HTTP client pour les appels API.

**Data:**
- **Pandas** (2.1.4) - Manipulation d data (f MockRepository).
- **Python-dotenv** (1.0.0) - Gestion d les variables d'environnement.

**Testing:**
- **Pytest** (8.4.1) - Framework d testing.
- **Pytest-asyncio** (0.23.3) - Support pour Async test.

---

## Backend Architecture

### FastAPI Application Structure

**Entry Point:** `backend/main.py`

```python
app = FastAPI(
    title="SRM API",
    description="SRM Water & Electricity Utility Customer Service API",
    version="1.0.0"
)
```

**Les Composants Mhimin:**

1. **CORS Middleware** - Bach tkhlli frontend yhdar m3a backend.
2. **Routers** - Handlers mferrqin (`/api/health`, `/api/chat`, `/api/ocr/*`).
3. **Startup Event** - Kay-initialisé AI agent mli server kaych3el.
4. **Dependency Injection** - Kat-wjd les instances d les services w l-agent.

### Models Layer (`backend/models/`)

Had l-layer katkhddem **Pydantic** bach t-validé data w t-serializiha.

#### User Model (`backend/models/user.py`)

```python
class User(BaseModel):
    cil: str  # Customer Identification Number (format: 1071324-101)
    name: str
    # ... autres champs
```

**CIL Validation:**
- Format: `7digits-3digits` (mithal: `1071324-101`).
- Validé b Pydantic field validator.
- Kay-lancer `ValueError` ila kan l-format machi howa hadak.

#### Zone Model, Chat Models, OCR Models
Koulchi définis b Pydantic bach n-assurer la qualité d data.

### Repository Pattern (`backend/repositories/`)

**Abstract Base Class:** `backend/repositories/base.py`

Kat-définir l-interface li ga3 les repositories khasshom y-implémentiw:

```python
class BaseRepository(ABC):
    @abstractmethod
    def get_user_by_cil(self, cil: str) -> Optional[User]
    # ... méthodes khrin
```

**Current Implementation:** `backend/repositories/mock_repository.py`

- Kaykhddem Pandas DataFrames f la mémoire (In-Memory).
- Kay-simulé les tables d la base de données (`_users_table`, `_zones_table`).
- Sahla tbeddlou b DB réelle (SQL) mli tbghi.

**Bach tzid Real Database:**
1. Créé classe jdida kat-hérité mn `BaseRepository`.
2. Implémenté les méthodes abstraites kamlin.
3. Bddel `backend/api/deps.py` bach tkhddem repository jdid.

### Services Layer (`backend/services/`)

Hna fin kayna **Business Logic** (Logique métier).

#### UserService (`backend/services/user_service.py`)

**L-hadaf:** Gérer les opérations d l-user, surtout `check_payment`.

**Kifach khddama:**
1. Jbed l-user mn repository b CIL.
2. Ila mal9itich l-user, rje3 erreur.
3. Checké status d l-khlass (Paid/Unpaid).
4. Formatté l-message b l-3arbiya 3la 7ssab l-état.
5. Rje3 `PaymentCheckResult`.

#### MaintenanceService (`backend/services/maintenance_service.py`)

**L-hadaf:** Checké wach kayn chi panne wla travaux f zone d l-client.

#### OCRService (`backend/services/ocr_service.py`)

**L-hadaf:** Jbed l-ma3loumat mn tsawer d l-factures b Azure Document Intelligence.

**Flow:**
1. Sift tswira l Azure API.
2. Reçevoir l-texte extracted.
3. Appliqué **Regex patterns** bach tjbed:
   - CIL (w t-normalizih, ex: `101-1071324` → `1071324-101`).
   - Nom, Montant, Date, etc.
4. Rje3 `OCRResult`.

### AI Agent (`backend/ai/`)

#### SRMAgent (`backend/ai/agent.py`)

**L-hadaf:** Orchestré l-conversation b LangChain w Azure GPT-4.

**Initialization:**
```python
agent = SRMAgent(...)
agent.initialize()  # Kay-wjd LLM w les tools
```

**Chat Flow:**
1. Jm3 l-messages (System Prompt + History + User Message).
2. Sift l LLM.
3. Chouf wach LLM bgha ysta3mel chi **Tool** (`response.tool_calls`).
4. Ila bgha tools:
   - Exécuté les tools (li kay-3eytou l services).
   - Zid les résultats (ToolMessage) l conversation.
   - 3awed 3eyet l LLM bach y3tik réponse finale.
5. Rje3 `ChatResponse`.

**Tools:** Des fonctions décorées b `@tool`, l-agent kay3rf imta ysta3mlhom b description dyalhom.

#### Prompts (`backend/ai/prompts.py`)

**System Prompt (`SYSTEM_PROMPT_AR`):**
- Kay-defini l-rôle d l-agent (SRM Assistant).
- Instructions bach ydwi b l-3arbiya.
- Règles (tloub CIL, t-checké paiement, etc.).

### Configuration (`backend/config.py`)

Kaysta3mel `pydantic-settings` bach y-géré les variables d'environnement (`.env`).
Kay-validé wach les clés Azure w API settings kymin.

### Dependency Injection (`backend/api/deps.py`)

**Singleton Pattern:** L-agent kayt-initialisé mra we7da w kayb9a f mémoire (`_agent_instance`).

---

## Frontend Architecture

### Streamlit Application (`frontend/app.py`)

**Initialization Flow:**
1. Configurer la page (Title, Layout).
2. Injecté CSS d l-3arbiya (RTL).
3. Initialisé API Client.
4. Checké Health d backend (ila tafi, l-app kat7bess).
5. Render les composants (Header, Sidebar, Chat).

**Session State:**
- `st.session_state.messages`: Hna fin mkhbyin les messages d chat bach maymchiwch mli dir refresh.

### Components

- **Chat Component:** L-interface principale. Kay-affiché messages w input field.
- **File Upload:** Upload d l-image, preview, w appel l OCR endpoint.
- **Sidebar:** Info w instructions.
- **Header:** Branding w styling.

### API Client (`frontend/api_client.py`)

Wrapper 3la `httpx.Client` bach ydwz les appels HTTP (GET/POST) l backend bla ma t-kerrer l-code d l-error handling.

### RTL Styling (`frontend/styles/rtl.py`)

Code CSS bach y-forced l-interface tkon mn limen l lissar (Right-to-Left) w y9ad l-fonts d l-3arbiya.

---

## Core Flows

### Chat Flow (Step-by-Step)

**Scenario:** User sift CIL number.

1. **User Input:** User kteb "CIL diali: 1071324-101".
2. **Frontend:** Sift request `POST /api/chat`.
3. **Backend Agent:**
   - LLM chaft CIL -> "Ah, khassni n-checké paiement".
   - **Tool Call:** `check_payment("1071324-101")`.
4. **Service Execution:**
   - `UserService` l9a user -> Status: "Paid".
   - Rejje3 message formatted: "معلومات العميل... ✅ مدفوع".
5. **Final Response:**
   - LLM chaft l-resultat -> "Ok, koulchi mkhless".
   - Généra réponse finale: "شكراً، وضعيتك سليمة...".
6. **Frontend:** Affiche la réponse.

### OCR Extraction Flow

1. **Upload:** User dar upload l image d l-facture.
2. **API Call:** Frontend sift image l `/api/ocr/extract-cil`.
3. **Processing:**
   - Azure Doc Intel jbed text.
   - Regex patterns 9lleb 3la format d CIL.
   - Normalize l-format (ila kan ma9loub).
4. **Result:** Rje3 CIL number.
5. **UI Update:** CIL tzad automatiquement f chat input.

---

## How to Modify/Extend (Kifach t-modifié l-code)

### Adding New API Endpoints (Zid Endpoint Jdid)

1. **Créé Route:** F `backend/api/routes/new_feature.py`.
2. **Add to Main:** Enregistré router f `backend/main.py`.
3. **Models:** Zid request/response models f `backend/models/`.

### Adding New AI Tools (Zid Tool Jdid l Agent)

1. **Créé Service Method:** Zid logique f service adéquat.
2. **Créé Tool Function:** F `backend/ai/tools.py`.
   ```python
   @tool
   def new_tool(param: str) -> str:
       """Description mzyana b l-3arbiya w English."""
       return service.method(param)
   ```
3. **Update Agent:** F `backend/ai/agent.py`, zid l-tool l la liste `self._tools`.
4. **Update System Prompt:** F `backend/ai/prompts.py`, 3lem l-agent anna 3ndu tool jdida.

### Swapping Mock Repository for Real Database (Bddel Mock b SQL)

1. **Créé SQL Repository:** F `backend/repositories/sql_repository.py`.
   - Implémenté `BaseRepository`.
   - Sta3mel `pyodbc` wla `sqlalchemy`.
2. **Update Deps:** F `backend/api/deps.py`.
   - Bddel `get_repository` bach y-instancié `SQLRepository` blasst `MockRepository`.
3. **Environment:** Zid Connection String f `.env`.

---

## Testing Guide

### Test Structure

- `tests/backend/`: Tests d API, Services, Agent.
- `tests/frontend/`: Tests d API Client.
- `conftest.py`: Fih les **Fixtures** (data d test, ex: `sample_user_paid`).

### Running Tests

```bash
# Lancer kolchi
pytest

# M3a coverage
pytest --cov=backend --cov=frontend

# Test spécifique
pytest tests/backend/test_services.py
```

### Writing New Tests (Kifach tkteb test)

Dima khddem **Mocking** l Azure services. Ma t-3eyetch l API d bss7 f tests!

```python
@patch('backend.services.ocr_service.OCRService._analyze_document')
def test_ocr(mock_analyze):
    mock_analyze.return_value = "fake text"
    # ... assert logic
```

---

## Deployment Considerations

### Environment Variables (Production)

Darouri tkon 3ndk had les variables f serveur de production:

```env
# Azure OpenAI (Prod Resource)
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_ENDPOINT=https://prod.openai.azure.com/

# Azure Doc Intel (Prod Resource)
AZURE_DOCUMENT_INTELLIGENCE_KEY=xxx

# Security
API_HOST=0.0.0.0
```

### Security Considerations

1. **API Keys:** Jamais t-commité `.env` f GitHub.
2. **CORS:** F Prod, ddir whitelist ghir l domain d frontend, machi `*`.
3. **HTTPS:** Darouri SSL/TLS f Production.

### Troubleshooting

- **Agent mabghach ykhdm?** Vérifié `AZURE_OPENAI_DEPLOYMENT_NAME` wach mtad9 m3a Azure Portal.
- **OCR kay-failé?** Vérifié wach tswira claire wla Azure Resource Key s7i7a.
- **Backend connexion refused?** Chouf wach port 8000 mftou7 w `API_HOST=0.0.0.0`.

---
