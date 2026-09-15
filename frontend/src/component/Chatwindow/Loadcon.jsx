import React, { useEffect, useState } from "react";

function Loadcon({ thread_id , messages,setMsg}) {
  // const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!thread_id) {
      setMsg([]);
      return;
    }

    const loadConversation = async () => {
      try {
        setLoading(true);

        const response = await fetch(
          `http://localhost:8000/load_convo/${thread_id}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();

        console.log("Conversation data:", data);

        // API can return either:
        // [ {...}, {...} ]
        // OR
        // { messages: [ {...}, {...} ] }

        const conversation = Array.isArray(data)
          ? data
          : data.messages || [];

          setMsg(conversation);

      } catch (error) {
        console.error("Error loading conversation:", error);
        setMsg([]);
      } finally {
        setLoading(false);
      }
    };

    loadConversation();
  }, [thread_id]);

  return (
    <div className="conversation">
      {loading && <p>Loading...</p>}

      {!loading && messages.length === 0 && (
        <p>No messages found.</p>
      )}

      {!loading &&
        messages.map((message, index) => (
          <div
            className={`chatwindow ${
              message.type === "human"
                ? "user-message"
                : "ai-message"
            }`}
            key={index}
          >
            <span className="chat-icon">
              {message.type === "human" ? "👤" : "🤖"}
            </span>

            <span className="chat-title">
              {message.content}
            </span>
          </div>
        ))}
    </div>
  );
}

export default Loadcon;
