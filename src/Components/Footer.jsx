import React, { useEffect, useState } from 'react'
import github from './github.png'
import github2 from './gw.png'
import twitter2 from './tw.png'
import twitter from './twitter.png'

function Footer({theme}) {

    const [color,setColor] = useState('#111827');
    const [image1,setimage1] = useState(github);
    const [image2,setimage2] = useState(twitter);

    useEffect(()=>{
        if(theme == 'dark')
        {
            setColor('#fff');
            setimage1(github2);
            setimage2(twitter2);
        }else{
            setColor('#111827');
            setimage1(github);
            setimage2(twitter);
        }
    },[theme]);


  return (
    <div className='footer' style={{color}}>
        <h5>Created by Muhammad Arqam</h5>
        <div className="icon">
            <img src={image1} />
            <img src={image2} />
        </div>
    </div>
  )
}

export default Footer