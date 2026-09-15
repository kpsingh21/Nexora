
import "./sidebar.css";
import React, { useEffect, useState } from "react";

function Sidebar({ onSelectChat, onNewchat , onNewchatClick,Newthreadid}) {
  const [threads, setThreads] = useState([]);

  useEffect(() => {
    const loadThreads = async () => {
      try {
        const response = await fetch(
          "http://localhost:8000/retrive_all_threads",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();

        console.log("Threads:", data);

        // API response:
        // ["sds", "ddwdw"]
        setThreads(data);
      } catch (error) {
        console.error("Error loading threads:", error);
        setThreads([]);
      }
    };

    loadThreads();
  }, []);

  function generateThreadId() {
    const threadId = crypto.randomUUID();

    console.log("New thread:", threadId);

    onNewchat(threadId);
    onNewchatClick([]);
  }

  return (
    <aside className="sidebar">

      {/* New Chat */}
      <button
        className="new-chat-btn"
        onClick={generateThreadId}
      >
        <span>＋</span>
        New chat
      </button>

      {/* Chat History */}
      <div className="chat-history">

        <div className="history-title">
          Today
        </div>

        {threads.map((threadId) => (
          <button
            key={threadId}
            className="chat-item"
            onClick={() => onSelectChat(threadId)}
          >
            <span className="chat-icon">
              💬
            </span>

            <span className="chat-title">
              {threadId}
            </span>
          </button>
        ))}

      </div>

    </aside>
  );
}

export default Sidebar;