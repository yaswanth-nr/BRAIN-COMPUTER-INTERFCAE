import pyautogui
import time
import threading
from collections import deque

class BrainControlInterface:
    def __init__(self):
        # Disable pyautogui failsafe for demo purposes (be careful!)
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Control parameters
        self.cursor_speed = 10
        self.last_action_time = 0
        self.action_cooldown = 0.5  # seconds between actions
        
        # Attention-based cursor control
        self.cursor_position = [pyautogui.size()[0] // 2, pyautogui.size()[1] // 2]
        self.cursor_direction = 0  # 0=right, 1=down, 2=left, 3=up
        
        # Alpha state actions
        self.alpha_actions = deque([
            self.type_letter_a,
            self.type_letter_b,
            self.type_letter_c,
            self.open_notepad,
            self.open_calculator,
            self.open_browser
        ])
        self.current_alpha_action = 0
        
    def execute_blink_action(self):
        """Execute mouse click on blink detection"""
        current_time = time.time()
        if current_time - self.last_action_time < self.action_cooldown:
            return False
            
        try:
            pyautogui.click()
            self.last_action_time = current_time
            print("Blink detected - Mouse click executed")
            return True
        except Exception as e:
            print(f"Error executing blink action: {e}")
            return False
            
    def control_cursor_with_attention(self, attention_level):
        """Control cursor movement based on attention level"""
        if attention_level < 20:
            return  # Too low attention, no movement
            
        # Map attention level to cursor speed
        speed = int((attention_level / 100) * self.cursor_speed)
        
        # Move cursor in current direction
        dx, dy = 0, 0
        if self.cursor_direction == 0:    # Right
            dx = speed
        elif self.cursor_direction == 1:  # Down
            dy = speed
        elif self.cursor_direction == 2:  # Left
            dx = -speed
        elif self.cursor_direction == 3:  # Up
            dy = -speed
            
        # Update cursor position
        new_x = max(0, min(pyautogui.size()[0], self.cursor_position[0] + dx))
        new_y = max(0, min(pyautogui.size()[1], self.cursor_position[1] + dy))
        
        self.cursor_position = [new_x, new_y]
        
        try:
            pyautogui.moveTo(new_x, new_y)
            
            # Change direction periodically based on attention fluctuations
            if attention_level > 80:
                self.cursor_direction = (self.cursor_direction + 1) % 4
                
        except Exception as e:
            print(f"Error controlling cursor: {e}")
            
    def execute_alpha_action(self):
        """Execute action when in alpha state"""
        current_time = time.time()
        if current_time - self.last_action_time < self.action_cooldown * 2:  # Longer cooldown for alpha actions
            return False
            
        try:
            # Execute current alpha action
            action = self.alpha_actions[self.current_alpha_action]
            action()
            
            # Move to next action
            self.current_alpha_action = (self.current_alpha_action + 1) % len(self.alpha_actions)
            self.last_action_time = current_time
            
            print(f"Alpha state detected - Action {self.current_alpha_action} executed")
            return True
            
        except Exception as e:
            print(f"Error executing alpha action: {e}")
            return False
            
    def type_letter_a(self):
        """Type letter 'a'"""
        pyautogui.typewrite('a')
        
    def type_letter_b(self):
        """Type letter 'b'"""
        pyautogui.typewrite('b')
        
    def type_letter_c(self):
        """Type letter 'c'"""
        pyautogui.typewrite('c')
        
    def open_notepad(self):
        """Open Notepad application"""
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.typewrite('notepad')
        pyautogui.press('enter')
        
    def open_calculator(self):
        """Open Calculator application"""
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.typewrite('calc')
        pyautogui.press('enter')
        
    def open_browser(self):
        """Open default web browser"""
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.typewrite('chrome')
        pyautogui.press('enter')
        
    def smart_app_launcher(self, app_index):
        """Launch specific app based on brain signal pattern"""
        apps = [
            ('notepad', 'Notepad'),
            ('calc', 'Calculator'),
            ('chrome', 'Chrome Browser'),
            ('mspaint', 'Paint'),
            ('explorer', 'File Explorer'),
            ('cmd', 'Command Prompt')
        ]
        
        if 0 <= app_index < len(apps):
            try:
                pyautogui.hotkey('win', 'r')
                time.sleep(0.5)
                pyautogui.typewrite(apps[app_index][0])
                pyautogui.press('enter')
                print(f"Launched {apps[app_index][1]}")
                return True
            except Exception as e:
                print(f"Error launching app: {e}")
                return False
        return False
        
    def gaming_control(self, control_type, value):
        """Control games using brain signals"""
        try:
            if control_type == "move_left":
                pyautogui.keyDown('left')
                time.sleep(0.1)
                pyautogui.keyUp('left')
            elif control_type == "move_right":
                pyautogui.keyDown('right')
                time.sleep(0.1)
                pyautogui.keyUp('right')
            elif control_type == "jump":
                pyautogui.press('space')
            elif control_type == "action":
                pyautogui.press('enter')
            elif control_type == "pause":
                pyautogui.press('p')
                
            return True
        except Exception as e:
            print(f"Error in gaming control: {e}")
            return False
            
    def typing_assistant(self, text):
        """Type text using brain signals"""
        try:
            pyautogui.typewrite(text, interval=0.1)
            return True
        except Exception as e:
            print(f"Error in typing assistant: {e}")
            return False
            
    def window_management(self, action):
        """Manage windows using brain signals"""
        try:
            if action == "minimize":
                pyautogui.hotkey('win', 'down')
            elif action == "maximize":
                pyautogui.hotkey('win', 'up')
            elif action == "close":
                pyautogui.hotkey('alt', 'f4')
            elif action == "switch":
                pyautogui.hotkey('alt', 'tab')
            elif action == "desktop":
                pyautogui.hotkey('win', 'd')
                
            return True
        except Exception as e:
            print(f"Error in window management: {e}")
            return False
            
    def accessibility_features(self, feature):
        """Accessibility features for users with disabilities"""
        try:
            if feature == "magnifier":
                pyautogui.hotkey('win', 'plus')
            elif feature == "narrator":
                pyautogui.hotkey('win', 'ctrl', 'enter')
            elif feature == "on_screen_keyboard":
                pyautogui.hotkey('win', 'ctrl', 'o')
            elif feature == "high_contrast":
                pyautogui.hotkey('left alt', 'left shift', 'printscreen')
                
            return True
        except Exception as e:
            print(f"Error in accessibility features: {e}")
            return False
            
    def process_brain_signals(self, signal_data):
        """Main processing function for brain signals"""
        try:
            # Extract signal data
            blink_detected = signal_data.get('blink_detected', False)
            attention_level = signal_data.get('attention_level', 0)
            alpha_state = signal_data.get('alpha_state', False)
            
            # Execute actions based on signals
            actions_executed = []
            
            if blink_detected:
                if self.execute_blink_action():
                    actions_executed.append("mouse_click")
                    
            if attention_level > 30:
                self.control_cursor_with_attention(attention_level)
                actions_executed.append("cursor_control")
                
            if alpha_state:
                if self.execute_alpha_action():
                    actions_executed.append("alpha_action")
                    
            return {
                "actions_executed": actions_executed,
                "cursor_position": self.cursor_position,
                "attention_level": attention_level
            }
            
        except Exception as e:
            print(f"Error processing brain signals: {e}")
            return {"error": str(e)}

