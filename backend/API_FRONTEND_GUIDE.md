# 📚 Documentation API - SRM Backend

Guide complet pour l'équipe frontend pour consommer les APIs du backend SRM.

## 🚀 Démarrage Rapide

### 1. Importer la Collection Postman

1. Ouvrir Postman
2. Cliquer sur **Import**
3. Sélectionner le fichier `SRM_API_Collection.postman_collection.json`
4. La collection "SRM API Collection" apparaît avec tous les endpoints

### 2. Configuration

**Base URL par défaut:** `http://localhost:5000/api`

**Variables de collection:**
- `base_url`: URL de base de l'API
- `conversation_id`: ID de conversation (auto-sauvegardé)

---

## 📋 Endpoints Disponibles

### 🏥 **Health Check**

#### `GET /api/health`
Vérifie que le serveur fonctionne.

**Réponse:**
```json
{
  "status": "healthy",
  "message": "SRM API is running",
  "message_ar": "نظام SRM يعمل بشكل صحيح"
}
```

---

### 💬 **Chat**

#### `POST /api/chat`
Envoyer un message au chat agent.

**Body (nouveau message):**
```json
{
  "message": "مرحبا، أريد معرفة حالة خدمتي"
}
```

**Body (continuer conversation):**
```json
{
  "message": "رقم CIL الخاص بي هو: 1071324-101",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Réponse:**
```json
{
  "response": "مرحبا بك! كيف يمكنني مساعدتك اليوم؟",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_new_conversation": true,
  "status": "success"
}
```

**Important pour le frontend:**
- Sauvegarder le `conversation_id` retourné
- Renvoyer ce `conversation_id` dans tous les messages suivants
- `is_new_conversation`: `true` si première requête, `false` sinon

#### `GET /api/chat/history/{conversation_id}`
Récupérer l'historique d'une conversation.

**Réponse:**
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-12-04T10:30:00",
  "messages": [
    {
      "role": "user",
      "content": "مرحبا",
      "timestamp": "2024-12-04T10:30:00"
    },
    {
      "role": "assistant",
      "content": "مرحبا بك...",
      "timestamp": "2024-12-04T10:30:05"
    }
  ],
  "message_count": 2,
  "status": "success"
}
```

#### `POST /api/chat/reset`
Réinitialiser la session de chat.

**Réponse:**
```json
{
  "message": "Chat session reset",
  "message_ar": "تم إعادة تعيين المحادثة",
  "status": "success"
}
```

---

### 📄 **OCR (Extraction de documents)**

#### `POST /api/ocr/extract`
Extraire le texte d'un document image.

**Content-Type:** `multipart/form-data`

**Body:**
- `image` (File): Document image (JPG, PNG, PDF)

**Réponse:**
```json
{
  "text": "Texte extrait du document...",
  "confidence": 0.95,
  "status": "success"
}
```

**Exemple JavaScript:**
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

const response = await fetch('/api/ocr/extract', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.text);
```

---

### 🎤 **Speech (Reconnaissance vocale)**

#### `GET /api/speech/languages`
Obtenir les langues supportées.

**Réponse:**
```json
{
  "languages": {
    "ar-SA": "العربية (السعودية)",
    "ar-EG": "العربية (مصر)",
    "ar-MA": "العربية (المغرب)",
    "ar-AE": "العربية (الإمارات)",
    "fr-FR": "Français (France)",
    "fr-MA": "Français (Maroc)"
  },
  "status": "success"
}
```

#### `POST /api/speech-to-text`
Convertir audio en texte seulement.

**Content-Type:** `multipart/form-data`

**Body:**
- `audio` (File): Fichier audio (WAV, MP3, OGG, WebM, M4A, FLAC)
- `language` (Text, optionnel): Code langue (défaut: `ar-SA`)

**Réponse:**
```json
{
  "text": "مرحبا، أريد معرفة حالة خدمتي",
  "language": "ar-MA",
  "status": "success"
}
```

**Exemple JavaScript:**
```javascript
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.wav');
formData.append('language', 'ar-MA');

const response = await fetch('/api/speech-to-text', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log('Transcription:', data.text);
```

#### `POST /api/speech-to-chat`
Convertir audio en texte ET envoyer au chat (tout en un).

**Content-Type:** `multipart/form-data`

**Body (nouveau message):**
- `audio` (File): Fichier audio
- `language` (Text, optionnel): Code langue

**Body (continuer conversation):**
- `audio` (File): Fichier audio
- `conversation_id` (Text): ID de la conversation
- `language` (Text, optionnel): Code langue

**Réponse:**
```json
{
  "transcribed_text": "مرحبا",
  "response": "مرحبا بك! كيف يمكنني مساعدتك اليوم؟",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_new_conversation": true,
  "language": "ar-MA",
  "status": "success"
}
```

**Exemple JavaScript:**
```javascript
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.wav');
formData.append('language', 'ar-MA');

// Si conversation existante
if (conversationId) {
  formData.append('conversation_id', conversationId);
}

const response = await fetch('/api/speech-to-chat', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log('Transcription:', data.transcribed_text);
console.log('Réponse:', data.response);
console.log('Conversation ID:', data.conversation_id);
```

---

## 🔄 Flux de Conversation

### Scénario 1 : Chat textuel

```javascript
// 1. Premier message
let response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: "مرحبا" })
});
let data = await response.json();
const conversationId = data.conversation_id; // Sauvegarder !

