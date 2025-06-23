import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Message, SteganographyOperation
from crypto_utils import CryptoUtils
from steganography import SteganographyUtils
import uuid

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper function for allowed file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')
        
        try:
            # Generate RSA keys for the user
            private_key, public_key = CryptoUtils.generate_rsa_keys()
            
            # Create new user
            user = User(
                username=username,
                email=email,
                rsa_private_key=private_key,
                rsa_public_key=public_key
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.created_at.desc()).limit(5).all()
    stego_ops = SteganographyOperation.query.filter_by(user_id=current_user.id).order_by(SteganographyOperation.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', messages=messages, stego_ops=stego_ops)

@app.route('/encrypt', methods=['GET', 'POST'])
@login_required
def encrypt():
    """Encrypt message"""
    if request.method == 'POST':
        message = request.form['message']
        
        if not message:
            flash('Message is required.', 'danger')
            return render_template('encrypt.html')
        
        try:
            # Encrypt message using user's public key
            encrypted_message = CryptoUtils.encrypt_message(message, current_user.rsa_public_key)
            
            # Generate MD5 hash
            md5_hash = CryptoUtils.generate_md5_hash(message)
            
            # Save to database
            msg_record = Message(
                user_id=current_user.id,
                original_message=message,
                encrypted_message=encrypted_message,
                md5_hash=md5_hash
            )
            db.session.add(msg_record)
            db.session.commit()
            
            flash('Message encrypted successfully!', 'success')
            return render_template('encrypt.html', 
                                 encrypted_message=encrypted_message, 
                                 md5_hash=md5_hash,
                                 original_message=message)
        except Exception as e:
            flash(f'Encryption failed: {str(e)}', 'danger')
    
    return render_template('encrypt.html')

@app.route('/decrypt', methods=['GET', 'POST'])
@login_required
def decrypt():
    """Decrypt message"""
    if request.method == 'POST':
        encrypted_message = request.form['encrypted_message']
        expected_hash = request.form.get('expected_hash', '')
        
        if not encrypted_message:
            flash('Encrypted message is required.', 'danger')
            return render_template('decrypt.html')
        
        try:
            # Decrypt message using user's private key
            decrypted_message = CryptoUtils.decrypt_message(encrypted_message, current_user.rsa_private_key)
            
            # Verify MD5 hash if provided
            hash_valid = None
            if expected_hash:
                hash_valid = CryptoUtils.verify_md5_hash(decrypted_message, expected_hash)
            
            flash('Message decrypted successfully!', 'success')
            return render_template('decrypt.html', 
                                 decrypted_message=decrypted_message,
                                 hash_valid=hash_valid,
                                 encrypted_message=encrypted_message)
        except Exception as e:
            flash(f'Decryption failed: {str(e)}', 'danger')
    
    return render_template('decrypt.html')

@app.route('/steganography', methods=['GET', 'POST'])
@login_required
def steganography():
    """Hide message in image"""
    if request.method == 'POST':
        message = request.form['message']
        secret_key = request.form['secret_key']
        
        if 'image' not in request.files:
            flash('No image file selected.', 'danger')
            return render_template('steganography.html')
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No image file selected.', 'danger')
            return render_template('steganography.html')
        
        if not message or not secret_key:
            flash('Message and secret key are required.', 'danger')
            return render_template('steganography.html')
        
        if file and allowed_file(file.filename):
            try:
                # Save uploaded file
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                
                # Create output filename
                output_filename = f"stego_{unique_filename}"
                output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
                
                # Hide message in image
                SteganographyUtils.hide_message_in_image(filepath, message, secret_key, output_path)
                
                # Save operation to database
                stego_op = SteganographyOperation(
                    user_id=current_user.id,
                    original_filename=unique_filename,
                    modified_filename=output_filename,
                    secret_message=message,
                    secret_key=secret_key
                )
                db.session.add(stego_op)
                db.session.commit()
                
                flash('Message hidden in image successfully!', 'success')
                return render_template('steganography.html', 
                                     success=True,
                                     output_filename=output_filename)
            except Exception as e:
                flash(f'Steganography failed: {str(e)}', 'danger')
        else:
            flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files.', 'danger')
    
    return render_template('steganography.html')

@app.route('/extract', methods=['GET', 'POST'])
@login_required
def extract():
    """Extract message from image"""
    if request.method == 'POST':
        secret_key = request.form['secret_key']
        
        if 'image' not in request.files:
            flash('No image file selected.', 'danger')
            return render_template('extract.html')
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No image file selected.', 'danger')
            return render_template('extract.html')
        
        if not secret_key:
            flash('Secret key is required.', 'danger')
            return render_template('extract.html')
        
        if file and allowed_file(file.filename):
            try:
                # Save uploaded file
                filename = secure_filename(file.filename)
                unique_filename = f"extract_{uuid.uuid4()}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                
                # Extract message from image
                extracted_message = SteganographyUtils.extract_message_from_image(filepath, secret_key)
                
                # Clean up uploaded file
                os.remove(filepath)
                
                flash('Message extracted successfully!', 'success')
                return render_template('extract.html', 
                                     extracted_message=extracted_message)
            except Exception as e:
                # Clean up uploaded file if it exists
                if 'filepath' in locals() and os.path.exists(filepath):
                    os.remove(filepath)
                flash(f'Message extraction failed: {str(e)}', 'danger')
        else:
            flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files.', 'danger')
    
    return render_template('extract.html')

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    """Download processed image"""
    # Verify user owns this file
    stego_op = SteganographyOperation.query.filter_by(
        user_id=current_user.id,
        modified_filename=filename
    ).first()
    
    if stego_op:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        flash('File not found or access denied.', 'danger')
        return redirect(url_for('dashboard'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
