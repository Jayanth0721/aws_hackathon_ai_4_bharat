# Credentials & User Management - Ashoka Platform

Complete guide to user accounts, roles, and authentication.

## Default User Accounts

### Admin Account
```
Username: admin
Password: admin123
Role: admin
Email: admin@ashoka.ai
```

**Capabilities:**
- Full platform access
- Security dashboard access
- User management
- System configuration
- All content features

**Security Tab:** ✅ Visible

### Demo Account
```
Username: demo
Password: demo123
Role: user
Email: demo@ashoka.ai
```

**Capabilities:**
- Content analysis
- Content generation
- Content transformation
- Monitoring view
- Alerts view

**Security Tab:** ❌ Hidden

---

## User Roles

### 1. User Role (Default)

**Access Level:** Standard

**Features:**
- ✅ Content Intelligence & Analysis
- ✅ AI Content Generator
- ✅ Multi-Platform Content Transformer
- ✅ Real-Time Monitoring (view only)
- ✅ Alerts & Notifications
- ❌ Security Dashboard
- ❌ User Management

**How to get:**
- Default role for new signups
- Select "User" during registration

### 2. Creator Role

**Access Level:** Enhanced

**Features:**
- ✅ All User role features
- ✅ Enhanced content creation tools
- ✅ Priority processing
- ❌ Security Dashboard
- ❌ User Management

**How to get:**
- Select "Creator" during registration
- Cannot be self-assigned after signup

### 3. Admin Role

**Access Level:** Full

**Features:**
- ✅ All User role features
- ✅ All Creator role features
- ✅ Security Dashboard
- ✅ Login activity monitoring
- ✅ Security event tracking
- ✅ User management
- ✅ System configuration

**How to get:**
- Pre-configured (admin account)
- Cannot be selected during signup
- Must be assigned by existing admin

### 4. Operator Role (Reserved)

**Access Level:** System

**Features:**
- System operations
- Maintenance tasks
- Reserved for future use

**How to get:**
- Not available via signup
- System-assigned only

---

## Authentication Flow

### 1. Login Process

```
1. Enter username and password
   ↓
2. System validates credentials
   ↓
3. OTP generated (5-digit code)
   ↓
4. OTP displayed in console
   ↓
5. User enters OTP
   ↓
6. System verifies OTP
   ↓
7. Session created
   ↓
8. Redirect to dashboard
```

### 2. OTP Details

**Generation:**
- 5-digit random code
- Generated after successful password verification
- Displayed in terminal/console

**Expiration:**
- Valid for 5 minutes
- Must be used before expiration
- New OTP required after expiration

**Security:**
- One-time use only
- Cannot be reused
- Invalidated after successful verification

### 3. Session Management

**Session Duration:**
- Default: 30 minutes
- Configurable: 15, 30, 60, or 120 minutes
- Extends on activity

**Session Storage:**
- Stored in DuckDB
- Includes: token, user_id, timestamps
- Tracked for security monitoring

**Session Termination:**
- Automatic after timeout
- Manual via logout
- Invalidated on security events

---

## Creating New Users

### Via Signup Page

**Steps:**
1. Navigate to login page
2. Click "Sign Up" tab
3. Fill in details:
   - Username (unique)
   - Email
   - Password
   - Role (User or Creator)
4. Click "Sign Up"
5. Login with new credentials

**Validation:**
- Username must be unique
- Email format validated
- Password minimum length
- Role must be User or Creator

### Via Python Code

```python
from src.services.auth_service import auth_service

# Create user
success, message = auth_service.signup(
    username="john_doe",
    email="john@ashoka.ai",
    password="secure_password_123",
    role="user"  # or "creator"
)

if success:
    print(f"User created: {message}")
else:
    print(f"Error: {message}")
```

### Via Database Direct Insert

```python
import duckdb
import bcrypt
from datetime import datetime

conn = duckdb.connect('data/ashoka.duckdb')

# Hash password
password_hash = bcrypt.hashpw(
    "password123".encode('utf-8'),
    bcrypt.gensalt()
).decode('utf-8')

# Insert user
conn.execute("""
    INSERT INTO ashoka_users 
    (user_id, username, password_hash, email, created_at, is_active, role)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    "user_newuser",
    "newuser",
    password_hash,
    "newuser@ashoka.ai",
    datetime.now(),
    True,
    "user"
])

conn.close()
print("User created successfully")
```

---

## User Management

### View All Users

