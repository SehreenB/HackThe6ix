import React from 'react';

const Logo = ({ size = 32 }) => (
  <div className="flex items-center select-none">
    <img 
      src="/logo_v2.png" 
      alt="Apogee Solutions" 
      style={{ height: size, width: 'auto' }}
      className="object-contain"
    />
  </div>
);

export default Logo;
