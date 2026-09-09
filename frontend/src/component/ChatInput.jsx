import React, { useState } from 'react';

function ChatInput() {
  const [text, setText] = useState('');
  const [response, setResponse] = useState('');

  const handleChange = (event) => {
    setText(event.target.value);
  };

  const handleSubmit = async () => {
    if (!text.trim()) {
      return;
    }

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          msg: text,
        }),
      });

      const data = await res.json();

      console.log(data.received_message.messages.content);

      // Only store the content
      setResponse(data.received_message.messages.content);

    } catch (error) {
      console.error('Error:', error);
      setResponse('Error occurred');
    }
  };

  return (
    <>
      <input
        type="text"
        value={text}
        onChange={handleChange}
        placeholder="Ask anything?"
      />

      <button onClick={handleSubmit}>
        Send
      </button>

      <div>
        {response}
      </div>
    </>
  );
}
export default ChatInput;
