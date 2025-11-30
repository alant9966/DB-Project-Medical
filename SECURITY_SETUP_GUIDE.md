# Security Setup Guide: SQL Roles & Permissions

## What Are SQL Roles and Permissions?

### Roles
A **role** in SQL is like a job title with specific responsibilities. In MySQL, we implement roles using separate database users, where each user represents a different role:

- **Application User** - The account your Flask app uses to interact with the database
- **Read-Only User** - An account that can only view data (for reports/analytics)
- **Backup User** - An account specifically for creating database backups

### Permissions (Privileges)
**Permissions** control what actions each role can perform:

- **SELECT** - Read data from tables
- **INSERT** - Add new records
- **UPDATE** - Modify existing records
- **DELETE** - Remove records
- **CREATE/DROP** - Create or delete tables (dangerous!)
- **GRANT** - Give permissions to other users

## Why This Matters for Your Project

### Current Security Issues ❌

1. **Using Root User**: Your [config.py](config.py#L2) connects as `root` - the superuser with unlimited power
2. **No Access Control**: Anyone who accesses the database can do ANYTHING
3. **Security Risk**: If your app is hacked, attackers have full database control
4. **Violates Best Practices**: Production apps should NEVER use root

### What Should Be Fixed ✅

You need to implement the **Principle of Least Privilege**:
> "Every user should have the minimum permissions needed to do their job, and nothing more."

## How to Fix It

### Step 1: Run the Security Setup SQL

Execute the permissions file to create dedicated users:

```bash
mysql -u root -p < database/SECURITY_ROLES_PERMISSIONS.sql
```

This creates three users:
1. `medical_app_user` - For your Flask application (limited permissions)
2. `medical_readonly_user` - For reports/analytics (read-only)
3. `medical_backup_user` - For database backups

### Step 2: Update Your Configuration

Replace your current [config.py](config.py) with the secure version:

**❌ Current (INSECURE):**
```python
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
```

**✅ Should Be (SECURE):**
```python
MYSQL_USER = 'medical_app_user'
MYSQL_PASSWORD = 'secure_app_password_2024'  # Change this!
```

### Step 3: Change Default Passwords

The default passwords in `SECURITY_ROLES_PERMISSIONS.sql` are placeholders. Change them:

```sql
-- In MySQL command line:
ALTER USER 'medical_app_user'@'localhost' IDENTIFIED BY 'your-strong-password-here';
```

### Step 4: Test the Connection

Verify your app can connect with the new user:

```bash
python -c "from app import mysql; print('Connection successful!')"
```

## What Each User Can Do

### medical_app_user (Your Flask App)

**CAN:**
- ✅ Read all tables (SELECT)
- ✅ Create new users, patients, doctors, appointments (INSERT)
- ✅ Update patient info, doctor info, appointments (UPDATE)
- ✅ Delete appointments and user accounts (DELETE)

**CANNOT:**
- ❌ Drop or alter tables
- ❌ Delete medical records or treatments (intentionally restricted)
- ❌ Access other databases
- ❌ Create new users or grant permissions

### medical_readonly_user (Reports/Analytics)

**CAN:**
- ✅ Read all tables (SELECT)

**CANNOT:**
- ❌ Modify any data
- ❌ Insert, update, or delete anything

### medical_backup_user (Backups)

**CAN:**
- ✅ Read all data for backup
- ✅ Lock tables during backup
- ✅ Reload privileges

**CANNOT:**
- ❌ Modify data
- ❌ Drop tables

## Verification Commands

Check what permissions each user has:

```sql
-- Show permissions for app user
SHOW GRANTS FOR 'medical_app_user'@'localhost';

-- Show permissions for readonly user
SHOW GRANTS FOR 'medical_readonly_user'@'localhost';

-- Show permissions for backup user
SHOW GRANTS FOR 'medical_backup_user'@'localhost';
```

## Real-World Example

Imagine a hospital database gets hacked:

### Scenario 1: Using Root (Your Current Setup) ⚠️
```
Hacker gains access → Has root privileges → Can:
  - Delete all patient records
  - Drop entire database
  - Access financial data
  - Create backdoor admin users
  - Destroy everything
```

### Scenario 2: Using Limited User (After Fix) ✅
```
Hacker gains access → Has limited privileges → Can:
  - Read patient data (still bad, but...)
  - Modify some records

Cannot:
  - Drop tables or database
  - Delete medical records (we restricted this!)
  - Access other databases
  - Grant themselves more permissions
```

**Damage is limited!** This is called "defense in depth."

## Best Practices for Class Project

### For Your Submission ✅

1. **Include this file** to show you understand security
2. **Document the changes** in your project report:
   - What roles you created
   - Why each role has specific permissions
   - How it improves security

3. **Explain the principle of least privilege**:
   - "We don't use root because..."
   - "Each user only has permissions they need..."

4. **Show verification** - Include output of `SHOW GRANTS`

### Bonus Points 🌟

Add application-level security too:
- ✅ Your app already checks `current_user.role` (good!)
- ✅ You verify patients can only edit their own data ([app.py:341](app.py#L341))
- ✅ You use parameterized queries to prevent SQL injection

## Common Questions

**Q: Why can't medical_app_user drop tables?**
A: Your application should never need to drop tables. That's done during development or migrations, not during normal operation.

**Q: Why restrict DELETE on medical records?**
A: Medical records have legal/compliance requirements. They often need to be kept for years. If deletion is needed, it should be an administrative function with audit trails.

**Q: What if I need to make schema changes?**
A: Use the root account for database migrations/changes, but NEVER for normal app operations.

**Q: Is this enough for HIPAA compliance?**
A: No - HIPAA requires encryption, audit logs, access controls, and much more. This is just one piece of a comprehensive security strategy.

## Additional Resources

- [MySQL Security Best Practices](https://dev.mysql.com/doc/refman/8.0/en/security-guidelines.html)
- [OWASP Database Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html)
- [Principle of Least Privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)

## Summary for Your Teammate

When your teammate asks about "SQL roles and permissions," you can say:

> "I created separate MySQL users with limited permissions instead of using root. The application user can read/write data but cannot drop tables or alter the schema. I also created a read-only user for reports and a backup user. This implements the principle of least privilege and improves security by limiting potential damage if the application is compromised."

Then show them [SECURITY_ROLES_PERMISSIONS.sql](database/SECURITY_ROLES_PERMISSIONS.sql) and this guide!
