# Start backend with proper environment variables
& .\.venv\Scripts\Activate.ps1
$env:DEBUG = "true"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
