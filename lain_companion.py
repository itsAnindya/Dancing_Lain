import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import random

class CompanionWindow:
    # Class variable to store all companion instances
    all_companions = []
    
    def __init__(self, gif_path, root=None):
        self.gif_path = gif_path
        
        # Use provided root or create new one
        if root is None:
            self.window = tk.Tk()
            self.is_main_window = True
        else:
            self.window = tk.Toplevel(root)
            self.is_main_window = False
        
        self.window.title("Lain Companion")
        
        # Make window transparent and always on top
        self.window.attributes('-topmost', True)
        self.window.attributes('-transparentcolor', self.window['bg'])
        
        # Remove window decorations for a floating effect
        self.window.overrideredirect(True)
        
        # Load GIF
        try:
            self.gif = Image.open(gif_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load GIF: {e}")
            self.window.destroy()
            return
        
        # Get frame count
        self.frames = []
        self.durations = []
        try:
            for frame_idx in range(self.gif.n_frames):
                self.gif.seek(frame_idx)
                # Get frame duration (default 100ms if not specified)
                duration = self.gif.info.get('duration', 100)
                self.durations.append(duration)
                # Convert frame to PhotoImage
                self.frames.append(ImageTk.PhotoImage(self.gif.convert('RGBA')))
        except Exception as e:
            messagebox.showerror("Error", f"Could not process GIF frames: {e}")
            self.window.destroy()
            return
        
        # Create label to display image
        self.label = tk.Label(self.window, image=self.frames[0], bd=0, bg='SystemButtonFace')
        self.label.pack()
        
        # Window size
        self.window.geometry(f"{self.gif.width}x{self.gif.height}+100+100")
        
        # Variables for dragging
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.current_frame = 0
        self.animating = True
        self.ctrl_pressed = False
        
        # Bind mouse events for dragging
        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.drag_window)
        self.label.bind('<ButtonRelease-1>', self.stop_drag)
        
        # Bind Ctrl+drag events
        self.label.bind('<Control-Button-1>', self.start_drag_all)
        self.label.bind('<Control-B1-Motion>', self.drag_all_windows)
        self.label.bind('<Control-ButtonRelease-1>', self.stop_drag_all)
        
        # Add this instance to the class list
        CompanionWindow.all_companions.append(self)
        
        # Start animation
        self.animate()
        
        # Instruction label (optional)
        print("Companion window created! Drag with mouse to move.")
        print("Right-click to close (or close the window normally)")
    
    def start_drag(self, event):
        """Store the initial mouse position"""
        self.drag_start_x = event.x_root - self.window.winfo_x()
        self.drag_start_y = event.y_root - self.window.winfo_y()
    
    def drag_window(self, event):
        """Move the window while dragging"""
        new_x = event.x_root - self.drag_start_x
        new_y = event.y_root - self.drag_start_y
        self.window.geometry(f"+{new_x}+{new_y}")
    
    def stop_drag(self, event):
        """Stop dragging"""
        pass
    
    def start_drag_all(self, event):
        """Store the initial mouse position for dragging all windows"""
        self.drag_start_x = event.x_root - self.window.winfo_x()
        self.drag_start_y = event.y_root - self.window.winfo_y()
        self.ctrl_pressed = True
    
    def drag_all_windows(self, event):
        """Move all windows while Ctrl+dragging"""
        if not self.ctrl_pressed:
            return
        
        new_x = event.x_root - self.drag_start_x
        new_y = event.y_root - self.drag_start_y
        
        # Calculate the offset
        offset_x = new_x - self.window.winfo_x()
        offset_y = new_y - self.window.winfo_y()
        
        # Move all companions by this offset
        for companion in CompanionWindow.all_companions:
            current_x = companion.window.winfo_x()
            current_y = companion.window.winfo_y()
            companion.window.geometry(f"+{current_x + offset_x}+{current_y + offset_y}")
        
        # Update drag start for next iteration
        self.drag_start_x = event.x_root - self.window.winfo_x()
        self.drag_start_y = event.y_root - self.window.winfo_y()
    
    def stop_drag_all(self, event):
        """Stop dragging all windows"""
        self.ctrl_pressed = False
    
    def animate(self):
        """Animate through the GIF frames"""
        if not self.animating or not self.frames:
            return
        
        # Update frame
        self.label.config(image=self.frames[self.current_frame])
        
        # Schedule next frame
        duration = self.durations[self.current_frame]
        self.window.after(duration, self.animate)
        
        # Move to next frame
        self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def run(self):
        """Start the main event loop"""
        self.window.mainloop()

if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gif_path = os.path.join(script_dir, "lain-dancing.gif")
    
    # Parse command line arguments
    num_companions = 1
    if len(sys.argv) > 1:
        try:
            num_companions = int(sys.argv[1])
            if num_companions < 1:
                print("Number of companions must be at least 1")
                num_companions = 1
            elif num_companions > 20:
                print("Warning: Creating more than 20 companions may impact performance")
        except ValueError:
            print(f"Invalid argument: '{sys.argv[1]}'. Please provide a number.")
            print("Usage: python lain_companion.py [number_of_companions]")
            sys.exit(1)
    
    # Check if GIF exists
    if not os.path.exists(gif_path):
        print(f"Error: {gif_path} not found!")
        print("Make sure lain-dancing.gif is in the same directory as this script.")
        sys.exit(1)
    
    # Create multiple companions
    companions = []
    root_window = tk.Tk()
    root_window.withdraw()  # Hide the root window
    
    for i in range(num_companions):
        # Offset each companion's starting position
        start_x = 100 + (i % 5) * 150
        start_y = 100 + (i // 5) * 150
        
        companion = CompanionWindow(gif_path, root=root_window)
        # Move window to offset position
        companion.window.geometry(f"{companion.gif.width}x{companion.gif.height}+{start_x}+{start_y}")
        companions.append(companion)
    
    print(f"Created {num_companions} companion(s)!")
    if num_companions > 1:
        print("All companions can be dragged independently.")
    
    # Run all companions together
    if companions:
        root_window.mainloop()
