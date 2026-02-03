from database import SessionLocal, init_db
from database.models import User, OnboardingResponse, ConversationLog, UserInsights
from datetime import datetime
import json

class DatabaseManager:
    """Manage all database operations"""
    
    def __init__(self):
        init_db()
    
    # ===================== USER OPERATIONS =====================
    
    def get_or_create_user(self, username: str) -> User:
        """Get existing user or create new one"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                user = User(username=username)
                db.add(user)
                db.commit()
                db.refresh(user)
            return user
        finally:
            db.close()
    
    def get_user(self, username: str) -> User:
        """Get user by username"""
        db = SessionLocal()
        try:
            return db.query(User).filter(User.username == username).first()
        finally:
            db.close()
    
    def update_user_onboarding(self, user_id: int, step: int, complete: bool = False) -> User:
        """Update user's onboarding progress"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.onboarding_step = step
                user.onboarding_complete = complete
                db.commit()
                db.refresh(user)
            return user
        finally:
            db.close()
    
    # ===================== ONBOARDING RESPONSE OPERATIONS =====================
    
    def save_onboarding_response(
        self,
        user_id: int,
        day: int,
        question_key: str,
        question: str,
        answer: str,
        anton_response: str
    ) -> OnboardingResponse:
        """Save a user's onboarding response"""
        db = SessionLocal()
        try:
            response = OnboardingResponse(
                user_id=user_id,
                day=day,
                question_key=question_key,
                question=question,
                answer=answer,
                anton_response=anton_response
            )
            db.add(response)
            db.commit()
            db.refresh(response)
            return response
        finally:
            db.close()
    
    def get_onboarding_response(self, user_id: int, day: int) -> OnboardingResponse:
        """Get onboarding response for a specific day"""
        db = SessionLocal()
        try:
            return db.query(OnboardingResponse).filter(
                OnboardingResponse.user_id == user_id,
                OnboardingResponse.day == day
            ).first()
        finally:
            db.close()
    
    def get_all_onboarding_responses(self, user_id: int) -> list:
        """Get all onboarding responses for a user"""
        db = SessionLocal()
        try:
            return db.query(OnboardingResponse).filter(
                OnboardingResponse.user_id == user_id
            ).order_by(OnboardingResponse.day).all()
        finally:
            db.close()
    
    # ===================== CONVERSATION LOG OPERATIONS =====================
    
    def save_conversation_message(
        self,
        user_id: int,
        message_type: str,
        content: str,
        day: int
    ) -> ConversationLog:
        """Save a conversation message"""
        db = SessionLocal()
        try:
            log = ConversationLog(
                user_id=user_id,
                message_type=message_type,
                content=content,
                day=day
            )
            db.add(log)
            db.commit()
            db.refresh(log)
            return log
        finally:
            db.close()
    
    def get_conversation_history(self, user_id: int, limit: int = 20) -> list:
        """Get recent conversation history for context"""
        db = SessionLocal()
        try:
            return db.query(ConversationLog).filter(
                ConversationLog.user_id == user_id
            ).order_by(ConversationLog.created_at.desc()).limit(limit).all()
        finally:
            db.close()
    
    def get_conversation_history_for_day(self, user_id: int, day: int) -> list:
        """Get all messages for a specific day"""
        db = SessionLocal()
        try:
            return db.query(ConversationLog).filter(
                ConversationLog.user_id == user_id,
                ConversationLog.day == day
            ).order_by(ConversationLog.created_at).all()
        finally:
            db.close()
    
    # ===================== EXPORT OPERATIONS =====================
    
    def export_user_data_to_json(self, user_id: int) -> dict:
        """Export all user data as JSON"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {}
            
            onboarding_data = {}
            for response in db.query(OnboardingResponse).filter(OnboardingResponse.user_id == user_id).all():
                onboarding_data[response.question_key] = {
                    "day": response.day,
                    "question": response.question,
                    "answer": response.answer,
                    "response_date": response.created_at.isoformat()
                }
            
            conversation_history = []
            for log in db.query(ConversationLog).filter(ConversationLog.user_id == user_id).order_by(ConversationLog.created_at).all():
                conversation_history.append({
                    "type": log.message_type,
                    "content": log.content,
                    "day": log.day,
                    "timestamp": log.created_at.isoformat()
                })
            
            return {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "created_at": user.created_at.isoformat(),
                    "onboarding_complete": user.onboarding_complete,
                    "onboarding_step": user.onboarding_step
                },
                "onboarding_data": onboarding_data,
                "conversation_history": conversation_history,
                "exported_at": datetime.utcnow().isoformat()
            }
        finally:
            db.close()
