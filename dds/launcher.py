#!/usr/bin/env python3
"""
Minecraft Farm Bot Launcher
Choose between basic and advanced versions of the farm bot
Made by DDS
"""

import os
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

def print_banner():
    """Print the bot banner"""
    print(f"{Fore.CYAN}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    MINECRAFT FARM BOT                        ║")
    print("║                     🌾 Automated Farming 🌾                  ║")
    print("║                        Made by DDS                           ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

def print_menu():
    """Print the main menu"""
    print(f"\n{Fore.YELLOW}Choose your farm bot version:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Basic Farm Bot - Simple automation")
    print(f"{Fore.BLUE}2.{Style.RESET_ALL} Advanced Farm Bot - Enhanced features")
    print(f"{Fore.RED}3.{Style.RESET_ALL} Exit")
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'pyautogui', 'opencv-python', 'numpy', 'pillow', 
        'keyboard', 'mouse', 'colorama', 'configparser'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"{Fore.RED}Missing required packages:{Style.RESET_ALL}")
        for package in missing_packages:
            print(f"  - {package}")
        print(f"\n{Fore.YELLOW}Install missing packages with:{Style.RESET_ALL}")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def run_basic_bot():
    """Run the basic farm bot"""
    print(f"{Fore.GREEN}Starting Basic Farm Bot...{Style.RESET_ALL}")
    try:
        import minecraft_farm_bot
        minecraft_farm_bot.main()
    except ImportError:
        print(f"{Fore.RED}Error: Could not import basic farm bot{Style.RESET_ALL}")
        print("Make sure 'minecraft_farm_bot.py' exists in the current directory.")

def run_advanced_bot():
    """Run the advanced farm bot"""
    print(f"{Fore.BLUE}Starting Advanced Farm Bot...{Style.RESET_ALL}")
    try:
        import advanced_farm_bot
        advanced_farm_bot.main()
    except ImportError:
        print(f"{Fore.RED}Error: Could not import advanced farm bot{Style.RESET_ALL}")
        print("Make sure 'advanced_farm_bot.py' exists in the current directory.")

def show_version_info():
    """Show information about both versions"""
    print(f"\n{Fore.CYAN}=== Version Information ==={Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}Basic Farm Bot Features:{Style.RESET_ALL}")
    print("  ✓ Automatic harvesting")
    print("  ✓ Smart planting")
    print("  ✓ Auto watering")
    print("  ✓ Configurable controls")
    print("  ✓ Hotkey controls")
    print("  ✓ Logging system")
    print("  ✓ Multiple crop support")
    
    print(f"\n{Fore.BLUE}Advanced Farm Bot Features:{Style.RESET_ALL}")
    print("  ✓ All basic features")
    print("  ✓ Inventory management")
    print("  ✓ Smart pathfinding")
    print("  ✓ Statistics tracking")
    print("  ✓ Enhanced crop detection")
    print("  ✓ Growth stage monitoring")
    print("  ✓ Auto restock alerts")
    print("  ✓ Session statistics")
    print("  ✓ Advanced configuration")

def main():
    """Main launcher function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print(f"\n{Fore.RED}Please install missing dependencies and try again.{Style.RESET_ALL}")
        input("Press Enter to exit...")
        return
    
    while True:
        print_menu()
        choice = input(f"{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            run_basic_bot()
            break
        elif choice == '2':
            run_advanced_bot()
            break
        elif choice == '3':
            print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
            break
        elif choice.lower() == 'info':
            show_version_info()
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Type 'info' to see version information.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Launcher interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        input("Press Enter to exit...") 