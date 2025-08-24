#!/usr/bin/env python3
"""
Setup script for Minecraft Farm Bot
Installs dependencies and sets up the environment
Made by DDS
"""

import subprocess
import sys
import os
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def print_banner():
    """Print setup banner"""
    print(f"{Fore.CYAN}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                MINECRAFT FARM BOT SETUP                       ║")
    print("║                     🛠️ Installation 🛠️                       ║")
    print("║                        Made by DDS                           ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

def check_python_version():
    """Check if Python version is compatible"""
    print(f"{Fore.YELLOW}Checking Python version...{Style.RESET_ALL}")
    
    if sys.version_info < (3, 7):
        print(f"{Fore.RED}Error: Python 3.7 or higher is required{Style.RESET_ALL}")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"{Fore.GREEN}✓ Python {sys.version.split()[0]} is compatible{Style.RESET_ALL}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print(f"\n{Fore.YELLOW}Installing dependencies...{Style.RESET_ALL}")
    
    dependencies = [
        'pyautogui==0.9.54',
        'opencv-python==4.8.1.78',
        'numpy==1.24.3',
        'pillow==10.0.1',
        'keyboard==0.13.5',
        'mouse==0.7.1',
        'colorama==0.4.6',
        'configparser==6.0.0'
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"{Fore.GREEN}✓ {dep} installed successfully{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}✗ Failed to install {dep}{Style.RESET_ALL}")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print(f"\n{Fore.YELLOW}Creating directories...{Style.RESET_ALL}")
    
    directories = ['logs', 'screenshots', 'config']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{Fore.GREEN}✓ Created directory: {directory}{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}✓ Directory already exists: {directory}{Style.RESET_ALL}")

def verify_files():
    """Verify that all required files exist"""
    print(f"\n{Fore.YELLOW}Verifying files...{Style.RESET_ALL}")
    
    required_files = [
        'minecraft_farm_bot.py',
        'advanced_farm_bot.py',
        'launcher.py',
        'requirements.txt',
        'config.ini',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"{Fore.GREEN}✓ {file}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {file} (missing){Style.RESET_ALL}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n{Fore.RED}Missing files: {', '.join(missing_files)}{Style.RESET_ALL}")
        return False
    
    return True

def run_tests():
    """Run basic tests to verify installation"""
    print(f"\n{Fore.YELLOW}Running basic tests...{Style.RESET_ALL}")
    
    try:
        # Test imports
        import pyautogui
        import cv2
        import numpy as np
        import keyboard
        import mouse
        import colorama
        import configparser
        from PIL import Image, ImageGrab
        
        print(f"{Fore.GREEN}✓ All imports successful{Style.RESET_ALL}")
        
        # Test screen capture
        try:
            screenshot = ImageGrab.grab()
            print(f"{Fore.GREEN}✓ Screen capture test successful{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Screen capture test failed: {e}{Style.RESET_ALL}")
        
        return True
        
    except ImportError as e:
        print(f"{Fore.RED}✗ Import test failed: {e}{Style.RESET_ALL}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print(f"\n{Fore.CYAN}=== Setup Complete! ==={Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Next steps:{Style.RESET_ALL}")
    print("1. Start Minecraft and load your world")
    print("2. Position yourself in the center of your farm")
    print("3. Run the launcher: python launcher.py")
    print("4. Choose between Basic or Advanced bot")
    print("5. Follow the on-screen instructions")
    
    print(f"\n{Fore.YELLOW}Important notes:{Style.RESET_ALL}")
    print("• Make sure Minecraft is in windowed mode")
    print("• Ensure you have seeds and farming tools")
    print("• Test in a safe environment first")
    print("• Use F1/F2/F3 to control the bot")
    
    print(f"\n{Fore.BLUE}For help:{Style.RESET_ALL}")
    print("• Read README.md for detailed instructions")
    print("• Check config.ini for settings")
    print("• View logs for troubleshooting")

def main():
    """Main setup function"""
    print_banner()
    
    print(f"{Fore.YELLOW}Welcome to the Minecraft Farm Bot setup!{Style.RESET_ALL}")
    print("This script will install dependencies and prepare your environment.")
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Install dependencies
    if not install_dependencies():
        print(f"\n{Fore.RED}Failed to install dependencies. Please check your internet connection.{Style.RESET_ALL}")
        input("Press Enter to exit...")
        return
    
    # Create directories
    create_directories()
    
    # Verify files
    if not verify_files():
        print(f"\n{Fore.RED}Some required files are missing. Please ensure all files are present.{Style.RESET_ALL}")
        input("Press Enter to exit...")
        return
    
    # Run tests
    if not run_tests():
        print(f"\n{Fore.YELLOW}Some tests failed, but setup may still work.{Style.RESET_ALL}")
    
    # Show next steps
    show_next_steps()
    
    print(f"\n{Fore.GREEN}Setup completed successfully!{Style.RESET_ALL}")
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Setup interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred during setup: {e}{Style.RESET_ALL}")
        input("Press Enter to exit...") 