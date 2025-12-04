import React from 'react';
import { motion } from 'framer-motion';
import { User, FileText } from 'lucide-react';
import { ChatMessage } from '../../types';
import { cn } from '../../lib/utils';
import { useLanguage } from '../../contexts/LanguageContext';
import { Logo } from '../common/Logo';

interface ModernChatMessageProps {
  message: ChatMessage;
}

export const ModernChatMessage: React.FC<ModernChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const { direction } = useLanguage();

  return (
    <motion.div
      initial={{ opacity: 0, y: 10, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ type: 'spring', stiffness: 200, damping: 20 }}
      className={cn(
        "flex w-full mb-6",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div className={cn(
        "flex max-w-[85%] md:max-w-[75%] gap-3",
        isUser ? "flex-row-reverse" : "flex-row"
      )}>
        {/* Avatar */}
        <div className={cn(
          "w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-sm mt-auto mb-1",
          isUser ? "bg-gradient-to-br from-srm-blue to-srm-blue-light" : "bg-white border border-gray-100"
        )}>
          {isUser ? (
            <User className="text-white w-4 h-4" />
          ) : (
            <Logo variant="center" className="w-full h-full object-contain" />
          )}
        </div>

        <div className="flex flex-col gap-1">
           {/* Message Bubble */}
          <div className={cn(
            "px-5 py-3.5 text-[15px] leading-relaxed shadow-sm rounded-2xl",
            "whitespace-pre-wrap",
            isUser ? "message-bubble-user" : "message-bubble-assistant"
          )}>
            <div dir={direction === 'rtl' ? 'rtl' : 'ltr'} className={cn(
              "text-right", // Default to right alignment for Arabic content usually, but dynamic is better
              direction === 'ltr' && "text-left"
            )}>
              {message.content}
            </div>
          </div>

          {/* Attachments Display in History */}
          {message.attachments && message.attachments.length > 0 && (
            <div className={cn(
              "flex flex-wrap gap-2 mt-1",
              isUser ? "justify-end" : "justify-start"
            )}>
              {message.attachments.map((att, idx) => (
                <div key={idx} className="relative w-16 h-16 rounded-lg overflow-hidden border border-white/20 shadow-sm">
                  {att.type === 'image' ? (
                    <img src={att.previewUrl} alt="Attachment" className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-full h-full bg-gray-100 flex items-center justify-center">
                      <FileText className="w-6 h-6 text-gray-500" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

