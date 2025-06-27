#!/bin/bash

# Hospital Chatbot Cleanup Script
# This script cleans up temporary files and cache directories

echo "🧹 Cleaning up Hospital Chatbot project..."

# Remove Python cache files
echo "🗑️  Removing Python cache files..."
find . -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -not -path "./.venv/*" -delete 2>/dev/null || true
find . -name "*.pyo" -not -path "./.venv/*" -delete 2>/dev/null || true

# Remove log files
echo "🗑️  Removing log files..."
find . -name "*.log" -not -path "./.venv/*" -delete 2>/dev/null || true

# Remove temporary files
echo "🗑️  Removing temporary files..."
find . -name "*.tmp" -not -path "./.venv/*" -delete 2>/dev/null || true
find . -name ".DS_Store" -delete 2>/dev/null || true

echo "✅ Cleanup completed!"
echo ""
echo "Project is now clean and organized! 🎉" 