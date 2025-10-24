from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sent_documents = relationship("Document", foreign_keys="Document.sender_id", back_populates="sender")
    received_documents = relationship("Document", foreign_keys="Document.recipient_id", back_populates="recipient")


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    encrypted_content = Column(LargeBinary, nullable=False)  # Encrypted content
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    view_limit = Column(Integer, nullable=True)  # View limit (optional)
    view_count = Column(Integer, default=0)  # View counter
    expires_at = Column(DateTime, nullable=True)  # Expiration date (optional)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)  # Soft delete
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_documents")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_documents")