```python
import duckdb

conn = duckdb.connect('data/ashoka.duckdb')

users = conn.execute("""
    SELECT user_id, username, email, role, created_at, is_active
    FROM ashoka_users
    ORDER BY created_at DESC
""").fetchall()

for user in users:
    print(f"Username: {user[1]}, Role: {user[3]}, Active: {user[5]}")

conn.close()
```

### Change User Role

```python
from src.services.auth_service import auth_service

# Change role (admin only)
success, message = auth_service.set_user_role(
    user_id="user_john_doe",
    role="creator"  # or "admin", "operator"
)

print(message)
```

### Deactivate User

```python
import duckdb

conn = duckdb.connect('data/ashoka.duckdb')

conn.execute("""
    UPDATE ashoka_users
    SET is_active = FALSE
    WHERE username = ?
""", ["username_to_deactivate"])

conn.close()
```

### Reset User Password

```python
import duckdb
import bcrypt

conn = duckdb.connect('data/ashoka.duckdb')

# Hash new password
new_password_hash = bcrypt.hashpw(
    "new_password_123".encode('utf-8'),
    bcrypt.gensalt()
).decode('utf-8')

# Update password
conn.execute("""
    UPDATE ashoka_users
    SET password_hash = ?
    WHERE username = ?
""", [new_password_hash, "username"])

conn.close()
print("Password reset successfully")
```

---

## Security Best Practices

### For Users

1. **Strong Passwords**
   - Minimum 8 characters
   - Mix of letters, numbers, symbols
   - Avoid common words
   - Don't reuse passwords

2. **OTP Security**
   - Don't share OTP codes
   - Enter OTP quickly (5-minute expiration)
   - Verify you're on correct login page

3. **Session Management**
   - Logout when done
   - Don't share session tokens
   - Use private/incognito for shared computers

4. **Account Security**
   - Change default passwords
   - Monitor login activity (admin)
   - Report suspicious activity

### For Administrators

1. **User Management**
   - Review user accounts regularly
   - Deactivate unused accounts
   - Audit role assignments
   - Monitor failed login attempts

2. **Security Monitoring**
   - Check security dashboard daily
   - Review login patterns
   - Investigate failed logins
   - Track security events

3. **Access Control**
   - Limit admin role assignments
   - Use principle of least privilege
   - Regular access reviews
   - Document role changes

4. **Data Protection**
   - Regular database backups
   - Secure .env file
   - Protect API keys
   - Monitor data access

---

## Troubleshooting

### "Invalid username or password"
- Verify username spelling
- Check password (case-sensitive)
- Ensure account is active
- Try default accounts (admin/demo)

### "OTP expired"
- OTP valid for 5 minutes only
- Login again to generate new OTP
- Check system time is correct

### "Invalid OTP code"
- Verify 5-digit code from console
- Check for typos
- Ensure using latest OTP
- Don't reuse old OTPs

### "Username already exists"
- Choose different username
- Check for existing account
- Contact admin if needed

### "Session expired"
- Login again
- Check session timeout setting
- Verify network connection

### "Access denied" (Security tab)
- Only admin role can access
- Verify your role in profile
- Contact admin for role change

---

## API Key Management

### Google Gemini API Key

**Location:** `.env` file
```
GOOGLE_API_KEY=your_api_key_here
```

**Security:**
- Never commit to version control
- Keep .env file private
- Rotate keys periodically
- Monitor API usage

**Getting a key:**
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into .env

---

## Data Privacy

### User Data Stored

- Username (unique identifier)
- Email address
- Password hash (bcrypt)
- Role assignment
- Account creation date
- Last login timestamp
- Session information

### Content Data Stored

- Analyzed text content
- Analysis results
- Transformation history
- Upload metadata
- Timestamps

### Security Data Stored (Admin only)

- Login attempts
- IP addresses
- Device information
- Security events
- Session tokens

### Data Retention

- User accounts: Indefinite (until deleted)
- Sessions: 30 days after expiration
- Content: Indefinite (user-managed)
- Logs: 90 days

### Data Deletion

Users can request data deletion by:
1. Contacting administrator
2. Admin removes user from database
3. Associated data is cascade deleted

---

## Compliance

### Password Storage
- Bcrypt hashing (industry standard)
- Salt per password
- No plaintext storage

### Session Security
- Secure token generation
- Expiration enforcement
- Activity tracking

### Access Logging
- All login attempts logged
- Security events tracked
- Audit trail maintained

---

## Support

For account issues:
1. Try default credentials (admin/demo)
2. Check SETUP.md for configuration
3. Review this documentation
4. Check database connectivity
5. Verify .env configuration
