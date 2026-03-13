"""
Vercel serverless function entry point for FastAPI
"""
from main import app

# Vercel requires a handler function
handler = app

