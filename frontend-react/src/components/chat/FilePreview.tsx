import React from 'react';
import { motion } from 'framer-motion';
import { X, FileText, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { FileAttachment } from '../../types';
import { useLanguage } from '../../contexts/LanguageContext';

interface FilePreviewProps {
  attachment: FileAttachment;
  onRemove: (id: string) => void;
}

export const FilePreview: React.FC<FilePreviewProps> = ({ attachment, onRemove }) => {
  const { t } = useLanguage();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="relative group w-20 h-20 bg-srm-gray-100 rounded-xl border border-srm-gray-200 overflow-hidden flex items-center justify-center flex-shrink-0"
    >
      {attachment.type === 'image' ? (
        <img 
          src={attachment.previewUrl} 
          alt="Preview" 
          className="w-full h-full object-cover"
        />
      ) : (
        <FileText className="w-8 h-8 text-srm-gray-800" />
      )}

      {/* Status Overlay */}
      <div className="absolute inset-0 bg-black/10 flex items-center justify-center">
        {attachment.uploadStatus === 'uploading' && (
          <div className="bg-white/80 p-1 rounded-full backdrop-blur-sm">
            <Loader2 className="w-4 h-4 animate-spin text-srm-teal" />
          </div>
        )}
        {attachment.uploadStatus === 'success' && (
          <div className="absolute top-1 right-1 bg-green-500 text-white rounded-full p-0.5">
            <CheckCircle className="w-3 h-3" />
          </div>
        )}
        {attachment.uploadStatus === 'error' && (
          <div className="absolute top-1 right-1 bg-red-500 text-white rounded-full p-0.5">
            <AlertCircle className="w-3 h-3" />
          </div>
        )}
      </div>

      {/* Remove Button */}
      <button
        onClick={() => onRemove(attachment.id)}
        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-md opacity-0 group-hover:opacity-100 transition-opacity transform hover:scale-110"
        title={t.file_preview_remove}
      >
        <X className="w-3 h-3" />
      </button>
    </motion.div>
  );
};

