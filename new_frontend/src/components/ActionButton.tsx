import React from 'react';
import { cn } from '@/lib/utils';

interface ActionButtonProps {
  icon: 'microphone' | 'file';
  title: string;
  description: string;
  onClick: () => void;
  className?: string;
}

export const ActionButton: React.FC<ActionButtonProps> = ({
  icon,
  title,
  description,
  onClick,
  className
}) => {
  const spriteUrl = icon === 'microphone' 
    ? '/microphone-sprite.png'
    : '/file-sprite.png';
    
  const spriteClass = icon === 'microphone' 
    ? 'microphone-sprite' 
    : 'file-sprite';

  return (
    <button
      onClick={onClick}
      className={cn(
        "tech-button action-button",
        "p-8 min-h-[200px] flex flex-col items-center justify-center gap-4",
        "group text-center max-w-sm",
        className
      )}
    >
      <div className="pixel-character">
        <img
          src={spriteUrl}
          alt={icon}
          className={cn("pixel-spritesheet", spriteClass)}
        />
      </div>
      
      <div className="space-y-2">
        <h3 className="text-xl font-semibold text-card-foreground group-hover:text-primary transition-colors">
          {title}
        </h3>
        <p className="text-sm text-muted-foreground leading-relaxed">
          {description}
        </p>
      </div>
    </button>
  );
};