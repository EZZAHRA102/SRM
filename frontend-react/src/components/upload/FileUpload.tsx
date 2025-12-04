import React, { useCallback, useState } from 'react';
import { Upload, X, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '../common/Button';
import { cn } from '../../lib/utils';
import { srmApi } from '../../services/api';
import { useChatStore } from '../../store/chatStore';

export const FileUpload: React.FC = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  
  const { sendMessage } = useChatStore();

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (selectedFile: File) => {
    // Reset states
    setError(null);
    setSuccess(false);

    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
    if (!validTypes.includes(selectedFile.type)) {
      setError('يرجى تحميل صورة (JPG, PNG) أو ملف PDF');
      return;
    }

    // Validate file size (max 5MB)
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError('حجم الملف يجب ألا يتجاوز 5 ميجابايت');
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsLoading(true);
    setError(null);

    try {
      const result = await srmApi.extractCil(file);
      
      if (result.success && result.data.cil) {
        setSuccess(true);
        // Automatically send CIL to chat
        await sendMessage(`رقم CIL الخاص بي هو: ${result.data.cil}`);
        
        // Reset after short delay
        setTimeout(() => {
           setFile(null);
           setSuccess(false);
        }, 3000);

      } else {
        setError('لم نتمكن من استخراج رقم CIL. يرجى المحاولة بصورة أوضح.');
      }
    } catch (err) {
      setError('حدث خطأ أثناء تحليل الملف. يرجى المحاولة مرة أخرى.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const removeFile = () => {
    setFile(null);
    setError(null);
    setSuccess(false);
  };

  return (
    <div className="w-full">
      {!file ? (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={cn(
            "border-3 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors relative",
            isDragging 
              ? "border-srm-blue bg-srm-blue/10" 
              : "border-gray-300 hover:border-srm-black bg-gray-50"
          )}
        >
          <input
            type="file"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={handleFileChange}
            accept=".jpg,.jpeg,.png,.pdf"
          />
          <Upload className="w-8 h-8 mx-auto mb-2 text-gray-400" />
          <p className="text-sm font-bold text-gray-600 mb-1">
            اضغط للتحميل أو اسحب الملف هنا
          </p>
          <p className="text-xs text-gray-500">
            JPG, PNG, PDF (Max 5MB)
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          <div className="bg-gray-50 border-2 border-srm-black p-3 flex items-center justify-between rounded-lg">
            <div className="flex items-center gap-2 overflow-hidden">
              <FileText className="w-5 h-5 text-srm-blue shrink-0" />
              <span className="text-sm truncate font-medium max-w-[150px]" dir="ltr">
                {file.name}
              </span>
            </div>
            <button 
              onClick={removeFile}
              className="p-1 hover:bg-gray-200 rounded-full transition-colors"
              disabled={isLoading}
            >
              <X className="w-4 h-4 text-gray-500" />
            </button>
          </div>

          {error && (
            <div className="flex items-center gap-2 text-red-600 text-xs font-bold bg-red-50 p-2 border-2 border-red-200 rounded" dir="rtl">
              <AlertCircle className="w-4 h-4 shrink-0" />
              {error}
            </div>
          )}

          {success && (
             <div className="flex items-center gap-2 text-green-700 text-xs font-bold bg-green-50 p-2 border-2 border-green-200 rounded" dir="rtl">
               <CheckCircle className="w-4 h-4 shrink-0" />
               تم استخراج الرقم بنجاح!
             </div>
          )}

          <Button
            onClick={handleUpload}
            variant="primary"
            size="sm"
            className="w-full"
            isLoading={isLoading}
            disabled={success}
          >
            {success ? 'تم الإرسال' : 'تحليل واستخراج CIL'}
          </Button>
        </div>
      )}
    </div>
  );
};
