"""
Vercel serverless function entry point for FastAPI
"""
from mangum import Mangum
from main import app

# Mangum adapter for ASGI apps on Vercel
handler = Mangum(app, lifespan="off")

