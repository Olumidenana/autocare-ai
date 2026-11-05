"""
Vercel Serverless Function Handler for AutoCare AI.
Routes all Vercel incoming HTTP requests directly into the FastAPI application.
"""

import sys
from pathlib import Path

# Ensure root directory is on PYTHONPATH for Vercel serverless environment
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.main import app
