# CryptoSecure App - Project Documentation

## Overview
A comprehensive Flask web application providing advanced cryptographic capabilities including RSA encryption, MD5 hashing, user authentication, and image steganography. The application demonstrates practical implementation of security concepts with a modern web interface.

**Current Status**: Fully functional with all core features implemented and tested.

## Project Architecture

### Core Components
- **Flask Backend**: Main application with SQLAlchemy ORM
- **PostgreSQL Database**: Production-ready data persistence
- **Cryptographic Engine**: RSA encryption/decryption with 2048-bit keys
- **Steganography Module**: LSB-based message hiding in images
- **Authentication System**: User registration/login with secure password hashing

### Key Features Implemented
- User authentication with automatic RSA key pair generation
- Message encryption/decryption with MD5 integrity verification
- Image steganography for hiding/extracting secret messages
- Responsive Bootstrap-based UI with dark theme
- Comprehensive error handling and validation

### Security Implementation
- RSA 2048-bit encryption with OAEP padding
- Werkzeug password hashing
- File upload validation and sanitization
- Session management with Flask-Login
- Input validation on client and server sides

## Recent Changes

### December 23, 2025
- Fixed missing error templates (404.html, 500.html)
- Resolved Feather icon issue by replacing 'dashboard' with 'grid'
- Created comprehensive README.md for project defense
- Application is fully functional with all features working

### Initial Implementation
- Set up Flask application with PostgreSQL integration
- Implemented complete user authentication system
- Built RSA encryption/decryption functionality
- Added image steganography capabilities
- Created responsive web interface with Bootstrap

## Technical Specifications

### Database Schema
- **Users**: Authentication, RSA keys, user metadata
- **Messages**: Encrypted messages with MD5 hashes
- **SteganographyOperations**: File processing history

### File Structure
```
├── app.py              # Flask configuration and database setup
├── main.py             # Application entry point
├── routes.py           # URL routing and business logic
├── models.py           # Database models
├── crypto_utils.py     # RSA and MD5 utilities
├── steganography.py    # Image processing utilities
├── templates/          # HTML templates with Jinja2
├── static/            # CSS, JavaScript, and assets
└── uploads/           # File upload directory
```

## User Preferences
- Professional communication style preferred
- Focus on security and technical implementation
- Comprehensive documentation required
- Production-ready code standards

## Deployment Notes
- Uses PostgreSQL database with environment variables
- Configured for Replit deployment with proper port binding
- File uploads limited to 16MB with validation
- Session management configured for production use

## Future Enhancements
- Hybrid encryption for larger messages (RSA + AES)
- Digital signatures for message authentication
- API endpoints for programmatic access
- Enhanced key management features