import React from 'react';
import { cn } from '../../lib/utils';
import { motion, HTMLMotionProps } from 'framer-motion';

interface ButtonProps extends HTMLMotionProps<"button"> {
  variant?: 'primary' | 'secondary' | 'accent' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', isLoading, children, ...props }, ref) => {
    
    const variants = {
      primary: 'bg-srm-blue text-white hover:bg-srm-blue/90',
      secondary: 'bg-srm-green text-white hover:bg-srm-green/90',
      accent: 'bg-srm-orange text-white hover:bg-srm-orange/90',
      outline: 'bg-srm-bg text-srm-black hover:bg-gray-100',
    };

    const sizes = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-6 py-3 text-base',
      lg: 'px-8 py-4 text-lg',
    };

    return (
      <motion.button
        ref={ref}
        whileHover={{ x: 2, y: 2, boxShadow: '2px 2px 0px 0px #1A1A1A' }}
        whileTap={{ x: 4, y: 4, boxShadow: '0px 0px 0px 0px #1A1A1A' }}
        className={cn(
          'relative font-bold border-3 border-srm-black shadow-neo transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed',
          variants[variant],
          sizes[size],
          className
        )}
        disabled={isLoading || props.disabled}
        {...props}
      >
        {isLoading && (
          <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
        )}
        {children as React.ReactNode}
      </motion.button>
    );
  }
);

Button.displayName = 'Button';

export { Button };
