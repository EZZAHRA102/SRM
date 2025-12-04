# Guide d'Utilisation - Azure Speech to Text API

Ce guide explique comment utiliser les nouveaux endpoints de reconnaissance vocale.

## 📋 Configuration Requise

### 1. Ajouter les clés Azure Speech dans `.env`

```env
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=francecentral
```

### 2. Installer les dépendances

```powershell
pip install -r requirements.txt
```

## 🎤 Endpoints Disponibles

### 1. `/api/speech/languages` (GET)
Obtenir la liste des langues supportées.

**Requête :**
```powershell
curl http://localhost:5000/api/speech/languages
```

**Réponse :**
```json
{
  "languages": {
    "ar-SA": "العربية (السعودية)",
    "ar-EG": "العربية (مصر)",
    "ar-MA": "العربية (المغرب)",
    "fr-FR": "Français (France)"
  },
  "status": "success"
}
```

### 2. `/api/speech-to-text` (POST)
Convertir un fichier audio en texte uniquement.

**Formats audio supportés :** WAV, MP3, OGG, WebM, M4A, FLAC

**Requête :**
```powershell
# Avec langue par défaut (ar-SA)
curl -X POST http://localhost:5000/api/speech-to-text `
  -F "audio=@recording.wav"

# Avec langue spécifique
curl -X POST http://localhost:5000/api/speech-to-text `
  -F "audio=@recording.wav" `
  -F "language=ar-MA"
```

**Réponse :**
```json
{
  "text": "مرحبا، أريد معرفة حالة خدمتي",
  "language": "ar-SA",
  "status": "success"
}
```

### 3. `/api/speech-to-chat` (POST)
Convertir audio en texte ET envoyer directement au chat agent.

**Requête :**
```powershell
# Premier message (nouvelle conversation)
curl -X POST http://localhost:5000/api/speech-to-chat `
  -F "audio=@recording.wav" `
  -F "language=ar-MA"

# Message suivant (conversation existante)
curl -X POST http://localhost:5000/api/speech-to-chat `
  -F "audio=@recording2.wav" `
  -F "conversation_id=550e8400-e29b-41d4-a716-446655440000"
```

**Réponse :**
```json
{
  "transcribed_text": "رقم CIL الخاص بي هو: 1071324-101",
  "response": "شكراً لتقديم رقم CIL الخاص بك...",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "is_new_conversation": false,
  "language": "ar-MA",
  "status": "success"
}
```

## 🧪 Tests avec PowerShell

### Test 1 : Transcription simple
```powershell
# Créer un fichier audio de test (ou utiliser un existant)
$audioFile = "test_audio.wav"

# Envoyer pour transcription
$response = Invoke-RestMethod -Uri "http://localhost:5000/api/speech-to-text" `
  -Method POST `
  -Form @{
    audio = Get-Item $audioFile
    language = "ar-MA"
  }

Write-Host "Texte transcrit: $($response.text)"
```

### Test 2 : Audio vers chat (flux complet)
```powershell
# 1. Premier audio - crée une conversation
$response1 = Invoke-RestMethod -Uri "http://localhost:5000/api/speech-to-chat" `
  -Method POST `
  -Form @{
    audio = Get-Item "message1.wav"
    language = "ar-MA"
  }

$convId = $response1.conversation_id
Write-Host "Conversation créée: $convId"
Write-Host "Transcrit: $($response1.transcribed_text)"
Write-Host "Réponse: $($response1.response)"

# 2. Deuxième audio - continue la conversation
$response2 = Invoke-RestMethod -Uri "http://localhost:5000/api/speech-to-chat" `
  -Method POST `
  -Form @{
    audio = Get-Item "message2.wav"
    conversation_id = $convId
  }

Write-Host "Transcrit: $($response2.transcribed_text)"
Write-Host "Réponse: $($response2.response)"
```

### Test 3 : Avec fetch JavaScript (Frontend)
```javascript
async function sendAudioMessage(audioBlob, conversationId = null) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.wav');
  formData.append('language', 'ar-MA');
  
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
  
  return data;
}
```

## 🎯 Cas d'Usage

### Scénario 1 : Transcription seulement
```powershell
# Utilisateur enregistre un audio
# → Envoie à /api/speech-to-text
# → Reçoit le texte transcrit
# → Peut éditer le texte avant de l'envoyer au chat
```

### Scénario 2 : Flux vocal direct
```powershell
# Utilisateur enregistre un audio
# → Envoie à /api/speech-to-chat
# → Transcription + traitement par l'agent en une seule requête
# → Reçoit la réponse directement
```

## 📝 Notes Importantes

1. **Langues supportées** : L'arabe marocain (`ar-MA`) est recommandé pour le Maroc
2. **Formats audio** : WAV est le plus fiable, mais MP3, OGG, WebM, M4A et FLAC sont aussi supportés
3. **Taille maximale** : 16MB (configuré dans app.py)
4. **Nettoyage** : Les fichiers audio sont automatiquement supprimés après traitement
5. **Conversation** : Le `conversation_id` est géré de la même façon que l'endpoint `/api/chat`

## ⚠️ Gestion des Erreurs

**Erreur : "Azure Speech credentials not configured"**
→ Vérifier que `AZURE_SPEECH_KEY` et `AZURE_SPEECH_REGION` sont dans `.env`

**Erreur : "No speech detected"**
→ L'audio est vide ou de mauvaise qualité

**Erreur : "File type not allowed"**
→ Utiliser un format supporté (WAV, MP3, OGG, WebM, M4A, FLAC)

## 🚀 Démarrage

```powershell
# 1. Configurer .env
# 2. Installer dépendances
pip install -r requirements.txt

# 3. Démarrer le serveur
cd backend
python app.py

# 4. Tester
curl http://localhost:5000/api/speech/languages
```
