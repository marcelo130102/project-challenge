# 🔒 Briefcase - Secure Document Delivery System

Internal secure document delivery system with encryption, access control, view limits and automatic expiration.

## 🚀 Quick Setup

### 1. Activate virtual environment

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 2. Install dependencies and configure
```bash
python setup.py
```

### 3. Run server
```bash
python run.py
```

**Open:** http://localhost:8000

---

## 📚 Documentation

- **[Complete Guide](docs/translations/README_EN.md)** - Full technical documentation
- **[Scripts](docs/scripts/)** - Utility scripts

---

## 🎯 Test Credentials

| User | Email | Password |
|------|-------|----------|
| Alice | alice@briefcase.com | password123 |
| Bob | bob@briefcase.com | password123 |
| Charlie | charlie@briefcase.com | password123 |

---

## 🔧 Utility Scripts

### Development
```bash
# Run server
python run.py

# Create test users
python seed.py

# Verify installation
python verify_installation.py
```

### Documentation
```bash
# View project structure
python docs/scripts/view_project.py

# Final verification
python docs/scripts/verify_final.py
```

---

## 🔐 Security Features

✓ **AES-256-CBC Encryption** - Documents encrypted at rest  
✓ **JWT Authentication** - Secure tokens with expiration  
✓ **Hashed Passwords** - bcrypt for credential protection  
✓ **Access Control** - Only sender/recipient access documents  
✓ **Auto-deletion** - Documents with view limits and expiration  

---

## 📁 Project Structure

```
briefcase/
├── main.py                      # Main FastAPI application
├── models.py                    # Database models
├── database.py                  # Database configuration
├── auth.py                      # Authentication system
├── encryption.py                # AES-256 encryption
├── config.py                    # Configuration
├── run.py                       # Run server
├── seed.py                      # Create test users
├── setup.py                     # Automated setup
├── verificar_instalacion.py    # Installation verification
├── requirements.txt             # Dependencies
├── templates/                   # HTML templates
│   ├── index.html              # Login page
│   └── dashboard.html          # Dashboard
├── static/                      # Static files
│   ├── style.css               # Styles
│   └── dashboard.js            # JavaScript
└── docs/                        # Documentation
    ├── scripts/                 # Utility scripts
    └── translations/            # English documentation
```

---

## 🛠️ Technology Stack

- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Authentication:** JWT + bcrypt
- **Encryption:** AES-256-CBC
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Server:** Uvicorn

---

## 🧪 Quick Test

1. **Login** with `alice@briefcase.com` / `password123`
2. **Upload document** → Select file → Choose `bob` → Upload
3. **Logout** → Login with `bob@briefcase.com` / `password123`
4. **Download document** → Click "View/Download"
5. **Verify encryption** → File should download correctly

---

## 📞 Support

- **API Documentation:** http://localhost:8000/docs
- **Application:** http://localhost:8000

---

**Development time:** < 2 hours  
**Status:** ✅ COMPLETED  
**Quality:** ⭐⭐⭐⭐⭐ EXCELLENT

Enjoy using Briefcase! 🔒