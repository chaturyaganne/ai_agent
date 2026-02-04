import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  try {
    // Get user status from your backend
    const response = await fetch("http://localhost:8000/api/user/status", {
      headers: { "Authorization": `Bearer ${req.headers.get("Authorization")}` },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch user status");
    }

    const data = await response.json();

    return NextResponse.json(data);
  } catch (error) {
    console.error("Error fetching user status:", error);
    return NextResponse.json(
      { error: "Failed to fetch status" },
      { status: 500 }
    );
  }
}

export async function POST(req: NextRequest) {
  try {
    const { action } = await req.json();

    if (action === "mark-day-complete") {
      const response = await fetch("http://localhost:8000/api/user/mark-complete", {
        method: "POST",
        headers: { "Authorization": `Bearer ${req.headers.get("Authorization")}` },
      });

      if (!response.ok) {
        throw new Error("Failed to mark day complete");
      }

      const data = await response.json();
      return NextResponse.json(data);
    }

    return NextResponse.json({ error: "Unknown action" }, { status: 400 });
  } catch (error) {
    console.error("Error in user API:", error);
    return NextResponse.json(
      { error: "Failed to process request" },
      { status: 500 }
    );
  }
}
