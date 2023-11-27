import React, { useState } from 'react';

function Navbar({theme}) {

    const [backgroundColor, setBackgroundColor] = useState('#F0F0F5');
    const [border, setborder] = useState('.5px solid #8F8FA2');
    const [justifyContent,setjustifyContent] = useState('start');
    const [bgColor, setbgColor] = useState('#F9FAFB');
    

    const navbar_btn_func = () => {
        setBackgroundColor((prevColor) => (prevColor === '#F0F0F5' ? '#0069D0' : '#F0F0F5'));
        setborder((prevBorder) => (prevBorder === '.5px solid #8F8FA2' ? 'none' : '.5px solid #8F8FA2'));
        setjustifyContent((prev) => (prev === 'start' ? 'end' : 'start'));
        setbgColor((prev) => (prev === '#F9FAFB' ? '#111827' : '#F9FAFB'));
        theme((prev)=> (prev === 'light' ? 'dark' : 'light'));
      };    

  return (
    <div className='navbar'>
        <div className='navbar_btn' style={{backgroundColor, border,justifyContent}} onClick={navbar_btn_func}>
            <div className='navbar_circle'></div>
        </div>
        <style>
            {`body{background-color: ${bgColor};}`}
        </style>
    </div>
  )
}

export default Navbar