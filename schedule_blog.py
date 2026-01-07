"""
Windows Task Scheduler script to run daily blog post generation at 12:00 PM
This script can be used with Windows Task Scheduler or as a standalone scheduler
"""
import subprocess
import sys
import os
from pathlib import Path

# Get the backend directory
BACKEND_DIR = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable
MANAGE_PY = BACKEND_DIR / "manage.py"

def generate_blog_post():
    """Run the daily blog post generation command"""
    try:
        # Change to backend directory
        os.chdir(BACKEND_DIR)
        
        # Run the management command
        result = subprocess.run(
            [PYTHON_EXE, str(MANAGE_PY), "generate_daily_blog"],
            capture_output=True,
            text=True,
            cwd=BACKEND_DIR
        )
        
        if result.returncode == 0:
            print("Blog post generated successfully!")
            print(result.stdout)
        else:
            print("Error generating blog post:")
            print(result.stderr)
            return False
        
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    generate_blog_post()

