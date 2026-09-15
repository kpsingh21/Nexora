import ChatInput from './component/ChatInput'
import Sidebar from './component/Sidebar/Sidebar'
import Loadcon  from './component/Chatwindow/Loadcon'
import { useState } from 'react';


function App() {
  const [selectedThreadId, setSelectedThreadId] = useState();
  const [threadId, setgenthreadId] = useState();
  const [messages, setMessages] = useState([]);



  return (
    <>
      <section id="center">
        <h1>Welcome to Nexora!</h1>
        <p>Next-generation AI assistant</p>
        <Sidebar  onSelectChat={setSelectedThreadId} Newthreadid={setgenthreadId} onNewchat={setgenthreadId} onNewchatClick={setMessages}/>
        <Loadcon thread_id ={selectedThreadId} messages={messages} setMsg={setMessages}/>
        <ChatInput thread_id={threadId}/>  
      </section>
    </>
  )
}

export default App
