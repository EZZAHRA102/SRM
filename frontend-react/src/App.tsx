import React from 'react';
import { ModernLayout } from './components/layout/ModernLayout';
import { ModernChatContainer } from './components/chat/ModernChatContainer';
import { LanguageProvider } from './contexts/LanguageContext';
import './index.css';

function App() {
  return (
    <LanguageProvider>
      <ModernLayout>
        <ModernChatContainer />
      </ModernLayout>
    </LanguageProvider>
  );
}

export default App;
