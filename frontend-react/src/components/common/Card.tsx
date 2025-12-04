import React from 'react';
import { cn } from '../../lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  noShadow?: boolean;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, noShadow, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'bg-white border-3 border-srm-black p-6',
          !noShadow && 'shadow-neo',
          className
        )}
        {...props}
      />
    );
  }
);

Card.displayName = 'Card';

export { Card };

