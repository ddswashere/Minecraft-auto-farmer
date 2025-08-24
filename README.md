# Minecraft-auto-farmer
# 🌾 Minecraft Farm Bot - Complete Automation System

**Made by DDS** | *Advanced Minecraft Farming Automation*

A comprehensive, feature-rich automation system for Minecraft farming that can handle everything from basic crop harvesting to advanced inventory management and smart pathfinding.

## 📋 Table of Contents

- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Advanced Features](#-advanced-features)
- [Troubleshooting](#-troubleshooting)
- [Safety & Legal](#-safety--legal)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [Credits](#-credits)

## ✨ Features

### 🟢 Basic Farm Bot
- **Automatic Harvesting**: Intelligent crop detection and harvesting
- **Smart Planting**: Automatically plants seeds in empty plots
- **Auto Watering**: Maintains optimal soil moisture
- **Multi-Crop Support**: Wheat, carrots, potatoes, beetroot
- **Configurable Controls**: Customizable key bindings
- **Hotkey System**: Easy start/stop/pause controls
- **Logging System**: Detailed activity tracking
- **Color Recognition**: Advanced crop maturity detection

### 🔵 Advanced Farm Bot
- **All Basic Features** plus:
- **Inventory Management**: Track seeds, crops, and tools
- **Smart Pathfinding**: Efficient movement algorithms
- **Statistics Tracking**: Real-time performance metrics
- **Growth Stage Monitoring**: Track crop development stages
- **Auto Restock Alerts**: Notify when supplies are low
- **Session Analytics**: Detailed farming statistics
- **Enhanced Detection**: Multi-stage crop recognition
- **Background Monitoring**: Continuous inventory tracking

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.7 or higher
- **RAM**: 4GB available
- **Storage**: 100MB free space
- **Minecraft**: Java Edition (any version)

### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **Python**: 3.9 or higher
- **RAM**: 8GB available
- **Storage**: 500MB free space
- **Minecraft**: Latest Java Edition
- **Graphics**: Dedicated GPU for better performance

### Dependencies
```
pyautogui==0.9.54
opencv-python==4.8.1.78
numpy==1.24.3
pillow==10.0.1
keyboard==0.13.5
mouse==0.7.1
colorama==0.4.6
configparser==6.0.0
```

## 🚀 Installation

### Method 1: Automated Setup (Recommended)
```bash
# Clone or download the repository
git clone <repository-url>
cd minecraft-farm-bot

# Run automated setup
python setup.py
```

### Method 2: Manual Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python launcher.py
```

### Method 3: Individual File Installation
```bash
# Install each dependency manually
pip install pyautogui==0.9.54
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
pip install pillow==10.0.1
pip install keyboard==0.13.5
pip install mouse==0.7.1
pip install colorama==0.4.6
pip install configparser==6.0.0
```

## ⚡ Quick Start

### 1. Prepare Minecraft
- Start Minecraft and load your world
- Position yourself in the center of your farm
- Ensure you have:
  - Seeds for planting
  - Water bucket (for auto-watering)
  - Hoe (for tilling soil if needed)
- Make sure your farm is properly tilled and ready

### 2. Launch the Bot
```bash
# Use the launcher (recommended)
python launcher.py

# Or run directly
python minecraft_farm_bot.py      # Basic version
python advanced_farm_bot.py       # Advanced version
```

### 3. Configure Settings
- Edit `config.ini` to customize bot behavior
- Adjust farm radius, delays, and controls
- Set your preferred hotkeys

### 4. Start Farming
- Press `Enter` when ready
- Use F1 to start/stop the bot
- Use F2 to pause/resume
- Use F3 to exit

## ⚙️ Configuration

### Main Settings (`config.ini`)
```ini
[Settings]
farm_radius = 5              # How far the bot farms from center
plant_delay = 0.5           # Delay between planting actions
harvest_delay = 0.3         # Delay between harvesting actions
water_delay = 1.0           # Delay between watering actions
farm_pattern = grid         # Farming pattern (grid/spiral/rows)
auto_water = true           # Enable auto watering
auto_plant = true           # Enable auto planting
auto_harvest = true         # Enable auto harvesting

[Advanced]
seed_threshold = 10         # Minimum seeds before restock alert
auto_restock = true         # Enable auto restock monitoring
smart_pathfinding = true    # Enable smart movement
color_threshold = 50        # Color detection sensitivity
scan_interval = 0.5         # How often to scan for crops
movement_speed = 0.1        # Movement speed multiplier
enable_statistics = true    # Enable statistics tracking

[Controls]
forward = w                 # Move forward key
backward = s                # Move backward key
left = a                    # Move left key
right = d                   # Move right key
jump = space                # Jump key
sneak = shift               # Sneak key
use = right                 # Use/place key
attack = left               # Attack/break key
inventory = e               # Open inventory key

[Hotkeys]
start_stop = F1             # Start/stop bot
pause_resume = F2           # Pause/resume bot
exit = F3                   # Exit bot
show_stats = F4             # Show statistics (advanced only)
```

## 🎮 Usage Guide

### Basic Controls
| Key | Action |
|-----|--------|
| **F1** | Start/Stop the bot |
| **F2** | Pause/Resume |
| **F3** | Exit completely |
| **F4** | Show statistics (Advanced only) |

### What the Bot Does
1. **Scans Farm Area**: Continuously monitors your farm
2. **Detects Mature Crops**: Uses color recognition to identify ready crops
3. **Harvests Automatically**: Breaks mature crops and collects drops
4. **Plants New Seeds**: Places seeds in empty farming plots
5. **Waters Crops**: Maintains optimal soil moisture
6. **Tracks Statistics**: Records farming performance (Advanced)

### Farming Patterns
- **Grid Pattern**: Systematic grid-based farming
- **Spiral Pattern**: Spiral movement from center outward
- **Row Pattern**: Row-by-row farming approach

### Crop Support
| Crop | Seeds | Growth Stages | Harvest Yield |
|------|-------|---------------|---------------|
| **Wheat** | Wheat Seeds | 4 stages | 1-3 wheat |
| **Carrots** | Carrot | 4 stages | 1-4 carrots |
| **Potatoes** | Potato | 4 stages | 1-4 potatoes |
| **Beetroot** | Beetroot Seeds | 4 stages | 1 beetroot |

## 🔧 Advanced Features

### Inventory Management
- **Real-time Tracking**: Monitor seed and crop quantities
- **Auto Restock Alerts**: Notify when supplies are low
- **Tool Detection**: Identify available farming tools
- **Smart Selection**: Choose best seeds based on inventory

### Smart Pathfinding
- **Efficient Movement**: Optimized routes between crops
- **Obstacle Avoidance**: Navigate around farm obstacles
- **Grid-based Navigation**: Systematic farm coverage
- **Position Tracking**: Maintain awareness of player location

### Statistics & Analytics
- **Session Duration**: Track farming time
- **Crops Harvested**: Count of harvested crops
- **Crops Planted**: Count of planted seeds
- **Watering Count**: Number of watering actions
- **Performance Metrics**: Efficiency calculations
- **Export Data**: Save statistics to JSON files

### Enhanced Detection
- **Multi-Stage Recognition**: Identify crop growth stages
- **Color Analysis**: Advanced color matching algorithms
- **Soil Moisture Detection**: Identify dry soil for watering
- **Tool Recognition**: Detect available farming tools

## 🛠️ Troubleshooting

### Common Issues

#### Bot Not Detecting Crops
**Symptoms**: Bot doesn't harvest or plant crops
**Solutions**:
- Ensure you're positioned in the center of your farm
- Check that your farm has proper lighting
- Verify crop colors match expected values
- Adjust `color_threshold` in config.ini
- Make sure Minecraft is the active window

#### Bot Not Moving Properly
**Symptoms**: Bot doesn't move or moves incorrectly
**Solutions**:
- Check your Minecraft key bindings in config.ini
- Ensure Minecraft is in windowed mode
- Verify the bot has proper permissions
- Test movement with manual key presses
- Check for conflicting software

#### Performance Issues
**Symptoms**: Bot runs slowly or uses too much CPU
**Solutions**:
- Reduce farm radius in settings
- Increase scan intervals
- Close unnecessary applications
- Update graphics drivers
- Use basic bot instead of advanced

#### Import Errors
**Symptoms**: "ModuleNotFoundError" or import failures
**Solutions**:
- Run `python setup.py` to install dependencies
- Install missing packages manually: `pip install <package>`
- Check Python version (3.7+ required)
- Verify virtual environment if using one

### Error Codes & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ImportError: No module named 'pyautogui'` | Missing dependency | Run `pip install pyautogui` |
| `PermissionError` | Insufficient permissions | Run as administrator |
| `Screen capture failed` | Graphics driver issue | Update graphics drivers |
| `Key binding error` | Invalid key in config | Check config.ini key bindings |
| `Color detection failed` | Lighting/color issue | Adjust color_threshold |

### Performance Optimization
- **Reduce Farm Radius**: Smaller areas = faster scanning
- **Increase Scan Intervals**: Less frequent checks = lower CPU usage
- **Use Basic Bot**: Advanced features use more resources
- **Close Background Apps**: Free up system resources
- **Update Drivers**: Ensure latest graphics drivers

## ⚠️ Safety & Legal

### Important Disclaimers
- **Educational Use**: This bot is for educational and personal use only
- **Server Rules**: Always check your server's automation policies
- **Minecraft ToS**: Ensure compliance with Minecraft's Terms of Service
- **Local Laws**: Verify compliance with local regulations
- **Use at Own Risk**: Developers are not responsible for consequences

### Safety Guidelines
1. **Always test** in a safe environment first
2. **Keep backups** of your Minecraft world
3. **Monitor the bot** while it's running
4. **Use pause function** (F2) if you need manual control
5. **Don't leave unattended** for extended periods
6. **Check server rules** before using on multiplayer

### Best Practices
- Start with small farm areas
- Test all features before full automation
- Keep the bot updated
- Monitor performance and adjust settings
- Use appropriate delays for your system
- Backup your world regularly

## 🔬 Technical Details

### Architecture
- **Multi-threaded Design**: Separate threads for farming and monitoring
- **Event-driven System**: Hotkey-based control system
- **Modular Code**: Separate modules for different features
- **Configurable**: Extensive configuration options
- **Extensible**: Easy to add new features

### Computer Vision
- **Color Detection**: RGB-based crop recognition
- **Screen Capture**: Real-time screen analysis
- **Pattern Matching**: Advanced image processing
- **Threshold Adjustment**: Configurable sensitivity

### Data Management
- **JSON Statistics**: Structured data storage
- **Logging System**: Comprehensive activity logs
- **Configuration Files**: Persistent settings
- **Session Tracking**: Performance monitoring

### Performance Metrics
- **CPU Usage**: Optimized for minimal impact
- **Memory Management**: Efficient resource usage
- **Response Time**: Fast hotkey response
- **Accuracy**: High crop detection success rate

## 🤝 Contributing

### How to Contribute
1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Areas for Improvement
- **New Crop Types**: Add support for more crops
- **Better Pathfinding**: Improve movement algorithms
- **GUI Interface**: Add graphical user interface
- **Multi-language Support**: Add internationalization
- **Plugin System**: Create modding framework
- **Cloud Integration**: Add cloud-based statistics

### Code Standards
- **Python 3.7+**: Use modern Python features
- **PEP 8**: Follow Python style guidelines
- **Documentation**: Include docstrings and comments
- **Error Handling**: Comprehensive exception handling
- **Testing**: Include unit tests for new features

## 📊 Credits

### Development
- **Created by**: DDS
- **Version**: 2.0.0
- **License**: MIT License
- **Last Updated**: 2024

### Technologies Used
- **Python**: Core programming language
- **OpenCV**: Computer vision and image processing
- **PyAutoGUI**: Screen automation and control
- **NumPy**: Numerical computing
- **Pillow**: Image processing
- **Colorama**: Terminal color output

### Acknowledgments
- **Minecraft Community**: For inspiration and feedback
- **Open Source Contributors**: For the libraries used
- **Beta Testers**: For bug reports and suggestions
- **Documentation Writers**: For comprehensive guides

### Contact & Support
- **Issues**: Report bugs via GitHub issues
- **Feature Requests**: Submit via GitHub discussions
- **Documentation**: Check README.md and inline comments
- **Community**: Join our Discord server (if available)

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Setup
python setup.py

# Launch
python launcher.py

# Direct run
python minecraft_farm_bot.py
python advanced_farm_bot.py
```

### Key Hotkeys
- **F1**: Start/Stop
- **F2**: Pause/Resume  
- **F3**: Exit
- **F4**: Statistics (Advanced)

### Important Files
- `config.ini` - Bot configuration
- `minecraft_bot.log` - Activity logs
- `bot_stats_*.json` - Statistics data

### Support
- Read this README thoroughly
- Check the troubleshooting section
- Review configuration options
- Test in safe environment first

---

**🌾 Happy Farming! 🌾**

*Made with ❤️ by DDS*

*Remember: The best farms are those tended with care, even when automated!* 

