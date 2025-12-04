export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  attachments?: FileAttachment[];
}

export interface FileAttachment {
  id: string;
  file: File;
  previewUrl: string;
  type: 'image' | 'document';
  uploadStatus: 'pending' | 'uploading' | 'success' | 'error';
  extractedData?: OCRResult['data'];
}

export interface ChatRequest {
  message: string;
  history: ChatMessage[];
  language: 'ar' | 'fr';
}

export interface ChatResponse {
  response: string;
  tool_calls?: any[];
}

export interface OCRResult {
  success: boolean;
  data: {
    cil?: string;
    customer_name?: string;
    amount?: number;
    due_date?: string;
    service_type?: string;
    consumption?: number;
    [key: string]: any;
  };
  error?: string;
}

export interface HealthCheckResponse {
  status: string;
  service: string;
  version: string;
}
