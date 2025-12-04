import React from 'react';
import { motion } from 'framer-motion';
import { LanguageToggle } from '../common/LanguageToggle';
import { Logo } from '../common/Logo';
import { useLanguage } from '../../contexts/LanguageContext';
import { useChatStore } from '../../store/chatStore';

interface ModernLayoutProps {
  children: React.ReactNode;
}

export const ModernLayout: React.FC<ModernLayoutProps> = ({ children }) => {
  const { direction } = useLanguage();
  const { clearHistory } = useChatStore();

  const handleLogoClick = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    clearHistory();
  };

  return (
    <div 
      className="min-h-screen bg-srm-gray-50 flex flex-col font-sans relative overflow-hidden"
      dir={direction}
    >
      {/* Background Decorative Elements */}
      <div className="fixed top-0 left-0 w-full h-96 bg-gradient-to-b from-srm-teal/5 to-transparent -z-10" />
      <div className="fixed -top-40 -right-40 w-96 h-96 bg-srm-blue/5 rounded-full blur-3xl -z-10" />
      <div className="fixed top-20 -left-20 w-72 h-72 bg-srm-teal/5 rounded-full blur-3xl -z-10" />

      {/* Header */}
      <header className="sticky top-0 z-30 w-full px-6 py-4 flex items-center justify-between glass-panel border-b border-white/20">
        <motion.button
          onClick={handleLogoClick}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 cursor-pointer transition-opacity hover:opacity-80"
          aria-label="Return to main page"
        >
          <Logo className="h-10" variant="header" />
        </motion.button>
        <LanguageToggle />
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative max-w-5xl mx-auto w-full p-4 md:p-6 h-[calc(100vh-80px)]">
        {children}
      </main>
    </div>
  );
};

