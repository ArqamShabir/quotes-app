import React, { useEffect, useState } from 'react';
import next from './Vector.png';

function Main({theme}) {

    const[backgroundColor,setBackgroundColor] = useState('#E5E7EB');
    const[color,setColor] = useState('#111827');
    const [quote, setQuote] = useState('');
    const [author, setAuthor] = useState('');
    const apiKey = process.env.REACT_APP_API_KEY;
    

  const fetchNewQuote = async () => {
    try {
      const response = await fetch('https://api.api-ninjas.com/v1/quotes?category=life', {
        headers: {
          'x-api-key': apiKey,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch quote - Status: ${response.status}`);
      }

      const data = await response.json();
      if (data.length > 0) {
        setQuote(data[0].quote);
        setAuthor(data[0].author);
      } else {
        setQuote('No quotes available');
        setAuthor('Try Next Time :)')
      }
    } catch (error) {
      console.error('Error fetching quote:', error.message);
    }
  };

    useEffect(() => {
        fetchNewQuote();
      }, [apiKey]);    


    useEffect(()=>{
        if(theme == 'dark')
    {
        setBackgroundColor('#1F2937');
        setColor('#fff')
    }
    else{
        setBackgroundColor('#E5E7EB');
        setColor('#111827')
    }
    },[theme])

  return (
    <div className='main'>
        <div className='main_cntr' >
            <div className='main_up' style={{backgroundColor,color}}>
                <h2>{quote}</h2>
                <p>{author}</p>
            </div>
            <div className='main_btn' onClick={fetchNewQuote}>
                <img src={next} />
            </div>
        </div>
    </div>
  )
}

export default Main