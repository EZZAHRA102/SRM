import React, { useEffect, useRef } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { useChatStore } from '../../store/chatStore';
import { ModernChatMessage } from './ModernChatMessage';
import { ModernChatInput } from './ModernChatInput';
import { TypingIndicator } from './TypingIndicator';
import { Logo } from '../common/Logo';
import { useLanguage } from '../../contexts/LanguageContext';

export const ModernChatContainer: React.FC = () => {
  const { messages, isLoading, error } = useChatStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { t } = useLanguage();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex flex-col h-full w-full max-w-3xl mx-auto relative">
      <div className="flex-1 overflow-y-auto min-h-0 mb-4 px-2 scrollbar-none space-y-2">
        {messages.length === 0 ? (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="h-full flex flex-col items-center justify-center text-center p-8 mt-10"
          >
            <div className="w-24 h-24 bg-white rounded-3xl shadow-xl flex items-center justify-center mb-8 border border-gray-50">
              <Logo className="h-16 w-16" variant="center" />
            </div>
            <h2 className="text-3xl font-bold text-srm-gray-900 mb-3 tracking-tight">
              {t.welcome_title}
            </h2>
            <p className="text-srm-gray-800 text-lg max-w-md leading-relaxed">
              {t.welcome_subtitle}
            </p>
          </motion.div>
        ) : (
          <div className="py-4">
            <AnimatePresence initial={false}>
              {messages.map((msg, idx) => (
                <ModernChatMessage key={idx} message={msg} />
              ))}
            </AnimatePresence>
            
            {isLoading && (
              <motion.div 
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }} 
                className="flex justify-start w-full mb-6 pl-2"
              >
                 <div className="bg-white border border-srm-gray-100 px-4 py-3 rounded-2xl rounded-tl-none shadow-sm flex items-center gap-2">
                   <TypingIndicator />
                   <span className="text-sm text-gray-400 font-medium">{t.typing_indicator}</span>
                 </div>
              </motion.div>
            )}

            {error && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 text-center text-sm font-medium mx-auto max-w-md my-4"
              >
                {t.error_generic}
              </motion.div>
            )}
            
            <div ref={messagesEndRef} className="h-4" />
          </div>
        )}
      </div>

      <div className="mt-auto pb-2">
        <ModernChatInput isLoading={isLoading} />
        <div className="text-center mt-4">
        </div>
      </div>
    </div>
  );
};

