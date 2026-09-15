import React, { useState } from 'react';
// import './Chatwindow/chatinput.css'


function ChatInput({thread_id}) {
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
          thread_id: thread_id
        }),
      });

      const data = await res.json();

      console.log(data);

      console.log(data.received_message);
      console.log(data.received_message.messages);

      console.log(data.received_message.messages[1].content);

      // Only store the content
      // setResponse(data.received_message.messages.content);
      setResponse(data.received_message.messages[1].content);


    } catch (error) {
      console.error('Error:', error);
      setResponse('Error occurred');
    }
  };

  return (
    <>
      {/* <input
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
      </div> */}


              <div className="message-toolbar">

          {/* <button className="tools-btn" type="button">
            <span className="plus-icon">＋</span>
            <span>Tools</span>
          </button>

          <span className="keyboard-hint">
            Enter to send&nbsp;&nbsp;•&nbsp;&nbsp;Shift+Enter for new line
          </span> */}


<div className="response">
        {response}
        </div>

          <input
                  type="text"
                  value={text}
                  className='inputbox'
                  onChange={handleChange}
                  placeholder="Ask anything?"
                />
          <button
            className="send-btn"
            onClick={handleSubmit}
            type="button"
            aria-label="Send message"
          >
            ↑
          </button>

        </div>

       
    </>

    
  );
}
export default ChatInput;
