# 🚀 START HERE - One-Command Launch

Get the Vehicle Repair Database running with **ONE COMMAND**!

---

## ⚡ Quick Start

### **Windows**
```batch
launch.bat
```

### **Mac/Linux**
```bash
./launch.sh
```

**That's it!** Everything else is automatic:
- ✅ Creates configuration files
- ✅ Sets up Python virtual environment
- ✅ Installs all dependencies
- ✅ Starts backend API
- ✅ Starts frontend app
- ✅ Opens your browser automatically
- ✅ Runs in background

---

## 📍 What You Get

After running the launcher:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Full web interface |
| **API Docs** | http://localhost:8000/docs | Interactive API testing |
| **API** | http://localhost:8000 | REST API endpoints |
| **Health** | http://localhost:8000/health | Status check |

---

## 🛑 Stop Services

### **Windows**
```batch
stop.bat
```

### **Mac/Linux**
```bash
./stop.sh
```

---

## 📋 First Time Setup

The launcher handles everything automatically on first run:

1. **Initial launch (~3-5 minutes)**:
   - Creates `.env` configuration
   - Installs Python packages
   - Installs Node.js packages
   - Starts all services

2. **Subsequent launches (~5 seconds)**:
   - Skips installation (already done)
   - Just starts the services

---

## 🔍 View Logs

All logs are saved in the `logs/` directory:

```bash
# Backend logs
tail -f logs/backend.log

# Frontend logs
tail -f logs/frontend.log
```

**Windows:**
```batch
type logs\backend.log
type logs\frontend.log
```

---

## ⚙️ What It Does Behind the Scenes

The launcher automatically:

1. ✅ Checks if Python and Node.js are installed
2. ✅ Creates `.env` from template if missing
3. ✅ Creates Python virtual environment
4. ✅ Installs Python dependencies (first time only)
5. ✅ Installs Node.js packages (first time only)
6. ✅ Kills any old processes
7. ✅ Starts backend API server
8. ✅ Starts frontend dev server
9. ✅ Verifies services are running
10. ✅ Opens browser automatically

**All complexity hidden - just one command!**

---

## 🎯 Common Use Cases

### Daily Development
```bash
# Start working
./launch.sh

# Code changes auto-reload!

# When done
./stop.sh
```

### Quick API Test
```bash
# Just need the API?
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Full Reset
```bash
# Stop everything
./stop.sh

# Delete and recreate
rm -rf backend/venv frontend/node_modules
./launch.sh
```

---

## 🐛 Troubleshooting

### "Port already in use"
```bash
# Stop services first
./stop.sh

# Then launch again
./launch.sh
```

### "Python not found"
Install Python 3.11+ from:
- **Windows**: https://www.python.org/downloads/
- **Mac**: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11`

### "Node not found"
Frontend won't work, but API will still run.

Install Node.js 18+ from:
- https://nodejs.org/

### Services not starting
Check logs:
```bash
cat logs/backend.log
cat logs/frontend.log
```

---

## 📚 More Documentation

If you need more control or want to customize:

- **QUICKSTART.md** - Detailed 5-minute guide
- **DEPLOYMENT.md** - Deploy to cloud platforms
- **setup-windows.bat** - Interactive setup wizard
- **setup-unix.sh** - Interactive setup wizard
- **README.md** - Full project documentation

---

## 💡 Pro Tips

1. **Auto-reload**: Both backend and frontend reload on code changes
2. **Multiple terminals**: Services run in background, terminal stays available
3. **Logs directory**: All logs saved automatically
4. **Clean stop**: Always use `stop.sh`/`stop.bat` to cleanly stop services
5. **Fast restart**: After first run, launching takes ~5 seconds

---

## ✅ Success Checklist

After running `launch.sh` or `launch.bat`:

- [x] Configuration file created
- [x] Dependencies installed
- [x] Backend API running
- [x] Frontend app running
- [x] Browser opened automatically
- [x] Ready to code!

---

## 🎉 You're All Set!

**Just run: `./launch.sh` or `launch.bat`**

Everything else is automatic!

---

## 📞 Need Help?

- Check logs: `logs/backend.log`, `logs/frontend.log`
- Read QUICKSTART.md for detailed steps
- See DEPLOYMENT.md for cloud hosting
- Open an issue on GitHub

**Happy coding! 🚗💨**
