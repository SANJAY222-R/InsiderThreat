# Project Cleanup & Environment Reset Guide

This guide provides step-by-step instructions and scripts to remove all Python packages, Node.js packages, build artifacts, temporary databases, logs, and `PYTHONPATH` configurations in WSL once you are finished working with the Insider Threat Detection project.

---

## 1. Remove / Revert `PYTHONPATH` from WSL `~/.bashrc`

If you added `PYTHONPATH` or project aliases to your `~/.bashrc`, run the following commands to remove them cleanly:

```bash
# Remove all lines mentioning 'InsiderThreat' from ~/.bashrc
sed -i '/InsiderThreat/d' ~/.bashrc

# Unset PYTHONPATH for the current active terminal session
unset PYTHONPATH

# Reload ~/.bashrc configuration
source ~/.bashrc
```

---

## 2. Remove Node.js Packages & Build Artifacts

To delete the `node_modules` directory, compiled production bundles, Vite cache, and purge the global npm cache:

```bash
# 1. Delete node_modules, build output, and Vite cache
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/node_modules
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/dist
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/.vite

# 2. Clear global npm cache to free up disk space in WSL
npm cache clean --force
```

---

## 3. Uninstall Python Packages

### Option A: Uninstall directly via `requirements.txt`
```bash
cd /mnt/c/Users/HP/Desktop/InsiderThreat
pip uninstall -y -r backend/requirements.txt
```

### Option B: Cleanly uninstall all specific packages installed for this project
```bash
pip uninstall -y \
  fastapi \
  uvicorn \
  sqlalchemy \
  pydantic \
  pydantic-settings \
  bcrypt \
  pyjwt \
  python-multipart \
  loguru \
  websockets \
  networkx \
  pandas \
  pyyaml \
  httpx \
  torch \
  torchvision \
  torchaudio \
  scikit-learn \
  requests
```

### Option C: Purge Pip Cache
```bash
pip cache purge
```

---

## 4. Remove Generated Database, Logs, and Bytecode (Optional)

To delete local SQLite database files, logs, and Python `__pycache__` folders:

```bash
cd /mnt/c/Users/HP/Desktop/InsiderThreat

# Remove local SQLite database and generated logs
rm -f insider_threat.db
rm -rf logs/

# Remove Python __pycache__ directories and .pyc files
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

---

## 5. All-in-One Complete Teardown Script

You can copy and run this single block to perform a full system cleanup in one command:

```bash
#!/bin/bash
set -e

echo "=== Starting Insider Threat Project Teardown ==="

# 1. Clean Node packages & build cache
echo "[1/4] Cleaning Node.js packages and cache..."
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/node_modules
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/dist
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/.vite
npm cache clean --force 2>/dev/null || true

# 2. Uninstall Python packages & purge pip cache
echo "[2/4] Uninstalling Python dependencies..."
pip uninstall -y -r /mnt/c/Users/HP/Desktop/InsiderThreat/backend/requirements.txt 2>/dev/null || true
pip uninstall -y networkx pandas pyyaml 2>/dev/null || true
pip cache purge

# 3. Clean temporary files, database, and bytecode
echo "[3/4] Cleaning temporary runtime artifacts..."
find /mnt/c/Users/HP/Desktop/InsiderThreat -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find /mnt/c/Users/HP/Desktop/InsiderThreat -type f -name "*.pyc" -delete 2>/dev/null || true
rm -f /mnt/c/Users/HP/Desktop/InsiderThreat/insider_threat.db
rm -rf /mnt/c/Users/HP/Desktop/InsiderThreat/logs

# 4. Revert PYTHONPATH from ~/.bashrc
echo "[4/4] Removing PYTHONPATH from ~/.bashrc..."
sed -i '/InsiderThreat/d' ~/.bashrc
unset PYTHONPATH
source ~/.bashrc

echo "=== Cleanup Complete! All project packages, caches, and path configurations have been removed. ==="
```

---

## 6. Verification Commands

To verify that the environment has been completely reset:

```bash
# Check if PYTHONPATH is cleared
echo $PYTHONPATH

# Check if node_modules is deleted
ls -la /mnt/c/Users/HP/Desktop/InsiderThreat/frontend/node_modules

# Check if backend packages are uninstalled
python3 -c "import fastapi" 2>&1
```
