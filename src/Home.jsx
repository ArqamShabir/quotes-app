import React, { useState } from 'react';
import Footer from './Components/Footer';
import Main from './Components/Main';
import Navbar from './Components/Navbar';

function Home() {

    const [theme,settheme] = useState("light");

  return (
    <>
       <div className='home'>
       <Navbar theme={settheme}/>
        <Main theme={theme}/>
        <Footer theme={theme}/>
       </div>
    </>
  )
}

export default Home