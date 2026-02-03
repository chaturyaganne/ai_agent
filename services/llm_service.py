import requests
import os
from typing import List, Dict
from huggingface_hub import InferenceClient

HF_API_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"

class LLMService:
    """Service for LLaMA 3.2 API calls via HuggingFace"""
    
    SYSTEM_PROMPT = """You are Anton, an empathetic AI companion for Hytribe.
- Respond warmly, peer-like, non-judgmental.
- Ask emotional questions and comment empathetically.
- Keep responses concise (max 50 tokens).
- Reference previous insights naturally.
- Never give therapeutic advice or diagnosis."""
    
    @staticmethod
    def generate_response(user_input: str, memory: List[Dict], max_tokens: int = 50) -> str:
        """
        Generate Anton's response using HuggingFace Inference API.
        
        Args:
            user_input: The user's message
            memory: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response string
        """
        
        # Build text prompt from memory
        context_text = "\n".join([m["content"] for m in memory if m["role"] == "assistant"])
        
        prompt = LLMService.SYSTEM_PROMPT + "\n"
        if context_text:
            prompt += "Previous insights:\n" + context_text + "\n"
        prompt += f"User: {user_input}\nAnton:"
        
        return LLMService._call_api(prompt, max_tokens)
    
    @staticmethod
    def generate_empathy_response(previous_answer: str, max_tokens: int = 40) -> str:
        """
        Generate an empathetic acknowledgment of a previous response.
        Used when transitioning between days.
        
        Args:
            previous_answer: The user's answer from the previous day
            max_tokens: Maximum tokens to generate
            
        Returns:
            Empathetic response
        """
        
        prompt = f"""You are Anton, an empathetic AI companion.
The user previously shared: '{previous_answer}'
Respond with warmth, empathy, and acknowledgment in 1-2 sentences, then ask how they're doing today."""
        
        return LLMService._call_api(prompt, max_tokens)
    
    @staticmethod
    def generate_check_in_response(previous_answers: Dict[str, str], current_day: int) -> str:
        """
        Generate a check-in message that references previous insights.
        
        Args:
            previous_answers: Dictionary of previous onboarding answers
            current_day: Current day number
            
        Returns:
            Check-in message
        """
        
        context = "\n".join([f"- {k}: {v[:100]}" for k, v in list(previous_answers.items())[-2:]])
        
        prompt = f"""You are Anton, an empathetic AI companion checking in with the user.
Previous insights:
{context}

Write a warm, brief check-in message (2-3 sentences) asking how they're doing today related to these areas."""
        
        return LLMService._call_api(prompt, 60)
    
    @staticmethod
    def _call_api(prompt: str, max_tokens: int) -> str:
        """
        Internal method to call HuggingFace API using HF SDK.
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text or fallback message
        """
        
        if not HF_API_TOKEN:
            return "Error: HF_TOKEN environment variable not set. Please set your HuggingFace token."
        
        try:
            client = InferenceClient(api_key=HF_API_TOKEN)
            
            # Use chat completion API
            message_list = [{"role": "user", "content": prompt}]
            response = client.chat_completion(
                messages=message_list,
                model=MODEL_NAME,
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9
            )
            
            # Extract text from response
            if hasattr(response, 'choices') and len(response.choices) > 0:
                text = response.choices[0].message.content.strip()
            elif isinstance(response, dict) and "choices" in response:
                text = response["choices"][0]["message"]["content"].strip()
            else:
                text = str(response).strip()
            
            # Clean up the response
            if "Anton:" in text:
                text = text.split("Anton:")[-1].strip()
            
            # Remove any "User:" prefixes
            if text.startswith("User:"):
                text = text[5:].strip()
            
            return text[:500]  # Limit response length
        
        except Exception as e:
            error_str = str(e).lower()
            if "401" in error_str or "unauthorized" in error_str or "invalid" in error_str:
                return "Error: Your HF_TOKEN may be invalid. Please verify your token on huggingface.co/settings/tokens"
            elif "timeout" in error_str:
                return "I'm thinking about what you said... please try again in a moment."
            else:
                return "I'm having trouble responding right now. Please try again."
