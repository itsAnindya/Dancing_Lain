# Lain Companion

A Python desktop companion application featuring Lain from *Serial Experiments Lain* (1998). Watch her dance on your screen while working, with the ability to drag her around—individually or as a group!

## Features

- 🎬 **Animated GIF Display**: Smooth animation of Lain dancing
- 🖱️ **Draggable Windows**: Click and drag to move companions around your screen
- 👥 **Multiple Companions**: Spawn multiple copies with a command-line parameter
- 🎯 **Group Dragging**: Hold Ctrl while dragging to move all companions together
- 🎨 **Borderless Design**: Clean, floating window aesthetic
- 📌 **Always on Top**: Companions stay visible above other windows

## Usage

### Basic Usage

Run with a single companion:
```bash
python companion.py
```

### Multiple Companions

Spawn multiple companions:
```bash
python companion.py --count 3
python companion.py --count 5
```

Companions are automatically positioned in a grid pattern and can be dragged independently.

Select GIF by id from the `gifs/` directory:
```bash
python companion.py --gif-id 2
```

Resize oversized GIFs (aspect preserved):
```bash
python companion.py --gif-id 3 --max-width 400 --max-height 400
```

Disable resizing and use original GIF size:
```bash
python companion.py --gif-id 4 --no-resize
```

### Controls

- **Left Click + Drag**: Move a single companion
- **Ctrl + Left Click + Drag**: Move all companions together (maintaining their relative positions)
- **Close Window**: Right-click on the window or use the close button to exit

## Requirements

- Python 3.7+
- `Pillow` (PIL) for GIF handling
- `tkinter` (usually included with Python)

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install Pillow
```

3. Run the application:
```bash
python companion.py [--count N] [--gif-id ID] [--max-width W] [--max-height H] [--no-resize]
```

## Project Structure

```
Companion_Lain/
├── companion.py            # Main application
├── gifs/                   # GIF assets (e.g., 1.gif, 2.gif, ...)
└── README.md               # This file
```

## Credits

### GIF Asset
The dancing Lain GIF was sourced from [Tenor](https://tenor.com/) by the user **schwagerin**.

### Character & Source Material
- **Character**: Lain Iwakura
- **Source**: *Serial Experiments Lain* (1998) - A psychological sci-fi anime series
- **Studio**: Triangle Staff, Yoshitoshi ABe, and others

This project is a fan creation and is not affiliated with the official *Serial Experiments Lain* franchise.

## License

This project is provided as-is for personal and educational use. The animated GIF and related artwork are subject to their original creators' rights. Please respect the intellectual property of Triangle Staff and the creators of *Serial Experiments Lain*.

## Notes

- Performance may degrade with more than 20 companions simultaneously
- The application works best on Windows with standard screen resolutions
- The window is set to always-on-top mode, so it may appear above other full-screen applications

## Troubleshooting

**Issue**: GIF not loading
- **Solution**: Ensure the GIF exists (e.g., `gifs/1.gif`) or provide a valid path via `--gif`

**Issue**: Multiple windows not appearing
- **Solution**: The application creates a hidden root window to manage all companions. Ensure tkinter is properly installed.

**Issue**: Slow performance with many companions
- **Solution**: Reduce the number of companions being displayed

---

Made with ✨ and a love for *Serial Experiments Lain*
