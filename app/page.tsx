"use client";

import { useEffect, useState } from "react";
import { useChat } from "@/lib/hooks/useChat";
import ChatWindow from "@/components/ChatWindow";
import UserStatus from "@/components/UserStatus";

export default function Home() {
  const [isLoading, setIsLoading] = useState(true);
  const { messages, sendMessage, userStatus, markDayComplete } = useChat();

  useEffect(() => {
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-4">🤖 Anton</h1>
          <p className="text-white opacity-75">Loading your companion...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Chat Area */}
          <div className="lg:col-span-3">
            <div className="bg-white bg-opacity-95 rounded-lg shadow-2xl overflow-hidden h-[600px] flex flex-col">
              <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6">
                <h1 className="text-3xl font-bold">🤖 Anton - Your AI Companion</h1>
                <p className="text-indigo-100 mt-1">Complete 7 days of onboarding to help us understand you better</p>
              </div>

              <ChatWindow
                messages={messages}
                onSendMessage={sendMessage}
                onMarkDayComplete={markDayComplete}
              />
            </div>
          </div>

          {/* Status Panel */}
          <div className="lg:col-span-1">
            <UserStatus status={userStatus} />
          </div>
        </div>
      </div>
    </main>
  );
}
