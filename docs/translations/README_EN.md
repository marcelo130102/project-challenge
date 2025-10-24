# 🔒 Briefcase - Secure Document Delivery System

Internal secure document delivery system with encryption, access control, view limits and automatic expiration.

## 🚀 Features

- ✅ **JWT Authentication** - Secure login system with JWT tokens
- 🔐 **AES-256 Encryption** - Documents encrypted at rest using AES-256-CBC
- 👥 **Access Control** - Only sender and recipient can access documents
- 📊 **View Limits** - Configurable per document
- ⏰ **Automatic Expiration** - Documents are deleted when expired or view limit reached
- 🎨 **Modern Interface** - Clean and responsive UI

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)

## 🛠️ Installation and Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd reto-tecnico
```

### 2. Create and activate virtual environment

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

*If you get execution policy error:*
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**On macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 📋 **OS-specific guides:**
> - 🪟 **Windows:** [QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md)
> - 🍎 **macOS:** [QUICK_START_MACOS.md](QUICK_START_MACOS.md)
> - 🐧 **Linux:** [QUICK_START_LINUX.md](QUICK_START_LINUX.md)

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**Note:** Dependencies have been tested and are compatible with Windows, macOS and Linux.

### 4. Configure environment variables (OPTIONAL for production)

Create a `.env` file based on `.env.example`:

```bash
SECRET_KEY=your-secret-key-change-in-production
ENCRYPTION_KEY=your-encryption-key-32-bytes
DATABASE_URL=sqlite:///./briefcase.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Note:** For development, default keys work. In production, **ALWAYS** use secure and random keys.

### 5. Initialize database with test users

```bash
python seed.py
```

This will create 3 test users:
- **Email:** alice@briefcase.com | **Password:** password123
- **Email:** bob@briefcase.com | **Password:** password123
- **Email:** charlie@briefcase.com | **Password:** password123

### 6. Verify installation (Optional)

```bash
python verificar_instalacion.py
```

This script verifies that:
- All modules are installed
- All project files exist
- Database is configured correctly

### 7. Run the application

```bash
python run.py
```

Or use alternative commands:

```bash
python main.py
# or
uvicorn main:app --reload
```

The application will be available at: **http://localhost:8000**

## 🎯 Usage

1. **Login:** Access with one of the test accounts
2. **Upload Document:**
   - Select a file
   - Choose recipient
   - (Optional) Configure view limit
   - (Optional) Configure expiration in days
3. **View Documents:**
   - Left panel: Sent documents
   - Right panel: Received documents
4. **Download:** Click "View/Download" (increments view counter)

## 🔐 Security Architecture

### Document Encryption

- **Algorithm:** AES-256-CBC
- **Implementation:** `cryptography` library (Python)
- **Process:**
  1. File is read as bytes
  2. Random IV (Initialization Vector) of 16 bytes is generated
  3. Content is encrypted using AES-256-CBC
  4. Stored: IV (16 bytes) + encrypted content
  5. When decrypting, IV is extracted and used to recover original content

### Authentication

- **JWT tokens** with configurable expiration (default: 30 minutes)
- **Hashed passwords** with bcrypt
- **HttpOnly cookies** for token storage (XSS protection)

### Access Control

- Only **sender** and **recipient** can access a document
- Verification on each download request
- Automatic deletion when limits are reached

### Deletion Rules

Documents are automatically deleted when:
1. Expiration date is reached (`expires_at`)
2. View limit is reached (`view_limit`)
3. System checks this on each listing and download

## 📁 Project Structure

```
briefcase/
├── main.py                      # Main FastAPI application
├── models.py                    # SQLAlchemy models (User, Document)
├── database.py                  # Database configuration
├── auth.py                      # JWT authentication system
├── encryption.py                # AES-256 encryption
├── config.py                    # Configuration and environment variables
├── seed.py                      # Script to create test users
├── run.py                       # Convenient script to run server
├── setup.py                     # Automated installation script
├── verificar_instalacion.py    # Script to verify installation
├── requirements.txt             # Python dependencies
├── templates/                   # HTML templates
│   ├── index.html              # Login page
│   └── dashboard.html          # Main dashboard
├── static/                      # Static files
│   ├── style.css               # CSS styles
│   └── dashboard.js            # Dashboard JavaScript
├── README.md                    # Complete documentation
├── QUICK_START_WINDOWS.md      # Windows quick guide
└── QUICK_INSTRUCTIONS.md       # Essential commands
```

### Useful Scripts

| Script | Purpose |
|--------|---------|
| `run.py` | Runs the server conveniently |
| `seed.py` | Creates test users in DB |
| `setup.py` | Complete automated installation |
| `verificar_instalacion.py` | Verifies everything is installed |

## 🔒 Security Notes

### For Development

✅ Default keys in `config.py` are sufficient for local testing

### For Production

❗ **CRITICAL - Change before deploying:**

1. **SECRET_KEY:** Use a strong random key (32+ characters)
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

2. **ENCRYPTION_KEY:** Use a key of exactly 32 bytes
   ```python
   import secrets
   print(secrets.token_urlsafe(24))  # Will result in ~32 chars base64
   ```

3. **Database:** Migrate from SQLite to PostgreSQL/MySQL

4. **HTTPS:** Use HTTPS in production (Nginx + Let's Encrypt)

5. **Environment variables:** Never commit `.env` with real keys

### Additional Considerations

- Deleted documents use "soft delete" (`is_deleted` flag)
- For permanent deletion, implement periodic cleanup task
- JWT tokens expire automatically
- Consider rate limiting in production
- Implement access logging for audit

## 🧪 Testing

### Manual Testing

1. Login with `alice@briefcase.com`
2. Upload a document for `bob@briefcase.com` with 2 view limit
3. Logout and login with `bob@briefcase.com`
4. Download the document 2 times
5. Verify it disappears automatically after second download

### Expiration Testing

1. Upload a document with 1 day expiration
2. Documents with `expires_at` in the past are automatically deleted

## 📚 API Endpoints

### Authentication
- `POST /api/login` - Login with email/password
- `POST /api/logout` - Logout
- `GET /api/me` - Get current user

### Users
- `GET /api/users` - List users (except current)

### Documents
- `POST /api/documents/upload` - Upload encrypted document
- `GET /api/documents` - List documents (sent and received)
- `GET /api/documents/{id}/download` - Download document

### UI
- `GET /` - Login page
- `GET /dashboard` - Main dashboard

## 🛠️ Technology Stack

- **Backend:** FastAPI 0.104+
- **ORM:** SQLAlchemy 2.0
- **Database:** SQLite (dev), PostgreSQL recommended (prod)
- **Auth:** python-jose (JWT), passlib (bcrypt)
- **Encryption:** cryptography (AES-256)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Server:** Uvicorn (ASGI)

## 📝 License

This is a technical test project.

## 👨‍💻 Author

Developed as part of a technical test to demonstrate knowledge in:
- Backend development with Python
- Security (encryption, authentication)
- REST API
- Access control
- User interface

---

**Development time:** < 2 hours  
**Completed:** ✅
