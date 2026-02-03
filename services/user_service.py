from database.db import DatabaseManager
from services.llm_service import LLMService
from collections import deque
from typing import List, Dict, Tuple

ONBOARDING_QUESTIONS = {
    1: {"key": "currentMood", "question": "How are you feeling today?"},
    2: {"key": "lonelinessTriggers", "question": "What situations make you feel lonely or disconnected?"},
    3: {"key": "stressSources", "question": "What has been stressing you most at work or life recently?"},
    4: {"key": "copingStrategies", "question": "When you feel stressed or down, how do you usually cope?"},
    5: {"key": "joyfulMoments", "question": "What moments in your life make you feel happy or relaxed?"},
    6: {"key": "relationshipGoals", "question": "What kind of friendships or connections do you hope to build here?"},
    7: {"key": "aspirations", "question": "Looking ahead, what would make you feel fulfilled in your social life or work?"}
}

class UserService:
    """Business logic for user interactions and onboarding"""
    
    def __init__(self, username: str):
        self.db = DatabaseManager()
        self.user = self.db.get_or_create_user(username)
        self.username = username
        self.short_term_memory = deque(maxlen=20)
        self.anton_started = False
    
    def get_initial_message(self) -> str:
        """Get Anton's initial greeting"""
        if self.user.onboarding_complete:
            # Generate check-in for completed users
            previous_responses = self.db.get_all_onboarding_responses(self.user.id)
            prev_answers = {r.question_key: r.answer for r in previous_responses}
            message = LLMService.generate_check_in_response(prev_answers, self.user.onboarding_step)
        else:
            # Initial greeting for new users
            message = "Hey! I'm Anton, your AI companion for Hytribe. Let's get to know each other over the next 7 days. " + \
                     ONBOARDING_QUESTIONS[1]["question"]
        
        self.short_term_memory.append({"role": "assistant", "content": message})
        self.db.save_conversation_message(
            self.user.id,
            "assistant",
            message,
            self.user.onboarding_step
        )
        self.anton_started = True
        return message
    
    def process_user_message(self, user_input: str) -> Tuple[str, bool]:
        """
        Process user message and generate Anton's response.
        
        Returns:
            Tuple of (response, should_show_mark_day_button)
        """
        
        # Store user input
        self.short_term_memory.append({"role": "user", "content": user_input})
        self.db.save_conversation_message(
            self.user.id,
            "user",
            user_input,
            self.user.onboarding_step
        )
        
        if not self.user.onboarding_complete:
            # Onboarding phase
            step = self.user.onboarding_step
            question_key = ONBOARDING_QUESTIONS[step]["key"]
            
            # Save the onboarding response
            self.db.save_onboarding_response(
                self.user.id,
                step,
                question_key,
                ONBOARDING_QUESTIONS[step]["question"],
                user_input,
                ""  # Will update after generating response
            )
            
            # Generate Anton's empathetic response
            response = LLMService.generate_response(user_input, list(self.short_term_memory))
            
            # Update the saved response with Anton's reply
            self.db.save_conversation_message(
                self.user.id,
                "assistant",
                response,
                step
            )
            
            self.short_term_memory.append({"role": "assistant", "content": response})
            
            return response, True  # Show mark day button
        else:
            # Post-onboarding: free conversation
            response = LLMService.generate_response(user_input, list(self.short_term_memory))
            
            self.db.save_conversation_message(
                self.user.id,
                "assistant",
                response,
                self.user.onboarding_step
            )
            
            self.short_term_memory.append({"role": "assistant", "content": response})
            return response, False
    
    def mark_day_complete(self) -> Tuple[str, bool]:
        """
        Mark the current day as complete and move to next day.
        
        Returns:
            Tuple of (message, onboarding_complete)
        """
        
        current_step = self.user.onboarding_step
        
        if current_step > 7:
            return "All onboarding already complete! 🎉", True
        
        # Move to next day
        next_step = current_step + 1
        self.db.update_user_onboarding(self.user.id, next_step, next_step > 7)
        self.user = self.db.get_or_create_user(self.username)
        
        # If onboarding is complete
        if next_step > 7:
            personality_data = {}
            for response in self.db.get_all_onboarding_responses(self.user.id):
                personality_data[response.question_key] = response.answer
            
            message = "🎉 You've completed all 7 onboarding days!\n\n" + \
                     "Here's your personality profile:\n" + \
                     "\n".join([f"**{k}**: {v[:100]}..." if len(v) > 100 else f"**{k}**: {v}" 
                               for k, v in personality_data.items()])
            
            self.db.save_conversation_message(
                self.user.id,
                "system",
                "Onboarding complete",
                current_step
            )
            
            return message, True
        
        # Generate transition message with empathy
        last_question_key = ONBOARDING_QUESTIONS[current_step]["key"]
        last_answer_response = self.db.get_onboarding_response(self.user.id, current_step)
        last_answer = last_answer_response.answer if last_answer_response else ""
        
        empathy_message = LLMService.generate_empathy_response(last_answer)
        
        # Get next question
        next_question = ONBOARDING_QUESTIONS[next_step]["question"]
        
        full_message = f"{empathy_message}\n\n**Day {next_step}/7:** {next_question}"
        
        self.short_term_memory.append({"role": "assistant", "content": full_message})
        self.db.save_conversation_message(
            self.user.id,
            "assistant",
            full_message,
            next_step
        )
        
        return full_message, False
    
    def get_current_question(self) -> str:
        """Get the current day's question"""
        if self.user.onboarding_complete:
            return "Feel free to chat with me about anything on your mind!"
        return ONBOARDING_QUESTIONS[self.user.onboarding_step]["question"]
    
    def get_user_status(self) -> Dict:
        """Get current user status"""
        return {
            "username": self.user.username,
            "onboarding_step": self.user.onboarding_step,
            "onboarding_complete": self.user.onboarding_complete,
            "current_question": self.get_current_question()
        }
    
    def export_user_data(self) -> Dict:
        """Export all user data as JSON"""
        return self.db.export_user_data_to_json(self.user.id)
