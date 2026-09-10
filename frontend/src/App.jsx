import ChatInput from './component/ChatInput'
import Sidebar from './component/Sidebar/Sidebar'
import Loadcon  from './component/Chatwindow/Loadcon'
import { useState } from 'react';


function App() {
  const [selectedThreadId, setSelectedThreadId] = useState();
  const [threadId, setgenthreadId] = useState();


  return (
    <>
      <section id="center">
        <h1>Welcome to Nexora!</h1>
        <p>Next-generation AI assistant</p>
        <Sidebar  onSelectChat={setSelectedThreadId} onNewchat={setgenthreadId}/>
        <Loadcon thread_id ={selectedThreadId}/>
        <ChatInput thread_id={threadId}/>  
      </section>
    </>
  )
}

export default App
