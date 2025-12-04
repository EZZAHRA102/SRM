import React from 'react';
import { cn } from '../../lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <div className="w-full">
        <input
          ref={ref}
          className={cn(
            'w-full bg-white border-3 border-srm-black p-3 text-srm-black placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-srm-blue/50 transition-all',
            error && 'border-red-500',
            className
          )}
          {...props}
        />
        {error && (
          <p className="mt-1 text-red-500 text-sm font-bold">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };

