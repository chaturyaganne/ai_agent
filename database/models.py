from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    """User model to store user information"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    onboarding_complete = Column(Boolean, default=False)
    onboarding_step = Column(Integer, default=1)
    
    # Relationships
    onboarding_responses = relationship("OnboardingResponse", back_populates="user", cascade="all, delete-orphan")
    conversation_logs = relationship("ConversationLog", back_populates="user", cascade="all, delete-orphan")

class OnboardingResponse(Base):
    """Store user responses from the 7-day onboarding"""
    __tablename__ = "onboarding_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    day = Column(Integer)  # 1-7
    question_key = Column(String(100))  # e.g., "currentMood", "lonelinessTriggers"
    question = Column(Text)  # The actual question asked
    answer = Column(Text)  # User's answer
    anton_response = Column(Text)  # Anton's response
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="onboarding_responses")

class ConversationLog(Base):
    """Store all conversation messages for context and analysis"""
    __tablename__ = "conversation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    message_type = Column(String(50))  # "user", "assistant", "system"
    content = Column(Text)
    day = Column(Integer)  # Which day the message was on
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="conversation_logs")

class UserInsights(Base):
    """Store extracted insights about the user from their responses"""
    __tablename__ = "user_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    insight_category = Column(String(100))  # e.g., "mood_pattern", "stress_trigger"
    insight_data = Column(JSON)  # Store flexible JSON data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
