import React from 'react';

const LoremDisplay = ({ text }) => {
  return (
    <div className="lorem-display">
      <p>{text || 'Click generate to create Lorem Ipsum text'}</p>
    </div>
  );
};

export default LoremDisplay;
