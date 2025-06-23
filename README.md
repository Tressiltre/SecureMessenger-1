# CryptoSecure App

A comprehensive Flask web application providing advanced cryptographic capabilities including RSA encryption, MD5 hashing, user authentication, and image steganography.

## 🛡️ Features

### Core Security Features
- **RSA Encryption/Decryption**: 2048-bit RSA public-key cryptography for secure message encryption
- **MD5 Hashing**: Message integrity verification using MD5 cryptographic hash functions
- **Image Steganography**: Hide and extract secret messages within images using LSB (Least Significant Bit) techniques
- **User Authentication**: Secure user registration and login system with password hashing

### Key Capabilities
- **Automatic Key Generation**: Personal RSA key pairs generated for each user upon registration
- **Message Integrity**: MD5 hash verification to ensure message authenticity
- **File Upload Security**: Support for multiple image formats with size and type validation
- **Secure Session Management**: Flask-Login integration for session handling
- **Responsive Design**: Bootstrap-based dark theme interface

## 🏗️ Architecture

### Backend Stack
- **Flask**: Python web framework for application structure
- **SQLAlchemy**: ORM for database operations and models
- **PostgreSQL**: Production-ready database for data persistence
- **Cryptography Library**: Industry-standard cryptographic operations
- **Pillow (PIL)**: Image processing for steganography operations

### Frontend Stack
- **Bootstrap 5**: Responsive UI framework with dark theme
- **Feather Icons**: Lightweight icon library
- **Custom CSS**: Enhanced styling and animations
- **Vanilla JavaScript**: Client-side validation and interactions

### Security Implementation
- **Werkzeug Security**: Password hashing and verification
- **RSA OAEP Padding**: Secure encryption padding scheme
- **File Validation**: Comprehensive upload security checks
- **CSRF Protection**: Built-in Flask security features

## 📁 Project Structure

```
├── app.py                 # Flask application configuration
├── main.py               # Application entry point
├── routes.py             # URL routing and view logic
├── models.py             # Database models and relationships
├── crypto_utils.py       # RSA encryption and MD5 hashing utilities
├── steganography.py      # Image steganography implementation
├── templates/            # Jinja2 HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Landing page
│   ├── login.html       # User authentication
│   ├── register.html    # User registration
│   ├── dashboard.html   # User dashboard
│   ├── encrypt.html     # Message encryption interface
│   ├── decrypt.html     # Message decryption interface
│   ├── steganography.html # Image hiding interface
│   ├── extract.html     # Message extraction interface
│   ├── 404.html         # Error handling
│   └── 500.html         # Error handling
├── static/
│   ├── css/custom.css   # Custom styling
│   └── js/main.js       # Client-side functionality
├── uploads/             # File upload directory
└── README.md           # Project documentation
```

## 🔧 Technical Specifications

### Cryptographic Features
- **RSA Key Size**: 2048-bit keys for optimal security/performance balance
- **Encryption Padding**: OAEP with SHA-256 MGF1 for enhanced security
- **Hash Algorithm**: MD5 for message integrity (educational purposes)
- **Steganography**: LSB modification with secret key protection

### Database Schema
- **Users**: Authentication and RSA key storage
- **Messages**: Encrypted message history with integrity hashes
- **Steganography Operations**: File processing history and metadata

### File Handling
- **Supported Formats**: PNG, JPG, JPEG, GIF, BMP
- **Maximum File Size**: 16MB upload limit
- **Security Validation**: File type and size verification
- **Unique Naming**: UUID-based filename generation

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Virtual environment (recommended)

### Environment Variables
```bash
DATABASE_URL=postgresql://username:password@localhost/dbname
SESSION_SECRET=your_secret_key_here
```

### Installation Steps

#### Local Development
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cryptosecure-app
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install flask flask-sqlalchemy flask-login cryptography pillow psycopg2-binary gunicorn werkzeug email-validator pyjwt sqlalchemy oauthlib
   ```

4. Set up PostgreSQL database and configure environment variables:
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost/cryptosecure"
   export SESSION_SECRET="your-super-secret-key-here"
   ```

5. Run the application:
   ```bash
   python main.py
   ```

#### Production Deployment
For production deployment using Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

#### Replit Deployment
This application is configured to run on Replit:
1. Fork or import the project to Replit
2. PostgreSQL database is automatically configured
3. Environment variables are handled by Replit
4. Run using the configured workflow or `python main.py`

### How to Run

#### Development Mode
```bash
# Activate virtual environment
source venv/bin/activate

# Run Flask development server
python main.py
```
The application will be available at `http://localhost:5000`

#### Production Mode
```bash
# Using Gunicorn for production
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

#### Docker (Optional)
```dockerfile
# Dockerfile example
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### Database Setup
The application automatically creates database tables on first run. For manual setup:
```python
from app import app, db
with app.app_context():
    db.create_all()
```

### File Structure Requirements
Ensure the `uploads/` directory exists for file uploads:
```bash
mkdir uploads
```

### Quick Start Guide

#### For First-Time Users:
1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd cryptosecure-app
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install flask flask-sqlalchemy flask-login cryptography pillow psycopg2-binary gunicorn werkzeug email-validator pyjwt sqlalchemy oauthlib
   ```

3. **Configure Database**:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost/cryptosecure"
   export SESSION_SECRET="your-secret-key"
   ```