// 2. Messages suivants
response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "رقم CIL الخاص بي هو: 1071324-101",
    conversation_id: conversationId
  })
});
```

### Scénario 2 : Chat vocal

```javascript
// 1. Premier audio
const formData1 = new FormData();
formData1.append('audio', audioBlob1);
formData1.append('language', 'ar-MA');

let response = await fetch('/api/speech-to-chat', {
  method: 'POST',
  body: formData1
});
let data = await response.json();
const conversationId = data.conversation_id; // Sauvegarder !

// 2. Audios suivants
const formData2 = new FormData();
formData2.append('audio', audioBlob2);
formData2.append('conversation_id', conversationId);

response = await fetch('/api/speech-to-chat', {
  method: 'POST',
  body: formData2
});
```

### Scénario 3 : Mixte (audio + texte)

```javascript
// 1. Commencer avec audio
const formData = new FormData();
formData.append('audio', audioBlob);
let response = await fetch('/api/speech-to-chat', {
  method: 'POST',
  body: formData
});
let data = await response.json();
const conversationId = data.conversation_id;

// 2. Continuer avec texte
response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "شكراً",
    conversation_id: conversationId
  })
});
```

---

## ⚠️ Gestion des Erreurs

Toutes les erreurs retournent un JSON avec `error` et `error_ar`:

```json
{
  "error": "Missing required field: message",
  "error_ar": "الرجاء تقديم رسالة"
}
```

**Codes HTTP:**
- `200`: Succès
- `400`: Erreur de requête (champs manquants, format incorrect)
- `404`: Ressource non trouvée (conversation_id invalide)
- `500`: Erreur serveur

**Exemple de gestion:**
```javascript
try {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userMessage })
  });
  
  const data = await response.json();
  
  if (!response.ok) {
    // Afficher l'erreur en arabe
    console.error(data.error_ar || data.error);
    return;
  }
  
  // Succès
  displayMessage(data.response);
  
} catch (error) {
  console.error('Network error:', error);
}
```

---

## 🧪 Tests Postman

### Ordre de test recommandé:

1. ✅ **Health Check** - Vérifier que le serveur fonctionne
2. ✅ **Get Languages** - Voir les langues disponibles
3. ✅ **Send Message (New)** - Créer une conversation
4. ✅ **Send Message (Continue)** - Continuer la conversation
5. ✅ **Get History** - Voir l'historique
6. ✅ **Speech to Text** - Tester la transcription
7. ✅ **Speech to Chat (New)** - Tester le flux vocal complet
8. ✅ **OCR Extract** - Tester l'extraction de documents

### Scripts automatiques

La collection inclut des scripts Postman qui :
- Sauvegardent automatiquement le `conversation_id`
- Réutilisent le `conversation_id` dans les requêtes suivantes
- Affichent les logs dans la console Postman

---

## 📱 Intégration Frontend

### React Example

```jsx
import { useState } from 'react';

function ChatComponent() {
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);

  const sendMessage = async (message) => {
    const payload = { message };
    if (conversationId) {
      payload.conversation_id = conversationId;
    }

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    
    if (!conversationId) {
      setConversationId(data.conversation_id);
    }

    setMessages([...messages, 
      { role: 'user', content: message },
      { role: 'assistant', content: data.response }
    ]);
  };

  return (
    <div>
      {/* UI du chat */}
    </div>
  );
}
```

### Vue Example

```vue
<script setup>
import { ref } from 'vue';

const conversationId = ref(null);
const messages = ref([]);

async function sendMessage(message) {
  const payload = { message };
  if (conversationId.value) {
    payload.conversation_id = conversationId.value;
  }

  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  
  if (!conversationId.value) {
    conversationId.value = data.conversation_id;
  }

  messages.value.push(
    { role: 'user', content: message },
    { role: 'assistant', content: data.response }
  );
}
</script>
```

---

## 🔧 Configuration Backend

Assurez-vous que le fichier `.env` contient:

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Azure Document Intelligence (OCR)
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_endpoint
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_key

# Azure Speech
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=francecentral
```

---

## 📞 Support

Pour toute question sur les APIs :
- Consulter la collection Postman
- Vérifier les logs du serveur backend
- Tester avec les exemples fournis

**URL de test:** http://localhost:5000/api/health
