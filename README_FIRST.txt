========================================
COLD-CHAIN EXPIRY ACCELERATOR
Quick Start Guide
========================================

SUPER SIMPLE 6-STEP INSTALLATION:

1. Double-click:  setup.bat
   (Wait for it to finish)

2. Double-click:  .env
   Change YOUR_MYSQL_PASSWORD to your real password
   Save and close

3. Open MySQL Workbench
   Run: CREATE DATABASE cold_chain_db;

4. Double-click:  init.bat
   (Creates database tables)

5. Double-click:  seed.bat
   (Loads sample data - OPTIONAL)

6. Double-click:  start.bat
   (Starts the application)

7. Open browser:  http://localhost:5000

========================================

THAT'S IT! 🎉

Daily usage: Just double-click start.bat

For detailed help: Open INSTALL_GUIDE.md

========================================

TROUBLESHOOTING:

❌ "Python not found"
   → Install Python from python.org

❌ "MySQL connection error"  
   → Check password in .env file
   → Make sure MySQL is running

❌ "Module not found"
   → Run setup.bat again

========================================

FILES YOU'LL USE:

✅ setup.bat   - First time setup
✅ .env        - Edit your MySQL password here
✅ init.bat    - Create database tables
✅ seed.bat    - Load sample data (optional)
✅ start.bat   - Start the application

========================================