4. **Run Application**:
   ```bash
   python main.py
   ```

5. **Access Application**:
   Open browser to `http://localhost:5000`

#### Default Access:
- **Registration**: Create new account at `/register`
- **Login**: Access existing account at `/login`
- **Dashboard**: Main interface at `/dashboard` (after login)

### Application Usage Flow

1. **Register Account**: Create user account with automatic RSA key generation
2. **Login**: Access your secure dashboard
3. **Encrypt Messages**: Use RSA encryption with MD5 integrity verification
4. **Hide Messages**: Use steganography to conceal secrets in images
5. **Decrypt/Extract**: Retrieve encrypted messages or extract hidden content

### Troubleshooting

#### Common Issues:
- **Database Connection**: Verify PostgreSQL is running and DATABASE_URL is correct
- **File Upload Errors**: Ensure uploads directory exists with proper permissions
- **Import Errors**: Install all dependencies in active virtual environment
- **Port Conflicts**: Default port 5000, modify in main.py if needed
- **Permission Issues**: Check file system permissions for uploads directory

#### Debug Mode:
Enable debug logging by setting Flask debug mode:
```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

## 💡 Usage Examples

### User Registration & Authentication
1. Create account with automatic RSA key generation
2. Secure login with password verification
3. Session management with Flask-Login

### Message Encryption Workflow
1. Enter message (up to 190 characters for RSA)
2. Automatic encryption using user's public key
3. MD5 hash generation for integrity verification
4. Secure storage in database

### Steganography Process
1. Upload image file (PNG, JPG, etc.)
2. Enter secret message and encryption key
3. LSB modification to hide message in image
4. Download processed image with hidden content

### Message Extraction
1. Upload image containing hidden message
2. Provide secret key used for hiding
3. Extract and display hidden message
4. Verify message integrity

## 🔒 Security Considerations

### Cryptographic Security
- RSA 2048-bit keys provide strong encryption
- OAEP padding prevents various attack vectors
- Secure random key generation
- Individual key pairs per user

### Application Security
- Password hashing with Werkzeug
- File upload validation and sanitization
- SQL injection prevention with SQLAlchemy
- XSS protection with Jinja2 templating

### Best Practices Implemented
- Secure session management
- Input validation on client and server
- Error handling without information disclosure
- Proper file handling and cleanup

## 📊 Performance Features

### Optimization Techniques
- Database connection pooling
- Efficient file handling with PIL
- Client-side validation to reduce server load
- Responsive design for all device types

### Scalability Considerations
- PostgreSQL for production-grade database operations
- Modular code structure for easy maintenance
- RESTful design patterns
- Efficient image processing algorithms

## 🎯 Educational Value

This project demonstrates:
- **Cryptographic Implementation**: Practical RSA encryption usage
- **Steganography Techniques**: LSB modification for data hiding
- **Web Security**: Authentication and secure file handling
- **Full-Stack Development**: Complete web application architecture
- **Database Design**: Relational data modeling with SQLAlchemy

## 🔬 Technical Deep Dive

### RSA Implementation
- Uses Python's `cryptography` library for production-grade security
- OAEP padding with SHA-256 for optimal security
- Base64 encoding for data transmission
- Automatic key pair generation and storage

### Steganography Algorithm
- LSB (Least Significant Bit) modification technique
- Secret key-based message positioning
- Delimiter-based message boundary detection
- Support for various image formats

### Database Design
- Normalized schema design
- Foreign key relationships for data integrity
- Timestamp tracking for audit trails
- Efficient querying with SQLAlchemy ORM

## 🛠️ Development Features

### Code Quality
- Modular architecture with separation of concerns
- Comprehensive error handling and logging
- Input validation and sanitization
- Clean, documented code structure

### User Experience
- Intuitive interface design
- Real-time form validation
- Progress indicators and feedback
- Responsive design for mobile devices

## 📈 Future Enhancements

Potential improvements and extensions:
- AES encryption for larger messages (hybrid cryptography)
- Digital signatures for message authentication
- Advanced steganography techniques
- API endpoints for programmatic access
- Enhanced key management features

---

## 🏆 Project Defense Points

### Technical Complexity
- **Advanced Cryptography**: Implementation of RSA encryption with proper padding schemes
- **Image Processing**: Custom steganography algorithm with LSB manipulation
- **Database Integration**: Complete CRUD operations with relational data modeling
- **Security Implementation**: Multiple layers of security including authentication, validation, and encryption

### Innovation & Functionality
- **Dual Security Approach**: Combines traditional encryption with steganographic hiding
- **User-Centric Design**: Automatic key generation and management
- **Comprehensive Feature Set**: Full-stack application with multiple cryptographic capabilities
- **Production-Ready**: PostgreSQL integration, error handling, and scalable architecture

### Educational & Practical Value
- **Real-World Application**: Practical implementation of cryptographic concepts
- **Security Awareness**: Demonstrates various security techniques and best practices
- **Technical Skills**: Full-stack development with modern frameworks and libraries
- **Documentation**: Comprehensive documentation and code organization

This CryptoSecure application represents a sophisticated implementation of cryptographic principles in a practical web application, demonstrating both technical proficiency and understanding of security concepts.