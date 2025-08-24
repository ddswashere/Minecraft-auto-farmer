#!/usr/bin/env python3
"""
Minecraft Farm Bot
A comprehensive automation bot for farming tasks in Minecraft
Made by DDS
"""

import pyautogui
import cv2
import numpy as np
import keyboard
import mouse
import time
import threading
import logging
import configparser
from colorama import init, Fore, Style
from PIL import Image, ImageGrab
import os

# Initialize colorama for colored output
init()

class MinecraftFarmBot:
    def __init__(self):
        self.running = False
        self.paused = False
        self.current_task = None
        self.config = self.load_config()
        self.setup_logging()
        
        # Bot settings
        self.farm_radius = self.config.getint('Settings', 'farm_radius', fallback=5)
        self.plant_delay = self.config.getfloat('Settings', 'plant_delay', fallback=0.5)
        self.harvest_delay = self.config.getfloat('Settings', 'harvest_delay', fallback=0.3)
        self.water_delay = self.config.getfloat('Settings', 'water_delay', fallback=1.0)
        
        # Key bindings
        self.forward_key = self.config.get('Controls', 'forward', fallback='w')
        self.backward_key = self.config.get('Controls', 'backward', fallback='s')
        self.left_key = self.config.get('Controls', 'left', fallback='a')
        self.right_key = self.config.get('Controls', 'right', fallback='d')
        self.jump_key = self.config.get('Controls', 'jump', fallback='space')
        self.sneak_key = self.config.get('Controls', 'sneak', fallback='shift')
        self.use_key = self.config.get('Controls', 'use', fallback='right')
        self.attack_key = self.config.get('Controls', 'attack', fallback='left')
        
        # Crop types and their growth stages
        self.crop_types = {
            'wheat': {'seeds': 'wheat_seeds', 'mature_color': (139, 69, 19)},
            'carrots': {'seeds': 'carrot', 'mature_color': (255, 165, 0)},
            'potatoes': {'seeds': 'potato', 'mature_color': (139, 69, 19)},
            'beetroot': {'seeds': 'beetroot_seeds', 'mature_color': (139, 0, 0)}
        }
        
        print(f"{Fore.GREEN}Minecraft Farm Bot initialized!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press 'F1' to start/stop the bot{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press 'F2' to pause/resume{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press 'F3' to exit{Style.RESET_ALL}")
    
    def load_config(self):
        """Load configuration from config.ini file"""
        config = configparser.ConfigParser()
        config_file = 'config.ini'
        
        if not os.path.exists(config_file):
            self.create_default_config(config)
        
        config.read(config_file)
        return config
    
    def create_default_config(self, config):
        """Create default configuration file"""
        config['Settings'] = {
            'farm_radius': '5',
            'plant_delay': '0.5',
            'harvest_delay': '0.3',
            'water_delay': '1.0',
            'auto_water': 'true',
            'auto_plant': 'true',
            'auto_harvest': 'true'
        }
        
        config['Controls'] = {
            'forward': 'w',
            'backward': 's',
            'left': 'a',
            'right': 'd',
            'jump': 'space',
            'sneak': 'shift',
            'use': 'right',
            'attack': 'left'
        }
        
        config['Hotkeys'] = {
            'start_stop': 'F1',
            'pause_resume': 'F2',
            'exit': 'F3'
        }
        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('minecraft_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Start the farm bot"""
        self.running = True
        self.logger.info("Farm bot started")
        print(f"{Fore.GREEN}Farm bot started!{Style.RESET_ALL}")
        
        # Start the main farming loop in a separate thread
        self.farming_thread = threading.Thread(target=self.farming_loop)
        self.farming_thread.daemon = True
        self.farming_thread.start()
        
        # Start the hotkey listener
        self.setup_hotkeys()
    
    def stop(self):
        """Stop the farm bot"""
        self.running = False
        self.logger.info("Farm bot stopped")
        print(f"{Fore.RED}Farm bot stopped!{Style.RESET_ALL}")
    
    def pause(self):
        """Pause/resume the farm bot"""
        self.paused = not self.paused
        status = "paused" if self.paused else "resumed"
        self.logger.info(f"Farm bot {status}")
        print(f"{Fore.YELLOW}Farm bot {status}!{Style.RESET_ALL}")
    
    def setup_hotkeys(self):
        """Setup hotkey listeners"""
        keyboard.add_hotkey('F1', self.toggle_bot)
        keyboard.add_hotkey('F2', self.pause)
        keyboard.add_hotkey('F3', self.exit_bot)
        keyboard.wait()
    
    def toggle_bot(self):
        """Toggle the bot on/off"""
        if self.running:
            self.stop()
        else:
            self.start()
    
    def exit_bot(self):
        """Exit the bot"""
        self.stop()
        print(f"{Fore.RED}Exiting Minecraft Farm Bot...{Style.RESET_ALL}")
        os._exit(0)
    
    def farming_loop(self):
        """Main farming automation loop"""
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue
            
            try:
                # Check for mature crops to harvest
                if self.config.getboolean('Settings', 'auto_harvest', fallback=True):
                    self.harvest_mature_crops()
                
                # Check for empty plots to plant
                if self.config.getboolean('Settings', 'auto_plant', fallback=True):
                    self.plant_crops()
                
                # Water crops if needed
                if self.config.getboolean('Settings', 'auto_water', fallback=True):
                    self.water_crops()
                
                time.sleep(0.5)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                self.logger.error(f"Error in farming loop: {e}")
                time.sleep(1)
    
    def get_screen_region(self, x, y, width, height):
        """Capture a specific region of the screen"""
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            return np.array(screenshot)
        except Exception as e:
            self.logger.error(f"Error capturing screen region: {e}")
            return None
    
    def detect_crop_color(self, x, y, width=10, height=10):
        """Detect the color of crops at a specific screen position"""
        region = self.get_screen_region(x, y, width, height)
        if region is None:
            return None
        
        # Convert to RGB and get average color
        region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)
        avg_color = np.mean(region_rgb, axis=(0, 1))
        return tuple(map(int, avg_color))
    
    def is_crop_mature(self, x, y, crop_type='wheat'):
        """Check if a crop is mature based on color detection"""
        color = self.detect_crop_color(x, y)
        if color is None:
            return False
        
        mature_color = self.crop_types[crop_type]['mature_color']
        # Simple color distance check
        distance = np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color, mature_color)))
        return distance < 50  # Threshold for color similarity
    
    def is_plot_empty(self, x, y):
        """Check if a farming plot is empty"""
        color = self.detect_crop_color(x, y)
        if color is None:
            return False
        
        # Check if the color is close to dirt/brown (empty plot)
        dirt_colors = [(139, 69, 19), (160, 82, 45), (205, 133, 63)]
        for dirt_color in dirt_colors:
            distance = np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color, dirt_color)))
            if distance < 30:
                return True
        return False
    
    def move_to_position(self, target_x, target_y):
        """Move the player to a specific position"""
        # This is a simplified movement - in a real implementation,
        # you'd need more sophisticated pathfinding
        current_x, current_y = pyautogui.position()
        
        # Calculate direction
        dx = target_x - current_x
        dy = target_y - current_y
        
        # Move towards target
        if abs(dx) > 5:
            if dx > 0:
                pyautogui.keyDown(self.right_key)
                time.sleep(0.1)
                pyautogui.keyUp(self.right_key)
            else:
                pyautogui.keyDown(self.left_key)
                time.sleep(0.1)
                pyautogui.keyUp(self.left_key)
        
        if abs(dy) > 5:
            if dy > 0:
                pyautogui.keyDown(self.backward_key)
                time.sleep(0.1)
                pyautogui.keyUp(self.backward_key)
            else:
                pyautogui.keyDown(self.forward_key)
                time.sleep(0.1)
                pyautogui.keyUp(self.forward_key)
    
    def harvest_mature_crops(self):
        """Harvest mature crops in the farm area"""
        self.logger.info("Checking for mature crops to harvest...")
        
        # Scan the farm area for mature crops
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        for x in range(center_x - 100, center_x + 100, 20):
            for y in range(center_y - 100, center_y + 100, 20):
                if not self.running or self.paused:
                    return
                
                # Check if crop is mature
                if self.is_crop_mature(x, y):
                    self.logger.info(f"Harvesting mature crop at ({x}, {y})")
                    
                    # Move to crop position
                    self.move_to_position(x, y)
                    
                    # Harvest the crop
                    pyautogui.click(x, y, button=self.attack_key)
                    time.sleep(self.harvest_delay)
    
    def plant_crops(self):
        """Plant crops in empty plots"""
        self.logger.info("Checking for empty plots to plant...")
        
        # Scan the farm area for empty plots
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        for x in range(center_x - 100, center_x + 100, 20):
            for y in range(center_y - 100, center_y + 100, 20):
                if not self.running or self.paused:
                    return
                
                # Check if plot is empty
                if self.is_plot_empty(x, y):
                    self.logger.info(f"Planting crop at ({x}, {y})")
                    
                    # Move to plot position
                    self.move_to_position(x, y)
                    
                    # Plant the crop
                    pyautogui.click(x, y, button=self.use_key)
                    time.sleep(self.plant_delay)
    
    def water_crops(self):
        """Water crops that need watering"""
        self.logger.info("Checking for crops that need watering...")
        
        # This is a simplified watering system
        # In a real implementation, you'd need to detect dry soil
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        # Check if player has water bucket
        # For now, we'll just simulate watering every few cycles
        if hasattr(self, '_water_counter'):
            self._water_counter += 1
        else:
            self._water_counter = 0
        
        if self._water_counter > 50:  # Water every 50 cycles
            self.logger.info("Watering crops...")
            pyautogui.keyDown(self.use_key)
            time.sleep(self.water_delay)
            pyautogui.keyUp(self.use_key)
            self._water_counter = 0
    
    def auto_farm_pattern(self):
        """Execute a predefined farming pattern"""
        patterns = {
            'grid': self.farm_grid_pattern,
            'spiral': self.farm_spiral_pattern,
            'rows': self.farm_row_pattern
        }
        
        pattern = self.config.get('Settings', 'farm_pattern', fallback='grid')
        if pattern in patterns:
            patterns[pattern]()
    
    def farm_grid_pattern(self):
        """Farm in a grid pattern"""
        self.logger.info("Executing grid farming pattern...")
        
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        for row in range(-self.farm_radius, self.farm_radius + 1):
            for col in range(-self.farm_radius, self.farm_radius + 1):
                if not self.running or self.paused:
                    return
                
                target_x = center_x + (col * 20)
                target_y = center_y + (row * 20)
                
                self.move_to_position(target_x, target_y)
                self.harvest_mature_crops()
                self.plant_crops()
    
    def farm_spiral_pattern(self):
        """Farm in a spiral pattern"""
        self.logger.info("Executing spiral farming pattern...")
        
        # Implementation for spiral pattern
        # This would move in a spiral from center outward
        pass
    
    def farm_row_pattern(self):
        """Farm in rows"""
        self.logger.info("Executing row farming pattern...")
        
        # Implementation for row pattern
        # This would farm row by row
        pass

def main():
    """Main function to run the Minecraft Farm Bot"""
    print(f"{Fore.CYAN}=== Minecraft Farm Bot ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}Made by DDS{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Make sure Minecraft is running and you're in a farming area!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Position yourself in the center of your farm.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Enter to start the bot...{Style.RESET_ALL}")
    
    input()
    
    bot = MinecraftFarmBot()
    bot.start()

if __name__ == "__main__":
    main() 