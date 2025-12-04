import { create } from 'zustand';
import { ChatMessage, FileAttachment } from '../types';
import { srmApi } from '../services/api';

interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  
  // File Upload State
  activeAttachments: FileAttachment[];
  isUploading: boolean;
  
  // Actions
  addMessage: (message: ChatMessage) => void;
  sendMessage: (content: string) => Promise<void>;
  clearHistory: () => void;
  
  // File Actions
  addAttachment: (file: File) => Promise<void>;
  removeAttachment: (id: string) => void;
  clearAttachments: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isLoading: false,
  error: null,
  activeAttachments: [],
  isUploading: false,

  addMessage: (message) => 
    set((state) => ({ messages: [...state.messages, message] })),

  sendMessage: async (content: string) => {
    const { messages, activeAttachments } = get();
    
    // Process any pending attachments (that haven't been processed yet)
    const attachmentsToProcess = activeAttachments.filter(att => att.uploadStatus === 'pending');
    let finalAttachments = [...activeAttachments];
    
    if (attachmentsToProcess.length > 0) {
      set({ isUploading: true });
      
      // Process each pending attachment
      const processedAttachments = await Promise.all(
        attachmentsToProcess.map(async (att) => {
          try {
            const result = await srmApi.extractBillInfo(att.file);
            return {
              ...att,
              uploadStatus: 'success' as const,
              extractedData: result.data
            };
          } catch (error) {
            console.error('OCR Error:', error);
            return {
              ...att,
              uploadStatus: 'error' as const
            };
          }
        })
      );
      
      // Merge processed attachments with existing ones
      finalAttachments = activeAttachments.map(att => {
        const processed = processedAttachments.find(p => p.id === att.id);
        return processed || att;
      });
      
      // Update state with processed attachments
      set({
        activeAttachments: finalAttachments,
        isUploading: false
      });
    }
    
    // Construct message with attachments if any
    let fullContent = content;
    
    // Append extracted data to the message for the AI context
    if (finalAttachments.length > 0) {
      const extractedInfos = finalAttachments
        .map(att => att.extractedData ? JSON.stringify(att.extractedData, null, 2) : '')
        .filter(info => info !== '')
        .join('\n\n');
        
      if (extractedInfos) {
        fullContent += `\n\n[System Note: User attached file(s) with extracted data:]\n${extractedInfos}`;
      }
    }

    const userMessage: ChatMessage = { 
      role: 'user', 
      content: content, // Display original content to user
      attachments: [...finalAttachments] // Store attachments for display
    };

    set((state) => ({ 
      messages: [...state.messages, userMessage], 
      isLoading: true, 
      error: null,
      activeAttachments: [] // Clear attachments after sending
    }));

    try {
      // Get current language from localStorage (same source as LanguageContext)
      const currentLanguage = (localStorage.getItem('srm-language') || 'ar') as 'ar' | 'fr';
      
      const response = await srmApi.chat({
        message: fullContent, // Send enriched content to AI
        history: messages.map(m => ({ role: m.role, content: m.content })), // Send history without attachment objects (clean for backend)
        language: currentLanguage,
      });

      const assistantMessage: ChatMessage = { 
        role: 'assistant', 
        content: response.response 
      };

      set((state) => ({ 
        messages: [...state.messages, assistantMessage], 
        isLoading: false 
      }));
    } catch (error) {
      console.error('Chat error:', error);
      set({ 
        isLoading: false, 
        error: 'Failed to send message. Please try again.' 
      });
    }
  },

  clearHistory: () => set({ messages: [], error: null }),

  addAttachment: async (file: File) => {
    const id = Math.random().toString(36).substring(7);
    const previewUrl = URL.createObjectURL(file);
    
    const newAttachment: FileAttachment = {
      id,
      file,
      previewUrl,
      type: file.type.startsWith('image/') ? 'image' : 'document',
      uploadStatus: 'pending' // Set to 'pending' instead of 'uploading' - will be processed when user sends message
    };

    // Just store the file locally without processing it yet
    set(state => ({ 
      activeAttachments: [...state.activeAttachments, newAttachment]
    }));
  },

  removeAttachment: (id) => {
    set(state => {
      const attachment = state.activeAttachments.find(a => a.id === id);
      if (attachment?.previewUrl) {
        URL.revokeObjectURL(attachment.previewUrl);
      }
      return {
        activeAttachments: state.activeAttachments.filter(a => a.id !== id)
      };
    });
  },

  clearAttachments: () => {
    set(state => {
      state.activeAttachments.forEach(a => URL.revokeObjectURL(a.previewUrl));
      return { activeAttachments: [] };
    });
  }
}));
