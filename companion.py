import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import argparse
import random

class CompanionWindow:
    # Class variable to store all companion instances
    all_companions = []
    
    def __init__(self, gif_path, root=None, max_width=None, max_height=None):
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
        
        # Determine target size based on max bounds (preserve aspect ratio)
        orig_w, orig_h = self.gif.width, self.gif.height
        target_w, target_h = orig_w, orig_h
        if max_width is not None or max_height is not None:
            mw = max_width if max_width is not None else orig_w
            mh = max_height if max_height is not None else orig_h
            scale = min(mw / orig_w, mh / orig_h, 1.0)
            target_w = max(1, int(orig_w * scale))
            target_h = max(1, int(orig_h * scale))
        else:
            scale = 1.0

        self.image_width = target_w
        self.image_height = target_h

        # Get frame count
        self.frames = []
        self.durations = []
        try:
            for frame_idx in range(self.gif.n_frames):
                self.gif.seek(frame_idx)
                # Get frame duration (default 100ms if not specified)
                duration = self.gif.info.get('duration', 100)
                self.durations.append(duration)
                # Convert frame to PhotoImage, resizing if necessary
                frame_img = self.gif.convert('RGBA').copy()
                if scale < 1.0:
                    frame_img = frame_img.resize((target_w, target_h), Image.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame_img))
        except Exception as e:
            messagebox.showerror("Error", f"Could not process GIF frames: {e}")
            self.window.destroy()
            return
        
        # Create label to display image
        self.label = tk.Label(self.window, image=self.frames[0], bd=0, bg='SystemButtonFace')
        self.label.pack()
        
        # Window size
        self.window.geometry(f"{self.image_width}x{self.image_height}+100+100")
        
        # Variables for dragging
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.current_frame = 0
        self.animating = True
        self.ctrl_pressed = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
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
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        self.last_mouse_x = event.x_root
        self.last_mouse_y = event.y_root
        self.ctrl_pressed = True
    
    def drag_all_windows(self, event):
        """Move all windows while Ctrl+dragging"""
        if not self.ctrl_pressed:
            return
        
        # Calculate the delta from the last mouse position
        delta_x = event.x_root - self.last_mouse_x
        delta_y = event.y_root - self.last_mouse_y
        
        # Update last mouse position
        self.last_mouse_x = event.x_root
        self.last_mouse_y = event.y_root
        
        # Move all companions by this delta
        for companion in CompanionWindow.all_companions:
            current_x = companion.window.winfo_x()
            current_y = companion.window.winfo_y()
            companion.window.geometry(f"+{current_x + delta_x}+{current_y + delta_y}")
    
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

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Lain Companion")
    parser.add_argument("--count", "-n", type=int, default=1, help="Number of companions")
    parser.add_argument("--gif-id", "-g", type=int, help="GIF id in gifs/ directory (e.g., 1 -> gifs/1.gif)")
    parser.add_argument("--gif", type=str, help="Explicit path to GIF (overrides --gif-id)")
    parser.add_argument("--max-width", type=int, help="Maximum width in pixels for resizing (defaults to 400)")
    parser.add_argument("--max-height", type=int, help="Maximum height in pixels for resizing (defaults to 400)")
    parser.add_argument("--no-resize", action="store_true", help="Disable resizing; use original GIF size")
    args = parser.parse_args()

    # Determine GIF path
    if args.gif:
        gif_path = args.gif
    elif args.gif_id is not None:
        gif_path = os.path.join(script_dir, f"gifs/{args.gif_id}.gif")
    else:
        gif_path = os.path.join(script_dir, "gifs/1.gif")

    # Validate count
    num_companions = args.count
    if num_companions < 1:
        print("Number of companions must be at least 1")
        num_companions = 1
    elif num_companions > 20:
        print("Warning: Creating more than 20 companions may impact performance")

    # Check if GIF exists
    if not os.path.exists(gif_path):
        print(f"Error: {gif_path} not found!")
        print("Ensure the GIF exists or specify a valid --gif path.")
        sys.exit(1)

    # Resizing bounds
    DEFAULT_MAX_W = 400
    DEFAULT_MAX_H = 400
    if args.no_resize:
        max_w = None
        max_h = None
    else:
        max_w = args.max_width if args.max_width is not None else DEFAULT_MAX_W
        max_h = args.max_height if args.max_height is not None else DEFAULT_MAX_H

    # Create multiple companions
    companions = []
    root_window = tk.Tk()
    root_window.withdraw()  # Hide the root window

    for i in range(num_companions):
        # Offset each companion's starting position
        start_x = 100 + (i % 5) * 150
        start_y = 100 + (i // 5) * 150

        companion = CompanionWindow(gif_path, root=root_window, max_width=max_w, max_height=max_h)
        # Move window to offset position using resized dimensions
        companion.window.geometry(f"{companion.image_width}x{companion.image_height}+{start_x}+{start_y}")
        companions.append(companion)

    print(f"Created {num_companions} companion(s)!")
    if num_companions > 1:
        print("All companions can be dragged independently.")

    # Run all companions together
    if companions:
        root_window.mainloop()