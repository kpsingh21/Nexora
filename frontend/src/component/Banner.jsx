import React, { useState } from 'react';

function Banner() {
 
  const handleSubmit = async () => {
    if (!text.trim()) {
      return;
    }

    try {
      const res = await fetch('http://localhost:8000/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          msg: text,
        }),
      });

      const data = await res.json();

      console.log(data.received_message);

      setResponse(data);

    } catch (error) {
      console.error('Error:', error);
      setResponse('error');

    }
  };




  return (
    <div>
      <p></p>
    </div>
  );
}

export default Banner;
