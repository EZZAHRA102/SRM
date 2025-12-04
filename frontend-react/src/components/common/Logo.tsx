import React from 'react';

interface LogoProps {
  className?: string;
  variant?: 'header' | 'center';
}

export const Logo: React.FC<LogoProps> = ({ className = "h-12", variant = 'center' }) => {
  const logoSrc = variant === 'header' ? '/srm_logo.png' : '/center_logo.jpeg';
  
  return (
    <img 
      src={logoSrc} 
      alt="SRM Logo" 
      className={`object-contain ${className}`}
    />
  );
};

