export type Language = 'ar' | 'fr';

export interface Translations {
  welcome_title: string;
  welcome_subtitle: string;
  input_placeholder: string;
  send_button: string;
  upload_file: string;
  processing_file: string;
  error_generic: string;
  error_file_upload: string;
  language_toggle: string;
  typing_indicator: string;
  file_preview_remove: string;
  cil_label: string;
  bill_label: string;
}

export const translations: Record<Language, Translations> = {
  ar: {
    welcome_title: "مرحباً بك في خدمة عملاء SRM",
    welcome_subtitle: "أنا هنا لمساعدتك في استفسارات الفواتير، الصيانة، وخدمات الماء والكهرباء.",
    input_placeholder: "كيف يمكنني مساعدتك اليوم؟",
    send_button: "إرسال",
    upload_file: "إرفاق ملف",
    processing_file: "جاري معالجة الملف...",
    error_generic: "عذراً، حدث خطأ ما. يرجى المحاولة مرة أخرى.",
    error_file_upload: "فشل تحميل الملف.",
    language_toggle: "English", // Keeping toggle name in opposite language or generic
    typing_indicator: "جاري الكتابة",
    file_preview_remove: "إزالة",
    cil_label: "استخراج رقم CIL",
    bill_label: "استخراج بيانات الفاتورة"
  },
  fr: {
    welcome_title: "Bienvenue au service client SRM",
    welcome_subtitle: "Je suis là pour vous aider avec vos factures, la maintenance et les services d'eau et d'électricité.",
    input_placeholder: "Comment puis-je vous aider aujourd'hui ?",
    send_button: "Envoyer",
    upload_file: "Joindre un fichier",
    processing_file: "Traitement du fichier...",
    error_generic: "Désolé, une erreur s'est produite. Veuillez réessayer.",
    error_file_upload: "Échec du téléchargement du fichier.",
    language_toggle: "العربية",
    typing_indicator: "En train d'écrire",
    file_preview_remove: "Supprimer",
    cil_label: "Extraire CIL",
    bill_label: "Extraire données facture"
  }
};

