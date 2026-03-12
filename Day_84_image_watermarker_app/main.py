import tkinter as tk
import multiprocessing
from gui import WatermarkApp

def main():
    """
    Entry point for the Image Watermark Application.
    """
    # Required safely initializing multicore processing pools in windows scripts
    multiprocessing.freeze_support() 
    
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
