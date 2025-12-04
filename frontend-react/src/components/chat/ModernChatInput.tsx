import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Paperclip, Loader2 } from 'lucide-react';
import { useChatStore } from '../../store/chatStore';
import { useLanguage } from '../../contexts/LanguageContext';
import { FilePreview } from './FilePreview';
import { cn } from '../../lib/utils';

interface ChatInputProps {
  isLoading?: boolean;
}

export const ModernChatInput: React.FC<ChatInputProps> = ({ isLoading }) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const { sendMessage, addAttachment, removeAttachment, activeAttachments, isUploading } = useChatStore();
  const { t, direction } = useLanguage();

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if ((!input.trim() && activeAttachments.length === 0) || isLoading || isUploading) return;

    await sendMessage(input);
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 150)}px`;
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      await addAttachment(e.target.files[0]);
    }
    // Reset input so same file can be selected again if needed
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="w-full relative z-20">
      {/* Attachments Area */}
      <AnimatePresence>
        {activeAttachments.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10, height: 0 }}
            animate={{ opacity: 1, y: 0, height: 'auto' }}
            exit={{ opacity: 0, y: 10, height: 0 }}
            className="flex gap-2 mb-2 overflow-x-auto pb-2 px-1"
          >
            {activeAttachments.map(att => (
              <FilePreview key={att.id} attachment={att} onRemove={removeAttachment} />
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      <form 
        onSubmit={handleSend}
        className={cn(
          "relative flex items-end gap-2 p-2 rounded-[24px] bg-white shadow-lg border border-white/20 transition-all duration-300",
          "focus-within:ring-2 focus-within:ring-srm-teal/20 focus-within:shadow-xl"
        )}
      >
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="p-3 text-srm-gray-800 hover:bg-srm-gray-100 rounded-full transition-colors flex-shrink-0"
          title={t.upload_file}
        >
          <Paperclip className="w-5 h-5" />
          <input 
            type="file" 
            ref={fileInputRef} 
            className="hidden" 
            onChange={handleFileChange}
            accept="image/*,.pdf"
          />
        </button>

        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder={t.input_placeholder}
          rows={1}
          disabled={isLoading || isUploading}
          dir={direction}
          className="flex-1 max-h-[150px] py-3 px-2 bg-transparent resize-none outline-none text-srm-gray-900 placeholder:text-gray-400 font-sans text-base leading-relaxed scrollbar-thin"
        />

        <button
          type="submit"
          disabled={(!input.trim() && activeAttachments.length === 0) || isLoading || isUploading}
          className={cn(
            "p-3 rounded-full transition-all duration-300 flex-shrink-0 flex items-center justify-center",
            (!input.trim() && activeAttachments.length === 0) || isLoading || isUploading
              ? "bg-gray-100 text-gray-400 cursor-not-allowed" 
              : "bg-srm-teal text-white shadow-md hover:bg-srm-teal-light hover:shadow-lg hover:scale-105 active:scale-95"
          )}
        >
          {isLoading || isUploading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <Send className={cn("w-5 h-5", direction === 'rtl' ? "rotate-180" : "")} />
          )}
        </button>
      </form>
    </div>
  );
};

