"""Script to run both backend and frontend."""
import subprocess
import sys
import time
import os


def run_backend():
    """Start the FastAPI backend server."""
    print("Starting backend server on http://localhost:8000...")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )


def run_frontend():
    """Start the Streamlit frontend."""
    print("Starting frontend on http://localhost:8501...")
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )


def main():
    """Main function to run both services."""
    print("=" * 60)
    print("SRM Application - Starting Backend and Frontend")
    print("=" * 60)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = run_backend()
        time.sleep(2)  # Wait for backend to start
        
        # Start frontend
        frontend_process = run_frontend()
        
        print("\n" + "=" * 60)
        print("Services started successfully!")
        print("Backend API: http://localhost:8000")
        print("Frontend UI: http://localhost:8501")
        print("API Docs: http://localhost:8000/docs")
        print("=" * 60)
        print("\nPress Ctrl+C to stop all services...\n")
        
        # Wait for processes
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\n\nStopping services...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("Services stopped.")
    except Exception as e:
        print(f"Error: {e}")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()


if __name__ == "__main__":
    main()


