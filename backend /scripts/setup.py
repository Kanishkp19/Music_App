"""Automated setup script for development environment"""
import subprocess
import sys
import os

def run_command(command):
    """Run shell command and handle errors"""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 Setting up MuseAIka development environment...")
    
    # Install dependencies
    if run_command("pip install -r requirements.txt"):
        print("✅ Dependencies installed")
    else:
        print("❌ Failed to install dependencies")
        return
    
    # Copy environment file
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        run_command("cp .env.example .env")
        print("✅ Environment file created")
    
    print("🎉 Setup complete! Edit .env with your configuration.")

if __name__ == "__main__":
    main()
