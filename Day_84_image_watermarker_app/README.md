# Image Watermarking Pro

A modular, beginner-friendly, and professional Python desktop application for watermarking images. Built with Tkinter and Pillow, this application allows users to fully customize and apply text or image-based watermarks, featuring live real-time previews, drag-and-drop positioning, and robust batch processing capabilities.

## 🚀 Features Currently Implemented

*   **Text & Image Watermarks**: Add custom text or overlay your logo.
*   **Live Interactive Preview**: See all changes in real-time before committing.
*   **Drag-and-Drop Positioning**: Intuitively move watermarks around the live canvas.
*   **Advanced Parameter Controls**: Adjust opacity, scale, color, and font size.
*   **Batch Processing Integration**: Select an input and output directory to apply an identical watermark configuration to hundreds of photos automatically.
*   **Dark Mode GUI**: Toggle seamlessly between Light and Dark application themes.
*   **Multiple Formats Supported**: Load from standard formats and export reliably to standard, transparent PNG or compressed JPEG.
*   **Dynamic Font Loading**: Place `.ttf` or `.otf` files into an `assets/fonts/` directory and they are automatically loaded!
*   **Strict Separation of Concerns**: Clean modular architecture making `gui.py` independent from `watermark_engine.py` for high maintainability.

---

## 💻 Getting Started

### Installation (Portable Executable)
The easiest way to run Image Watermarking Pro is to use the standalone executable. You do **not** need Python installed.
1. Download the latest `WatermarkApp.exe` release (or generate your own via the Developer steps below).
2. Double-click to run! 

### Developer Setup (Source Code)
1.  Clone or download the repository to your local machine.
2.  Ensure you have **Python 3.7+** installed.
3.  Install the required dependencies via `pip`:
    ```bash
    pip install Pillow
    ```
4. Run the application directly:
    ```bash
    python gui.py
    ```

### 📦 Packaging for Distribution (PyInstaller)
To compile your own cross-platform executable, install PyInstaller (`pip install pyinstaller`) and run the build command for your respective operating system from the project root:

**Windows:**
```bash
python -m PyInstaller --noconfirm --onedir --windowed --name "WatermarkApp" --add-data "assets/fonts/*;assets/fonts/" "main.py"
```
*(Find your built `.exe` inside the generated `dist/WatermarkApp/` folder).*

**macOS:**
```bash
python3 -m PyInstaller --noconfirm --onedir --windowed --name "WatermarkApp" --add-data "assets/fonts/*:assets/fonts/" "main.py"
```

**Linux:**
```bash
python3 -m PyInstaller --noconfirm --onedir --windowed --name "WatermarkApp" --add-data "assets/fonts/*:assets/fonts/" "main.py"
```
*Note: macOS and Linux use a colon `:` instead of a semicolon `;` for the `--add-data` separator.*

---

## 🗺️ Roadmap & Future Enhancements
This project is continuously evolving. As a portfolio piece, the codebase is being prepped for the following advanced functionalities:

### 1️⃣ Advanced User Experience (UX)
*   Resizable preview window (zoom in/out capabilities).
*   Undo/Redo watermark edits to easily correct mistakes.
*   Multi-language support (English, etc.).
*   Tooltips and help guides explicitly explaining each GUI element.

### 2️⃣ Enhanced Watermark Features
*   Custom shapes or repetitive patterns as watermarks.
*   Placing multiple distinct watermarks on the same image simultaneously.
*   Smart Positioning: Dynamically detect and place watermarks based on contrast and content.
*   Watermark Templates: Save your favorite configurations to reuse later without re-entering values.

### 3️⃣ Performance & Optimization
*   Performance optimizations for processing extremely large images.
*   GPU acceleration processing using frameworks such as OpenCV or PyTorch.
*   Memory optimizations to handle processing thousands of images at once seamlessly.

### 4️⃣ Export & Integration
*   Export to web-optimized next-generation formats (e.g., WebP).
*   Direct API integration to upload to social media, Google Drive, or Dropbox.
*   Project auto-save mechanisms to keep your place.

### 5️⃣ Customization & Personalization
*   Expanded Theme Customizations (e.g., Modern, High-Contrast modes).
*   Dynamic font preview explicitly shown within the dropdown selector itself.

### 6️⃣ Automation & AI Enhancements
*   AI-powered void detection for the perfect un-intrusive watermark placement.
*   Automatic watermark resizing scaling flawlessly relative to image resolution.
*   AI suggestions finding the optimal color/opacity to blend into the base photo cleanly.

### 7️⃣ Professional Packaging
*   Executable builds provided for Windows (`.exe`), macOS (`.app`), and Linux.
*   Standardized installers encapsulating external dependencies.
*   Tutorial videos available for portfolio demos.

### 8️⃣ Analytics & Logging
*   Local usage tracking to determine the most used fonts and colors.
*   Detailed error/crash logging routines for swift debugging and improvement.

### 9️⃣ Cloud & Web Integration
*   Web version built utilizing Flask or PyWebView.
*   External API endpoints mapped allowing for headless remote watermarking.

### 🔟 Future-Proofing
*   Plugin support allowing the open-source community to add unique new watermark effects.
*   Consistent version control to showcase iterative, continuous development.
