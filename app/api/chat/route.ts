import { NextRequest, NextResponse } from "next/server";

// This would connect to your LLM service
// For now, we'll create a simple integration point

export async function POST(req: NextRequest) {
  try {
    const { message, memory } = await req.json();

    if (!message) {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 }
      );
    }

    // Call your Python LLM service
    const response = await fetch("http://localhost:8000/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_input: message, memory }),
    });

    if (!response.ok) {
      throw new Error("LLM service error");
    }

    const data = await response.json();

    return NextResponse.json({
      response: data.response,
    });
  } catch (error) {
    console.error("Error in chat API:", error);
    return NextResponse.json(
      { error: "Failed to generate response" },
      { status: 500 }
    );
  }
}
