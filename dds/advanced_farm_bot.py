#!/usr/bin/env python3
"""
Advanced Minecraft Farm Bot
Enhanced automation bot with inventory management and advanced farming features
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
import json
from colorama import init, Fore, Style
from PIL import Image, ImageGrab, ImageFilter
import os
from datetime import datetime

# Initialize colorama for colored output
init()

class AdvancedMinecraftFarmBot:
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
        
        # Advanced settings
        self.inventory_slots = 36  # Standard inventory size
        self.seed_threshold = self.config.getint('Advanced', 'seed_threshold', fallback=10)
        self.auto_restock = self.config.getboolean('Advanced', 'auto_restock', fallback=True)
        self.smart_pathfinding = self.config.getboolean('Advanced', 'smart_pathfinding', fallback=True)
        
        # Key bindings
        self.forward_key = self.config.get('Controls', 'forward', fallback='w')
        self.backward_key = self.config.get('Controls', 'backward', fallback='s')
        self.left_key = self.config.get('Controls', 'left', fallback='a')
        self.right_key = self.config.get('Controls', 'right', fallback='d')
        self.jump_key = self.config.get('Controls', 'jump', fallback='space')
        self.sneak_key = self.config.get('Controls', 'sneak', fallback='shift')
        self.use_key = self.config.get('Controls', 'use', fallback='right')
        self.attack_key = self.config.get('Controls', 'attack', fallback='left')
        self.inventory_key = self.config.get('Controls', 'inventory', fallback='e')
        
        # Enhanced crop types with growth stages
        self.crop_types = {
            'wheat': {
                'seeds': 'wheat_seeds',
                'growth_stages': [
                    (34, 139, 34),   # Stage 1 - Light green
                    (50, 205, 50),   # Stage 2 - Medium green
                    (85, 107, 47),   # Stage 3 - Dark green
                    (139, 69, 19)    # Stage 4 - Mature brown
                ],
                'mature_color': (139, 69, 19),
                'harvest_yield': 1
            },
            'carrots': {
                'seeds': 'carrot',
                'growth_stages': [
                    (255, 140, 0),   # Stage 1 - Light orange
                    (255, 165, 0),   # Stage 2 - Orange
                    (255, 69, 0),    # Stage 3 - Dark orange
                    (255, 165, 0)    # Stage 4 - Mature orange
                ],
                'mature_color': (255, 165, 0),
                'harvest_yield': 1
            },
            'potatoes': {
                'seeds': 'potato',
                'growth_stages': [
                    (139, 69, 19),   # Stage 1 - Light brown
                    (160, 82, 45),   # Stage 2 - Brown
                    (205, 133, 63),  # Stage 3 - Dark brown
                    (139, 69, 19)    # Stage 4 - Mature brown
                ],
                'mature_color': (139, 69, 19),
                'harvest_yield': 1
            },
            'beetroot': {
                'seeds': 'beetroot_seeds',
                'growth_stages': [
                    (255, 0, 0),     # Stage 1 - Light red
                    (220, 20, 60),   # Stage 2 - Red
                    (178, 34, 34),   # Stage 3 - Dark red
                    (139, 0, 0)      # Stage 4 - Mature dark red
                ],
                'mature_color': (139, 0, 0),
                'harvest_yield': 1
            }
        }
        
        # Inventory tracking
        self.inventory = {
            'seeds': {'wheat_seeds': 0, 'carrot': 0, 'potato': 0, 'beetroot_seeds': 0},
            'crops': {'wheat': 0, 'carrot': 0, 'potato': 0, 'beetroot': 0},
            'tools': {'hoe': False, 'water_bucket': False, 'shovel': False}
        }
        
        # Statistics tracking
        self.stats = {
            'crops_harvested': 0,
            'crops_planted': 0,
            'waterings': 0,
            'start_time': None,
            'session_duration': 0
        }
        
        # Pathfinding grid
        self.farm_grid = None
        self.player_position = [0, 0]
        
        print(f"{Fore.GREEN}Advanced Minecraft Farm Bot initialized!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press 'F1' to start/stop the bot{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press 'F2' to pause/resume{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press 'F3' to exit{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Press 'F4' to show statistics{Style.RESET_ALL}")
    
    def load_config(self):
        """Load configuration from config.ini file"""
        config = configparser.ConfigParser()
        config_file = 'config.ini'
        
        if not os.path.exists(config_file):
            self.create_default_config(config)
        
        config.read(config_file)
        return config
    
    def create_default_config(self, config):
        """Create default configuration file with advanced settings"""
        config['Settings'] = {
            'farm_radius': '5',
            'plant_delay': '0.5',
            'harvest_delay': '0.3',
            'water_delay': '1.0',
            'farm_pattern': 'grid',
            'auto_water': 'true',
            'auto_plant': 'true',
            'auto_harvest': 'true'
        }
        
        config['Advanced'] = {
            'seed_threshold': '10',
            'auto_restock': 'true',
            'smart_pathfinding': 'true',
            'color_threshold': '50',
            'scan_interval': '0.5',
            'movement_speed': '0.1',
            'enable_statistics': 'true'
        }
        
        config['Controls'] = {
            'forward': 'w',
            'backward': 's',
            'left': 'a',
            'right': 'd',
            'jump': 'space',
            'sneak': 'shift',
            'use': 'right',
            'attack': 'left',
            'inventory': 'e'
        }
        
        config['Hotkeys'] = {
            'start_stop': 'F1',
            'pause_resume': 'F2',
            'exit': 'F3',
            'show_stats': 'F4'
        }
        
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
    def setup_logging(self):
        """Setup enhanced logging configuration"""
        log_filename = f"minecraft_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Start the advanced farm bot"""
        self.running = True
        self.stats['start_time'] = datetime.now()
        self.logger.info("Advanced farm bot started")
        print(f"{Fore.GREEN}Advanced farm bot started!{Style.RESET_ALL}")
        
        # Initialize farm grid
        self.initialize_farm_grid()
        
        # Start the main farming loop in a separate thread
        self.farming_thread = threading.Thread(target=self.advanced_farming_loop)
        self.farming_thread.daemon = True
        self.farming_thread.start()
        
        # Start inventory monitoring thread
        self.inventory_thread = threading.Thread(target=self.monitor_inventory)
        self.inventory_thread.daemon = True
        self.inventory_thread.start()
        
        # Start the hotkey listener
        self.setup_hotkeys()
    
    def stop(self):
        """Stop the farm bot"""
        self.running = False
        self.update_session_duration()
        self.logger.info("Advanced farm bot stopped")
        print(f"{Fore.RED}Advanced farm bot stopped!{Style.RESET_ALL}")
    
    def pause(self):
        """Pause/resume the farm bot"""
        self.paused = not self.paused
        status = "paused" if self.paused else "resumed"
        self.logger.info(f"Advanced farm bot {status}")
        print(f"{Fore.YELLOW}Advanced farm bot {status}!{Style.RESET_ALL}")
    
    def setup_hotkeys(self):
        """Setup hotkey listeners"""
        keyboard.add_hotkey('F1', self.toggle_bot)
        keyboard.add_hotkey('F2', self.pause)
        keyboard.add_hotkey('F3', self.exit_bot)
        keyboard.add_hotkey('F4', self.show_statistics)
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
        self.save_statistics()
        print(f"{Fore.RED}Exiting Advanced Minecraft Farm Bot...{Style.RESET_ALL}")
        os._exit(0)
    
    def show_statistics(self):
        """Display current bot statistics"""
        self.update_session_duration()
        print(f"\n{Fore.CYAN}=== Bot Statistics ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Session Duration: {self.stats['session_duration']}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Crops Harvested: {self.stats['crops_harvested']}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Crops Planted: {self.stats['crops_planted']}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Waterings: {self.stats['waterings']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Inventory Status:{Style.RESET_ALL}")
        for seed_type, count in self.inventory['seeds'].items():
            print(f"  {seed_type}: {count}")
    
    def update_session_duration(self):
        """Update session duration"""
        if self.stats['start_time']:
            self.stats['session_duration'] = str(datetime.now() - self.stats['start_time']).split('.')[0]
    
    def save_statistics(self):
        """Save statistics to file"""
        self.update_session_duration()
        stats_file = f"bot_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2, default=str)
        self.logger.info(f"Statistics saved to {stats_file}")
    
    def initialize_farm_grid(self):
        """Initialize the farm grid for pathfinding"""
        grid_size = self.farm_radius * 2 + 1
        self.farm_grid = np.zeros((grid_size, grid_size), dtype=int)
        self.player_position = [self.farm_radius, self.farm_radius]
        self.logger.info(f"Initialized farm grid: {grid_size}x{grid_size}")
    
    def advanced_farming_loop(self):
        """Enhanced main farming automation loop"""
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue
            
            try:
                # Check inventory levels
                self.check_inventory_levels()
                
                # Smart farming based on inventory and crop maturity
                if self.config.getboolean('Settings', 'auto_harvest', fallback=True):
                    self.smart_harvest_crops()
                
                if self.config.getboolean('Settings', 'auto_plant', fallback=True):
                    self.smart_plant_crops()
                
                if self.config.getboolean('Settings', 'auto_water', fallback=True):
                    self.smart_water_crops()
                
                # Update farm grid
                self.update_farm_grid()
                
                time.sleep(self.config.getfloat('Advanced', 'scan_interval', fallback=0.5))
                
            except Exception as e:
                self.logger.error(f"Error in advanced farming loop: {e}")
                time.sleep(1)
    
    def monitor_inventory(self):
        """Monitor inventory levels in background"""
        while self.running:
            try:
                # Simulate inventory checking (in real implementation, you'd use OCR)
                # For now, we'll use a simple simulation
                time.sleep(5)  # Check every 5 seconds
                
                if self.auto_restock and self.needs_restock():
                    self.logger.info("Inventory restock needed")
                    # In a real implementation, you'd trigger restock logic
                    
            except Exception as e:
                self.logger.error(f"Error in inventory monitoring: {e}")
                time.sleep(1)
    
    def check_inventory_levels(self):
        """Check current inventory levels"""
        # This is a simplified inventory check
        # In a real implementation, you'd use OCR to read inventory
        pass
    
    def needs_restock(self):
        """Check if inventory needs restocking"""
        for seed_type, count in self.inventory['seeds'].items():
            if count < self.seed_threshold:
                return True
        return False
    
    def smart_harvest_crops(self):
        """Smart harvesting with crop type detection"""
        self.logger.info("Smart harvesting crops...")
        
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        for x in range(center_x - 100, center_x + 100, 20):
            for y in range(center_y - 100, center_y + 100, 20):
                if not self.running or self.paused:
                    return
                
                # Detect crop type and maturity
                crop_info = self.detect_crop_type_and_maturity(x, y)
                if crop_info and crop_info['mature']:
                    self.logger.info(f"Harvesting mature {crop_info['type']} at ({x}, {y})")
                    
                    # Use smart pathfinding to move to crop
                    if self.smart_pathfinding:
                        self.smart_move_to_position(x, y)
                    else:
                        self.move_to_position(x, y)
                    
                    # Harvest with appropriate tool
                    self.harvest_crop(x, y, crop_info['type'])
                    self.stats['crops_harvested'] += 1
    
    def smart_plant_crops(self):
        """Smart planting with seed selection"""
        self.logger.info("Smart planting crops...")
        
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        for x in range(center_x - 100, center_x + 100, 20):
            for y in range(center_y - 100, center_y + 100, 20):
                if not self.running or self.paused:
                    return
                
                if self.is_plot_empty(x, y):
                    # Select best seed based on inventory
                    best_seed = self.select_best_seed()
                    if best_seed:
                        self.logger.info(f"Planting {best_seed} at ({x}, {y})")
                        
                        if self.smart_pathfinding:
                            self.smart_move_to_position(x, y)
                        else:
                            self.move_to_position(x, y)
                        
                        self.plant_crop(x, y, best_seed)
                        self.stats['crops_planted'] += 1
    
    def smart_water_crops(self):
        """Smart watering based on soil moisture detection"""
        self.logger.info("Smart watering crops...")
        
        # Check if we have water bucket
        if not self.inventory['tools']['water_bucket']:
            self.logger.warning("No water bucket available for watering")
            return
        
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2
        
        for x in range(center_x - 100, center_x + 100, 20):
            for y in range(center_y - 100, center_y + 100, 20):
                if not self.running or self.paused:
                    return
                
                if self.needs_watering(x, y):
                    self.logger.info(f"Watering crop at ({x}, {y})")
                    
                    if self.smart_pathfinding:
                        self.smart_move_to_position(x, y)
                    else:
                        self.move_to_position(x, y)
                    
                    self.water_crop(x, y)
                    self.stats['waterings'] += 1
    
    def detect_crop_type_and_maturity(self, x, y):
        """Detect crop type and maturity level"""
        color = self.detect_crop_color(x, y)
        if color is None:
            return None
        
        for crop_type, crop_data in self.crop_types.items():
            for stage, stage_color in enumerate(crop_data['growth_stages']):
                distance = np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color, stage_color)))
                if distance < self.config.getint('Advanced', 'color_threshold', fallback=50):
                    return {
                        'type': crop_type,
                        'stage': stage,
                        'mature': stage == len(crop_data['growth_stages']) - 1
                    }
        
        return None
    
    def select_best_seed(self):
        """Select the best seed based on inventory and preferences"""
        # Simple selection logic - can be enhanced
        for seed_type, count in self.inventory['seeds'].items():
            if count > 0:
                return seed_type
        return None
    
    def needs_watering(self, x, y):
        """Check if a crop needs watering"""
        # Simplified watering detection
        # In a real implementation, you'd detect dry soil
        return np.random.random() < 0.1  # 10% chance of needing water
    
    def smart_move_to_position(self, target_x, target_y):
        """Smart pathfinding to target position"""
        # Simplified A* pathfinding
        # In a real implementation, you'd implement proper pathfinding
        self.move_to_position(target_x, target_y)
    
    def update_farm_grid(self):
        """Update the farm grid with current state"""
        # Update grid based on current farming state
        pass
    
    def harvest_crop(self, x, y, crop_type):
        """Harvest a specific crop type"""
        pyautogui.click(x, y, button=self.attack_key)
        time.sleep(self.harvest_delay)
        
        # Update inventory
        if crop_type in self.inventory['crops']:
            self.inventory['crops'][crop_type] += self.crop_types[crop_type]['harvest_yield']
    
    def plant_crop(self, x, y, seed_type):
        """Plant a specific seed type"""
        pyautogui.click(x, y, button=self.use_key)
        time.sleep(self.plant_delay)
        
        # Update inventory
        if seed_type in self.inventory['seeds']:
            self.inventory['seeds'][seed_type] -= 1
    
    def water_crop(self, x, y):
        """Water a crop"""
        pyautogui.click(x, y, button=self.use_key)
        time.sleep(self.water_delay)
    
    # Inherit other methods from the basic bot
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

def main():
    """Main function to run the Advanced Minecraft Farm Bot"""
    print(f"{Fore.CYAN}=== Advanced Minecraft Farm Bot ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}Made by DDS{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Enhanced features: Inventory management, smart pathfinding, statistics{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Make sure Minecraft is running and you're in a farming area!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Position yourself in the center of your farm.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Enter to start the advanced bot...{Style.RESET_ALL}")
    
    input()
    
    bot = AdvancedMinecraftFarmBot()
    bot.start()

if __name__ == "__main__":
    main() 