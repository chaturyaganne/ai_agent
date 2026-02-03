"""
Anton - AI Companion for Hytribe
Main entry point for the application
"""

from ui.app import launch

if __name__ == "__main__":
    print("🤖 Starting Anton - AI Companion...")
    print("Make sure HF_TOKEN is set: export HF_TOKEN='your_token'")
    launch()
