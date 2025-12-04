import React from 'react';
import { motion } from 'framer-motion';
import { useLanguage } from '../../contexts/LanguageContext';
import { Globe } from 'lucide-react';

export const LanguageToggle: React.FC = () => {
  const { language, toggleLanguage } = useLanguage();

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleLanguage}
      className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/50 backdrop-blur-md border border-white/20 shadow-sm hover:bg-white/80 transition-all text-srm-gray-800 text-sm font-medium"
    >
      <Globe className="w-4 h-4 text-srm-teal" />
      <span>{language === 'ar' ? 'Français' : 'العربية'}</span>
    </motion.button>
  );
};

