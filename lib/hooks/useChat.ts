import { useState, useCallback } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface UserStatus {
  username: string;
  onboarding_step: number;
  onboarding_complete: boolean;
  created_at: string;
  last_message_at: string;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [userStatus, setUserStatus] = useState<UserStatus | null>(null);

  const fetchUserStatus = useCallback(async () => {
    try {
      const response = await fetch("/api/user");
      if (response.ok) {
        const data = await response.json();
        setUserStatus(data);
        return data;
      }
    } catch (error) {
      console.error("Failed to fetch user status:", error);
    }
  }, []);

  const sendMessage = useCallback(
    async (message: string) => {
      if (!message.trim()) return;

      // Add user message to UI
      setMessages((prev) => [...prev, { role: "user", content: message }]);

      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message,
            memory: messages,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: data.response },
          ]);
        } else {
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: "I'm having trouble responding. Please try again.",
            },
          ]);
        }
      } catch (error) {
        console.error("Failed to send message:", error);
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: "Error connecting to server. Please try again.",
          },
        ]);
      }
    },
    [messages]
  );

  const markDayComplete = useCallback(async () => {
    try {
      const response = await fetch("/api/user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "mark-day-complete" }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: data.message },
        ]);
        await fetchUserStatus();
      }
    } catch (error) {
      console.error("Failed to mark day complete:", error);
    }
  }, [fetchUserStatus]);

  // Initialize
  useEffect(() => {
    fetchUserStatus();
  }, [fetchUserStatus]);

  return {
    messages,
    sendMessage,
    userStatus,
    markDayComplete,
  };
}

import { useEffect } from "react";
