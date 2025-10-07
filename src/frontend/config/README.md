# Authentication Configuration

## Default User Credentials

This system comes with three pre-configured user accounts:

### 🔐 User Accounts

| Username | Password | Role | Description |
|----------|----------|------|-------------|
| `admin` | `churn123` | Administrator | Full system access |
| `demo` | `demo123` | Demo User | Standard access for demonstrations |
| `user` | `user123` | Standard User | Standard access for regular users |

## 🔒 Security Features

- **Password Hashing**: All passwords are stored as SHA-256 hashes
- **Session Management**: Secure session-based authentication
- **Page Protection**: All pages require authentication
- **User Management**: Add/remove users via configuration file

## 📝 User Management

### Adding New Users

1. Generate password hash:
   ```python
   import hashlib
   password = "your_new_password"
   hashed = hashlib.sha256(password.encode()).hexdigest()
   print(hashed)
   ```

2. Add to `users.json`:
   ```json
   {
     "existing_users": "...",
     "new_username": "generated_hash_here"
   }
   ```

### Removing Users

Simply delete the username entry from `users.json`.

### Changing Passwords

1. Generate new hash using the method above
2. Replace the existing hash in `users.json`

## 🛡️ Best Practices

- **Change Default Passwords**: Update default passwords before production use
- **Strong Passwords**: Use complex passwords with mixed characters
- **Regular Updates**: Periodically update user credentials
- **Backup Configuration**: Keep secure backups of user configurations
- **Environment Variables**: Consider using environment variables for sensitive data

## 🔧 Advanced Configuration

For production deployment, consider:

- **Database Authentication**: Integrate with existing user databases
- **LDAP/Active Directory**: Enterprise authentication systems  
- **OAuth Integration**: Social login providers
- **Multi-Factor Authentication**: Additional security layers
- **Session Timeout**: Automatic logout after inactivity

## 📁 File Structure
```
src/frontend/config/
├── users.json          # User credentials (hashed passwords)
└── README.md           # This documentation file
```

## ⚠️ Security Warnings

- **Never commit plain text passwords** to version control
- **Keep users.json secure** - restrict file permissions
- **Use HTTPS** in production environments
- **Regular security audits** of user access logs
- **Monitor failed login attempts** for security threats