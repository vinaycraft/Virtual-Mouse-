"""
Virtual Mouse Configuration Utility
Easily customize gesture thresholds and settings
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class GestureConfig:
    """Configuration for gesture detection thresholds"""
    # Distance thresholds (0.0 to 1.0, smaller = more sensitive)
    click_threshold: float = 0.03
    double_click_threshold: float = 0.02
    right_click_threshold: float = 0.03
    scroll_threshold: float = 0.03
    move_threshold: float = 0.15
    
    # Timing settings
    action_cooldown: float = 0.3  # Seconds between actions
    gesture_cooldown: float = 0.1  # Seconds between gesture detections
    
    # Performance settings
    smoothing_factor: float = 0.7  # 0.0 to 1.0, higher = smoother
    confidence_threshold: float = 0.7  # Hand detection confidence
    
    # Camera settings
    camera_width: int = 640
    camera_height: int = 480
    camera_fps: int = 30
    
    # Display settings
    show_fps: bool = True
    show_instructions: bool = True
    show_landmarks: bool = True
    
    def save_to_file(self, filename: str = "virtual_mouse_config.json"):
        """Save configuration to JSON file"""
        config_dict = asdict(self)
        with open(filename, 'w') as f:
            json.dump(config_dict, f, indent=4)
        print(f"✅ Configuration saved to {filename}")
    
    @classmethod
    def load_from_file(cls, filename: str = "virtual_mouse_config.json"):
        """Load configuration from JSON file"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                config_dict = json.load(f)
            print(f"✅ Configuration loaded from {filename}")
            return cls(**config_dict)
        else:
            print(f"⚠️ Configuration file {filename} not found, using defaults")
            return cls()
    
    def create_presets(self) -> Dict[str, Dict[str, Any]]:
        """Create different configuration presets"""
        return {
            "precise": {
                "click_threshold": 0.02,
                "double_click_threshold": 0.015,
                "right_click_threshold": 0.02,
                "scroll_threshold": 0.02,
                "move_threshold": 0.1,
                "smoothing_factor": 0.8,
                "action_cooldown": 0.2
            },
            "responsive": {
                "click_threshold": 0.04,
                "double_click_threshold": 0.025,
                "right_click_threshold": 0.04,
                "scroll_threshold": 0.04,
                "move_threshold": 0.2,
                "smoothing_factor": 0.5,
                "action_cooldown": 0.15
            },
            "beginner": {
                "click_threshold": 0.06,
                "double_click_threshold": 0.04,
                "right_click_threshold": 0.06,
                "scroll_threshold": 0.06,
                "move_threshold": 0.25,
                "smoothing_factor": 0.9,
                "action_cooldown": 0.5
            }
        }
    
    def apply_preset(self, preset_name: str):
        """Apply a configuration preset"""
        presets = self.create_presets()
        if preset_name in presets:
            preset_config = presets[preset_name]
            for key, value in preset_config.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            print(f"✅ Applied '{preset_name}' preset")
        else:
            print(f"❌ Preset '{preset_name}' not found. Available: {list(presets.keys())}")

def create_config_wizard():
    """Interactive configuration wizard"""
    print("🧙‍♂️ Virtual Mouse Configuration Wizard")
    print("=" * 50)
    
    config = GestureConfig()
    
    # Let user choose preset
    print("\n📋 Choose a preset:")
    print("1. Precise - High accuracy, less sensitive")
    print("2. Responsive - Balanced performance")
    print("3. Beginner - More forgiving gestures")
    print("4. Custom - Manual configuration")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    presets = {"1": "precise", "2": "responsive", "3": "beginner"}
    
    if choice in presets:
        config.apply_preset(presets[choice])
    elif choice == "4":
        print("\n⚙️ Custom Configuration")
        print("Enter values (0.0-1.0 for thresholds, higher = less sensitive)")
        
        try:
            config.click_threshold = float(input("Click threshold (default 0.03): ") or "0.03")
            config.double_click_threshold = float(input("Double click threshold (default 0.02): ") or "0.02")
            config.right_click_threshold = float(input("Right click threshold (default 0.03): ") or "0.03")
            config.scroll_threshold = float(input("Scroll threshold (default 0.03): ") or "0.03")
            config.move_threshold = float(input("Move threshold (default 0.15): ") or "0.15")
            config.smoothing_factor = float(input("Smoothing factor 0.0-1.0 (default 0.7): ") or "0.7")
        except ValueError:
            print("❌ Invalid input, using defaults")
    
    # Save configuration
    config.save_to_file()
    
    print("\n✨ Configuration complete!")
    print("📁 Config saved as 'virtual_mouse_config.json'")
    print("🚀 Run 'python virtual_mouse_enhanced.py' to start")
    
    return config

if __name__ == "__main__":
    create_config_wizard()
