from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
import base64
import io

from database import get_db, init_db
from models import User, Document
from auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from encryption import DocumentEncryption
from config import settings
from pydantic import BaseModel

app = FastAPI(title="Briefcase - Secure Document Delivery System")

# Initialize encryption
encryptor = DocumentEncryption(settings.ENCRYPTION_KEY)

# Templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Pydantic schemas
class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class DocumentResponse(BaseModel):
    id: int
    filename: str
    sender_id: int
    sender_username: str
    recipient_id: int
    recipient_username: str
    view_limit: Optional[int]
    view_count: int
    expires_at: Optional[datetime]
    created_at: datetime
    is_expired: bool
    is_limit_reached: bool
    
    class Config:
        from_attributes = True


# Dependency to get current user from token
async def get_current_user_dependency(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user = get_current_user(db, token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return user


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page - shows login or redirects to dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/login")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint - returns JWT token"""
    user = authenticate_user(db, login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username
            }
        },
        headers={"Set-Cookie": f"access_token={access_token}; HttpOnly; SameSite=Strict; Path=/"}
    )


@app.post("/api/logout")
async def logout():
    """Logout endpoint - removes cookie"""
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("access_token")
    return response


@app.get("/api/me")
async def get_me(current_user: User = Depends(get_current_user_dependency)):
    """Gets current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }


@app.get("/api/users")
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """Lists all users (to select recipient)"""
    users = db.query(User).filter(User.id != current_user.id).all()
    return [
        {"id": u.id, "username": u.username, "email": u.email}
        for u in users
    ]


@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    recipient_id: int = Form(...),
    view_limit: Optional[int] = Form(None),
    expires_in_days: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Uploads an encrypted document and assigns it to a recipient
    """
    # Validate recipient
    recipient = db.query(User).filter(User.id == recipient_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    # Read file content
    file_content = await file.read()
    
    # Encrypt content
    encrypted_content = encryptor.encrypt_file(file_content)
    
    # Calculate expiration date
    expires_at = None
    if expires_in_days and expires_in_days > 0:
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    # Create document in database
    document = Document(
        filename=file.filename,
        encrypted_content=encrypted_content,
        sender_id=current_user.id,
        recipient_id=recipient_id,
        view_limit=view_limit if view_limit and view_limit > 0 else None,
        expires_at=expires_at
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        "message": "Document uploaded successfully",
        "document_id": document.id,
        "filename": document.filename
    }


@app.get("/api/documents")
async def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Lists user documents (sent and received)
    Applies automatic deletion rules
    """
    # Delete expired documents or those that reached view limit
    now = datetime.utcnow()
    expired_docs = db.query(Document).filter(
        Document.is_deleted == False,
        ((Document.expires_at != None) & (Document.expires_at <= now))
    ).all()
    
    for doc in expired_docs:
        doc.is_deleted = True
    
    # Documents that reached the limit
    limit_reached_docs = db.query(Document).filter(
        Document.is_deleted == False,
        Document.view_limit != None,
        Document.view_count >= Document.view_limit
    ).all()
    
    for doc in limit_reached_docs:
        doc.is_deleted = True
    
    db.commit()
    
    # Get sent documents
    sent_docs = db.query(Document).filter(
        Document.sender_id == current_user.id,
        Document.is_deleted == False
    ).all()
    
    # Get received documents
    received_docs = db.query(Document).filter(
        Document.recipient_id == current_user.id,
        Document.is_deleted == False
    ).all()
    
    def format_doc(doc: Document):
        is_expired = doc.expires_at and doc.expires_at <= now
        is_limit_reached = doc.view_limit and doc.view_count >= doc.view_limit
        
        return {
            "id": doc.id,
            "filename": doc.filename,
            "sender_id": doc.sender_id,
            "sender_username": doc.sender.username,
            "recipient_id": doc.recipient_id,
            "recipient_username": doc.recipient.username,
            "view_limit": doc.view_limit,
            "view_count": doc.view_count,
            "expires_at": doc.expires_at.isoformat() if doc.expires_at else None,
            "created_at": doc.created_at.isoformat(),
            "is_expired": is_expired,
            "is_limit_reached": is_limit_reached
        }
    
    return {
        "sent": [format_doc(doc) for doc in sent_docs],
        "received": [format_doc(doc) for doc in received_docs]
    }


@app.get("/api/documents/{document_id}/download")
# auth_verify(request_user, )
async def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_dependency)
):
    """
    Downloads a document (only if user is sender or recipient)
    Increments view counter
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.is_deleted == False
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permissions: only sender and recipient can access
    if document.sender_id != current_user.id and document.recipient_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to access this document")
    
    # Check if expired
    if document.expires_at and document.expires_at <= datetime.utcnow():
        document.is_deleted = True
        db.commit()
        raise HTTPException(status_code=410, detail="The document has expired")
    
    # Check if reached view limit
    if document.view_limit and document.view_count >= document.view_limit:
        document.is_deleted = True
        db.commit()
        raise HTTPException(status_code=410, detail="The document reached the view limit")
    
    # Increment view counter (only for recipient)
    if current_user.id == document.recipient_id:
        document.view_count += 1
        
        # If reached limit, mark as deleted
        if document.view_limit and document.view_count >= document.view_limit:
            document.is_deleted = True
        
        db.commit()
    
    # Decrypt content
    try:
        decrypted_content = encryptor.decrypt_file(document.encrypted_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error decrypting document")
    
    # Return file
    return StreamingResponse(
        io.BytesIO(decrypted_content),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={document.filename}"
        }
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# Estructura de proyecto
'''
app/
    controllers/
        file_controller.py
        user_controller.py
    services/
        file_service.py
        user_service.py
        notification_service.py -- patron observer
    repositories/
        file_repository.py
        user_repository.py
    models/
        file_model.py
        user_model.py
    dtos/
        file_dto.py	
    routes/
        file_routes.py
        user_routes.py
'''