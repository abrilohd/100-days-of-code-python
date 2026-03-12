import os
import copy
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageTk

# New modular SDK integrations
from watermark_engine import (
    WatermarkLayer, 
    WatermarkTemplate, 
    apply_watermark_layers, 
    process_batch_multicore,
    upload_to_cloud,
    suggest_watermark_defaults
)

# ==========================================
# ADVANCED UX COMPONENTS
# ==========================================

class Tooltip:
    """A professional balloon tooltip implementation for Tkinter widgets."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text: return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

# Multi-language support configuration
LOCALES = {
    "en": {
        "title": "Image Watermarking Pro",
        "btn_upload_base": "📂 Upload Image",
        "lbl_base_none": "No image selected",
        "frame_mode": "Watermark Stack Operations",
        "btn_add_text": "+ Add Text Layer",
        "btn_add_img": "+ Add Logo Layer",
        "btn_undo": "↩ Undo",
        "btn_redo": "↪ Redo",
        "btn_save_tpl": "💾 Save Template",
        "btn_load_tpl": "📂 Load Template",
        "btn_save_img": "📸 Export Single Image",
        "btn_batch": "🔁 Batch Process Folder",
        "lbl_preview": "Interactive Preview (Drag items or resize window)",
        "lbl_lang": "Language:"
    },
    "es": {
        "title": "Marca de Agua Pro",
        "btn_upload_base": "📂 Subir Imagen",
        "lbl_base_none": "Ninguna imagen seleccionada",
        "frame_mode": "Operaciones de Capa",
        "btn_add_text": "+ Añadir Texto",
        "btn_add_img": "+ Añadir Logo",
        "btn_undo": "↩ Deshacer",
        "btn_redo": "↪ Rehacer",
        "btn_save_tpl": "💾 Guardar Plantilla",
        "btn_load_tpl": "📂 Cargar Plantilla",
        "btn_save_img": "📸 Exportar Imagen",
        "btn_batch": "🔁 Procesar Carpeta",
        "lbl_preview": "Vista Previa (Arrastre items o redimensione)",
        "lbl_lang": "Idioma:"
    }
}

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.lang = "en"
        self.root.title(LOCALES[self.lang]["title"])
        self.root.geometry("1300x800")
        
        # --- Memory State Trackers ---
        self.base_image_path = None
        self.base_image_pil = None         
        self.template = WatermarkTemplate()
        
        # --- Undo / Redo Stacks ---
        # Stores deep copies of self.template.layers 
        self.history_stack = [[]] 
        self.redo_stack = []
        
        # --- Interface Modifiers ---
        self.is_dark_mode = False
        self.themes = {
            "light": {"bg": "#f0f0f0", "fg": "black", "pane_bg": "#ddd", "frame_bg": "#ffffff", "canvas_bg": "#1e1e1e", "btn_bg": "#e0e0e0"},
            "dark": {"bg": "#2b2b2b", "fg": "white", "pane_bg": "#444", "frame_bg": "#3c3f41", "canvas_bg": "#1e1e1e", "btn_bg": "#555"}
        }
        
        self.preview_scale_factor = 1.0 
        self.preview_offset_x = 0
        self.preview_offset_y = 0
        
        self.create_widgets()
        self.apply_theme()
        
    def create_widgets(self):
        # 1. Top Navigation & Localization Bar
        nav_bar = tk.Frame(self.root, pady=5, padx=10)
        nav_bar.pack(fill="x", side="top")
        
        self.lbl_lang = tk.Label(nav_bar, text=LOCALES[self.lang]["lbl_lang"])
        self.lbl_lang.pack(side="left")
        self.lang_var = tk.StringVar(value="en")
        lang_dropdown = ttk.Combobox(nav_bar, textvariable=self.lang_var, values=["en", "es"], state="readonly", width=5)
        lang_dropdown.pack(side="left", padx=5)
        lang_dropdown.bind("<<ComboboxSelected>>", self.change_language)
        
        self.theme_btn = tk.Button(nav_bar, text="🌙 Dark Mode", command=self.toggle_theme, bg="#555", fg="white", relief="flat")
        self.theme_btn.pack(side="right")
        Tooltip(self.theme_btn, "Toggle between Light and Dark interface themes")

        # 2. Main Resizable Splitted Panels
        self.main_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=5, bg="#ddd")
        self.main_pane.pack(fill="both", expand=True)
        
        # ================= LEFT: Control Panel =================
        self.control_frame = tk.Frame(self.main_pane, width=400, padx=15, pady=15)
        self.main_pane.add(self.control_frame, minsize=380)
        
        # Base Image UI
        upload_frame = tk.Frame(self.control_frame, pady=5)
        upload_frame.pack(fill="x")
        self.btn_upload_base = tk.Button(upload_frame, text=LOCALES[self.lang]["btn_upload_base"], command=self.upload_base_image, bg="#e0e0e0")
        self.btn_upload_base.pack(side="left")
        Tooltip(self.btn_upload_base, "Select the background image to apply watermarks to")
        self.lbl_base_none = tk.Label(upload_frame, text=LOCALES[self.lang]["lbl_base_none"], fg="gray")
        self.lbl_base_none.pack(side="left", padx=10)
        
        # Layer Management Frame
        self.layer_frame = tk.LabelFrame(self.control_frame, text=LOCALES[self.lang]["frame_mode"], pady=10, padx=10)
        self.layer_frame.pack(fill="x", pady=10)
        
        btn_box = tk.Frame(self.layer_frame)
        btn_box.pack(fill="x", pady=5)
        self.btn_add_text = tk.Button(btn_box, text=LOCALES[self.lang]["btn_add_text"], command=self.add_text_layer, bg="#4CAF50", fg="white")
        self.btn_add_text.pack(side="left", expand=True, fill="x", padx=2)
        self.btn_add_img = tk.Button(btn_box, text=LOCALES[self.lang]["btn_add_img"], command=self.add_image_layer, bg="#2196F3", fg="white")
        self.btn_add_img.pack(side="left", expand=True, fill="x", padx=2)
        
        history_box = tk.Frame(self.layer_frame)
        history_box.pack(fill="x", pady=5)
        self.btn_undo = tk.Button(history_box, text=LOCALES[self.lang]["btn_undo"], command=self.undo)
        self.btn_undo.pack(side="left", expand=True, fill="x", padx=2)
        Tooltip(self.btn_undo, "Revert the last added watermark layer")
        self.btn_redo = tk.Button(history_box, text=LOCALES[self.lang]["btn_redo"], command=self.redo)
        self.btn_redo.pack(side="left", expand=True, fill="x", padx=2)
        
        template_box = tk.Frame(self.layer_frame)
        template_box.pack(fill="x", pady=5)
        self.btn_save_tpl = tk.Button(template_box, text=LOCALES[self.lang]["btn_save_tpl"], command=self.save_template)
        self.btn_save_tpl.pack(side="left", expand=True, fill="x", padx=2)
        Tooltip(self.btn_save_tpl, "Save the current stack of watermarks to a .json file for future use")
        self.btn_load_tpl = tk.Button(template_box, text=LOCALES[self.lang]["btn_load_tpl"], command=self.load_template)
        self.btn_load_tpl.pack(side="left", expand=True, fill="x", padx=2)

        # Active Layers Listbox
        tk.Label(self.layer_frame, text="Active Layers (Stack):").pack(anchor="w")
        self.layer_listbox = tk.Listbox(self.layer_frame, height=8)
        self.layer_listbox.pack(fill="x", pady=5)
        btn_del_layer = tk.Button(self.layer_frame, text="❌ Delete Selected Layer", command=self.delete_selected_layer)
        btn_del_layer.pack(fill="x")
        
        # Action Triggers
        action_frame = tk.Frame(self.control_frame, pady=20)
        action_frame.pack(fill="x", side="bottom")
        
        self.btn_save_img = tk.Button(action_frame, text=LOCALES[self.lang]["btn_save_img"], command=self.process_single, bg="#008CBA", fg="white", font=("Arial", 11, "bold"), pady=5)
        self.btn_save_img.pack(fill="x", pady=2)
        
        # New Cloud Export Button
        self.btn_cloud = tk.Button(action_frame, text="☁️ Upload to Cloud", command=self.upload_cloud_image, bg="#673AB7", fg="white", font=("Arial", 11, "bold"), pady=5)
        self.btn_cloud.pack(fill="x", pady=2)
        
        self.btn_batch = tk.Button(action_frame, text=LOCALES[self.lang]["btn_batch"], command=self.process_batch, bg="#ff9800", fg="white", font=("Arial", 11, "bold"), pady=5)
        self.btn_batch.pack(fill="x", pady=2)
        Tooltip(self.btn_batch, "Utilizes maximum CPU cores to watermark hundreds of photos instantly")
        
        # ================= RIGHT: Live Preview Canvas =================
        self.preview_frame = tk.Frame(self.main_pane, bg="#2d2d2d")
        self.main_pane.add(self.preview_frame)
        
        self.lbl_preview = tk.Label(self.preview_frame, text=LOCALES[self.lang]["lbl_preview"], bg="#2d2d2d", fg="white", font=("Arial", 11, "italic"))
        self.lbl_preview.pack(pady=10)
        
        self.canvas = tk.Canvas(self.preview_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Bind dynamic resizing recalculations & interactive dragging
        self.canvas.bind("<Configure>", lambda e: self.update_preview())
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
    def on_canvas_drag(self, event):
        if not self.base_image_pil or not self.template.layers: return
        
        selected = self.layer_listbox.curselection()
        if not selected: return
            
        index = selected[0]
        layer = self.template.layers[index]
        
        # Guard check if preview factors have been generated yet
        if not hasattr(self, 'preview_scale_factor'): return
        
        # Convert raw canvas pixel to original high-res image space
        img_x = int((event.x - self.preview_offset_x) / self.preview_scale_factor)
        img_y = int((event.y - self.preview_offset_y) / self.preview_scale_factor)
        
        img_w, img_h = self.base_image_pil.size
        img_x = max(0, min(img_x, img_w))
        img_y = max(0, min(img_y, img_h))
        
        layer.kwargs["position"] = "custom"
        layer.kwargs["custom_coords"] = (img_x, img_y)
        
        self.update_preview()

    def on_canvas_release(self, event):
        selected = self.layer_listbox.curselection()
        if selected: self.save_state() # Push the dragged coordinate into the Undo/Redo matrix
    
    # --- LANGUAGE & THEME LOGIC ---
    def change_language(self, event=None):
        self.lang = self.lang_var.get()
        L = LOCALES[self.lang]
        self.root.title(L["title"])
        self.lbl_lang.config(text=L["lbl_lang"])
        self.btn_upload_base.config(text=L["btn_upload_base"])
        self.lbl_base_none.config(text=L["lbl_base_none"] if not self.base_image_path else os.path.basename(self.base_image_path))
        self.layer_frame.config(text=L["frame_mode"])
        self.btn_add_text.config(text=L["btn_add_text"])
        self.btn_add_img.config(text=L["btn_add_img"])
        self.btn_undo.config(text=L["btn_undo"])
        self.btn_redo.config(text=L["btn_redo"])
        self.btn_save_tpl.config(text=L["btn_save_tpl"])
        self.btn_load_tpl.config(text=L["btn_load_tpl"])
        self.btn_save_img.config(text=L["btn_save_img"])
        self.btn_batch.config(text=L["btn_batch"])
        self.lbl_preview.config(text=L["lbl_preview"])
        
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_btn.config(text="☀️ Light Mode" if self.is_dark_mode else "🌙 Dark Mode")
        self.apply_theme()

    def apply_theme(self):
        t = self.themes["dark"] if self.is_dark_mode else self.themes["light"]
        self.root.configure(bg=t["bg"])
        self.main_pane.configure(bg=t["pane_bg"])
        
        def repaint_widget(widget):
            try:
                # Exclude explicitly colored semantic buttons
                is_semantic = isinstance(widget, tk.Button) and widget.cget("bg") in ["#008CBA", "#ff9800", "#4CAF50", "#2196F3"]
                if not is_semantic and widget != self.theme_btn:
                    if isinstance(widget, (tk.Frame, tk.LabelFrame)): widget.configure(bg=t["bg"])
                    elif isinstance(widget, tk.Label): widget.configure(bg=t["bg"], fg=t["fg"])
                    elif isinstance(widget, tk.Button): widget.configure(bg=t["btn_bg"], fg=t["fg"])
                    elif isinstance(widget, tk.Listbox): widget.configure(bg=t["frame_bg"], fg=t["fg"])
            except: pass
            for child in widget.winfo_children(): repaint_widget(child)
        repaint_widget(self.root)

    # --- STATE MANAGEMENT (UNDO/REDO) ---
    def save_state(self):
        """Creates a deep copy of the engine's layers matrix before modifications."""
        current_state = copy.deepcopy(self.template.layers)
        self.history_stack.append(current_state)
        # Clearing redo stack because we made a new branching change
        self.redo_stack.clear() 
        self.refresh_layer_listbox()
        self.update_preview()
        
    def undo(self):
        if len(self.history_stack) > 1:
            current_state = self.history_stack.pop()
            self.redo_stack.append(current_state)
            self.template.layers = copy.deepcopy(self.history_stack[-1])
            self.refresh_layer_listbox()
            self.update_preview()
            
    def redo(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.history_stack.append(state)
            self.template.layers = copy.deepcopy(state)
            self.refresh_layer_listbox()
            self.update_preview()
            
    def refresh_layer_listbox(self):
        self.layer_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.template.layers):
            desc = f"[{layer.type.upper()}] "
            if layer.type == "text": desc += layer.kwargs.get("text", "")[:15]
            if layer.type == "image": desc += os.path.basename(layer.kwargs.get("logo_path", ""))
            self.layer_listbox.insert(tk.END, f"{i+1}. {desc}")

    def delete_selected_layer(self):
        sel = self.layer_listbox.curselection()
        if sel:
            idx = sel[0]
            self.template.layers.pop(idx)
            self.save_state()

    # --- ADDING WATERMARK UI POPUPS ---
    def add_text_layer(self):
        # Fetch AI heuristics if a base image has already been loaded for intelligent defaults
        ai_suggests = {}
        if self.base_image_pil:
            ai_suggests = suggest_watermark_defaults(self.base_image_pil)
            
        default_color = ai_suggests.get("color", (255, 255, 255))
        default_opacity = ai_suggests.get("opacity", 150)
        default_size = ai_suggests.get("font_size", 80)
        
        # A more advanced popup dialog to configure basic text layer properties initially
        top = tk.Toplevel(self.root)
        top.title("Add Text AI Suggestions")
        top.geometry("400x300")
        
        tk.Label(top, text="Text:").pack(pady=5)
        txt_var = tk.StringVar(value="Watermark")
        tk.Entry(top, textvariable=txt_var, width=30).pack()
        
        # Color Palette Selector
        color_frame = tk.Frame(top)
        color_frame.pack(pady=10)
        
        selected_color = {"rgb": default_color}
        
        def set_color(hex_code):
            h = hex_code.lstrip('#')
            selected_color["rgb"] = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            lbl_color_preview.config(bg=hex_code)
            
        def pick_custom():
            color_code = colorchooser.askcolor(title="Choose color", initialcolor='#%02x%02x%02x' % default_color)[1]
            if color_code: set_color(color_code)
            
        tk.Button(color_frame, text="🎨 Custom", command=pick_custom).pack(side="left", padx=5)
        lbl_color_preview = tk.Label(color_frame, width=3, bg='#%02x%02x%02x' % default_color, relief="sunken")
        lbl_color_preview.pack(side="left", padx=10)
        
        # Quick-select palette blocks
        palette_box = tk.Frame(color_frame)
        palette_box.pack(side="left")
        for hex_color in ["#ffffff", "#000000", "#ff0000", "#00ff00", "#0000ff", "#ffff00"]:
            tk.Button(palette_box, bg=hex_color, width=2, height=1, relief="ridge", command=lambda c=hex_color: set_color(c)).pack(side="left", padx=1)
            
        # Font fetcher looking inside assets/fonts dynamically
        font_dir = os.path.join(os.path.dirname(__file__), "assets", "fonts")
        fonts = ["Default"]
        if os.path.exists(font_dir):
            for f in os.listdir(font_dir):
                if f.lower().endswith(('.ttf', '.otf')):
                    fonts.append(os.path.join(font_dir, f))
                    
        font_frame = tk.Frame(top)
        font_frame.pack(pady=10)
        tk.Label(font_frame, text="Font:").pack(side="left")
        
        font_var = tk.StringVar(value="Default")
        
        def update_font_preview(event=None):
            sel = font_var.get()
            if sel != "Default":
                family = os.path.splitext(sel)[0]
                try: lbl_font_preview.config(font=(family, 14))
                except: pass
            else:
                lbl_font_preview.config(font=("Arial", 14))
                
        font_dropdown = ttk.Combobox(font_frame, textvariable=font_var, values=[os.path.basename(f) for f in fonts], state="readonly", width=15)
        self.font_paths_mapping = {os.path.basename(f): f for f in fonts} 
        font_dropdown.pack(side="left", padx=5)
        font_dropdown.bind("<<ComboboxSelected>>", update_font_preview)
        
        lbl_font_preview = tk.Label(font_frame, text=" Ag", font=("Arial", 14))
        lbl_font_preview.pack(side="left")

        # Position Dropdown
        pos_frame = tk.Frame(top)
        pos_frame.pack(pady=5)
        tk.Label(pos_frame, text="Position:").pack(side="left")
        pos_var = tk.StringVar(value=ai_suggests.get("position", "smart"))
        ttk.Combobox(pos_frame, textvariable=pos_var, values=["smart", "top-left", "top-right", "bottom-left", "bottom-right", "center"], state="readonly", width=12).pack(side="left", padx=5)

        # Size & Opacity Sliders
        sliders_frame = tk.Frame(top)
        sliders_frame.pack(pady=10)
        tk.Label(sliders_frame, text="Font Size:").grid(row=0, column=0, sticky="e")
        size_slider = tk.Scale(sliders_frame, from_=10, to=240, orient="horizontal", length=150)
        size_slider.set(default_size)
        size_slider.grid(row=0, column=1)
        
        tk.Label(sliders_frame, text="Opacity:").grid(row=1, column=0, sticky="e")
        opacity_slider = tk.Scale(sliders_frame, from_=0, to=255, orient="horizontal", length=150)
        opacity_slider.set(default_opacity)
        opacity_slider.grid(row=1, column=1)

        def submit():
            text = txt_var.get()
            if text:
                f_key = font_var.get()
                f_path = self.font_paths_mapping.get(f_key, "Default")
                
                layer = WatermarkLayer(
                    layer_type="text",
                    text=text,
                    position=pos_var.get(), 
                    opacity=int(opacity_slider.get()),
                    color=selected_color["rgb"],
                    font_size=int(size_slider.get()),
                    font_path=f_path
                )
                self.template.add_layer(layer)
                self.save_state()
                top.destroy()
                
        tk.Button(top, text="Add Text Watermark", command=submit, bg="#4CAF50", fg="white").pack(pady=15)
            
    def add_image_layer(self):
        ai_suggests = {}
        if self.base_image_pil:
            ai_suggests = suggest_watermark_defaults(self.base_image_pil)
            
        path = filedialog.askopenfilename(title="Select Logo", filetypes=(("Images", "*.png *.jpg *.jpeg"),))
        if not path: return
            
        top = tk.Toplevel(self.root)
        top.title("Configure Image Watermark")
        top.geometry("350x250")
        
        # Position Dropdown
        pos_frame = tk.Frame(top)
        pos_frame.pack(pady=10)
        tk.Label(pos_frame, text="Position:").pack(side="left")
        pos_var = tk.StringVar(value=ai_suggests.get("position", "smart"))
        ttk.Combobox(pos_frame, textvariable=pos_var, values=["smart", "top-left", "top-right", "bottom-left", "bottom-right", "center"], state="readonly", width=12).pack(side="left", padx=5)

        # Size & Opacity Sliders
        sliders_frame = tk.Frame(top)
        sliders_frame.pack(pady=10)
        
        tk.Label(sliders_frame, text="Scale (0.1 - 2.0):").grid(row=0, column=0, sticky="e")
        scale_slider = tk.Scale(sliders_frame, from_=0.1, to=2.0, resolution=0.1, orient="horizontal", length=150)
        scale_slider.set(ai_suggests.get("scale", 0.5))
        scale_slider.grid(row=0, column=1)
        
        tk.Label(sliders_frame, text="Opacity:").grid(row=1, column=0, sticky="e")
        opacity_slider = tk.Scale(sliders_frame, from_=0, to=255, orient="horizontal", length=150)
        opacity_slider.set(ai_suggests.get("opacity", 200))
        opacity_slider.grid(row=1, column=1)

        def submit():
            layer = WatermarkLayer(
                layer_type="image",
                logo_path=path,
                position=pos_var.get(),
                opacity=int(opacity_slider.get()),
                scale=float(scale_slider.get())
            )
            self.template.add_layer(layer)
            self.save_state()
            top.destroy()
            
        tk.Button(top, text="Add Logo Layer", command=submit, bg="#4CAF50", fg="white").pack(pady=15)
            
    # --- TEMPLATE JSON I/O ---
    def save_template(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if path:
            self.template.save_template(path)
            messagebox.showinfo("Success", "Template saved successfully!")
            
    def load_template(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            try:
                self.template = WatermarkTemplate.load_template(path)
                self.save_state()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON template:\n{e}")

    # --- CANVAS LIVE PREVIEW ---
    def upload_base_image(self):
        path = filedialog.askopenfilename(title="Select Base Image")
        if path:
            self.base_image_path = path
            self.lbl_base_none.config(text=os.path.basename(path), fg="black")
            try:
                self.base_image_pil = Image.open(path).convert("RGBA")
                self.update_preview()
            except Exception as e:
                messagebox.showerror("IO Error", f"Failed to load image: {e}")

    def update_preview(self, event=None):
        if not self.base_image_pil: return
        
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w < 50 or canvas_h < 50: return 
        
        # Calculate exactly how to scale the massive image into the resizable window
        img_w, img_h = self.base_image_pil.size
        scale_w = canvas_w / img_w
        scale_h = canvas_h / img_h
        self.preview_scale_factor = min(scale_w, scale_h) * 0.95 
        
        new_w = max(1, int(img_w * self.preview_scale_factor))
        new_h = max(1, int(img_h * self.preview_scale_factor))
        
        # Generate the fast GPU-friendly ghost representation
        preview_base = self.base_image_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Manually invoke the exact rendering pipeline code from the engine!
        # Because the engine expects file paths, we simulate it via the private _render functions
        import watermark_engine
        for layer in self.template.layers:
            # We scale all layer configs temporarily by the GUI preview constraints
            ghost_kwargs = copy.deepcopy(layer.kwargs)
            
            # Map scaling math
            if "font_size" in ghost_kwargs: ghost_kwargs["font_size"] = max(8, int(ghost_kwargs["font_size"] * self.preview_scale_factor))
            if "scale" in ghost_kwargs: ghost_kwargs["scale"] = ghost_kwargs["scale"] * self.preview_scale_factor
            if "width" in ghost_kwargs: ghost_kwargs["width"] = int(ghost_kwargs["width"] * self.preview_scale_factor)
            if "height" in ghost_kwargs: ghost_kwargs["height"] = int(ghost_kwargs["height"] * self.preview_scale_factor)
            
            # Render exactly as production engine does
            if layer.type == "text": watermark_engine._render_text_layer(preview_base, ghost_kwargs)
            elif layer.type == "image": watermark_engine._render_image_layer(preview_base, ghost_kwargs)
            elif layer.type == "shape": watermark_engine._render_shape_layer(preview_base, ghost_kwargs)
            
        self.preview_photo = ImageTk.PhotoImage(preview_base)
        self.canvas.delete("all")
        
        self.preview_offset_x = (canvas_w - new_w) // 2
        self.preview_offset_y = (canvas_h - new_h) // 2
        self.canvas.create_image(self.preview_offset_x, self.preview_offset_y, anchor="nw", image=self.preview_photo)

    # --- PROCESS EXECUTION EXPORTERS ---
    def process_single(self):
        if not self.base_image_path or not self.template.layers:
            messagebox.showwarning("Warning", "Ensure you have an image and at least one watermark layer.")
            return
            
        # Feature: Auto-generated dynamic filename based on the original image
        import time 
        base_name = os.path.splitext(os.path.basename(self.base_image_path))[0]
        timestamp = time.strftime("%Y%m%d-%H%M")
        suggested_name = f"{base_name}_watermarked_{timestamp}.png"
        
        out_path = filedialog.asksaveasfilename(
            initialfile=suggested_name,
            defaultextension=".png", 
            filetypes=[("PNG (Lossless)", "*.png"), ("JPEG (Web)", "*.jpg"), ("WebP (Next Gen)", "*.webp")]
        )
        if out_path:
            # Invoking the production engine pipeline!
            success = apply_watermark_layers(self.base_image_path, out_path, self.template.layers)
            if success: messagebox.showinfo("Success", f"Exported: {out_path}")
            
    def upload_cloud_image(self):
        if not self.base_image_path or not self.template.layers:
            messagebox.showwarning("Warning", "Ensure you have an image and at least one watermark layer.")
            return
            
        # Generate temporary processed file
        import tempfile
        import time
        fd, temp_path = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        
        success = apply_watermark_layers(self.base_image_path, temp_path, self.template.layers)
        if success:
            top = tk.Toplevel(self.root)
            top.title("Uploading...")
            tk.Label(top, text="Transmitting to Secure Cloud SDK...\n(Mock Network Activity)", padx=20, pady=20).pack()
            self.root.update()
            
            # Hooking into the decoupled Engine Mock SDK
            upload_success = upload_to_cloud(temp_path)
            
            top.destroy()
            if upload_success:
                messagebox.showinfo("Cloud Upload", "Successfully transmitted watermarked image to remote server!")
            else:
                messagebox.showerror("Error", "Cloud connection failed.")
                
        # Clean up memory leak footprint
        try: os.remove(temp_path)
        except: pass
        
    def process_batch(self):
        if not self.template.layers:
            messagebox.showwarning("Warning", "Add at least one layer to the stack first.")
            return
            
        messagebox.showinfo("Batch Info", "Ensure your template is finalized. The engine will now utilize all CPU cores to crunch through a folder.")
        i_dir = filedialog.askdirectory(title="Input Folder")
        if not i_dir: return
        o_dir = filedialog.askdirectory(title="Output Folder")
        if not o_dir: return
        
        try:
            # Invokes the massively optimized Multiprocessing framework over the GIL!
            s_count, t_count = process_batch_multicore(i_dir, o_dir, self.template)
            messagebox.showinfo("Success", f"Batch Complete! Watermarked {s_count}/{t_count} images.")
        except Exception as e:
            messagebox.showerror("Crash", f"Multicore execution failure: {e}")

if __name__ == "__main__":
    import multiprocessing
    # Required safely initializing multicore processing pools in windows scripts
    multiprocessing.freeze_support() 
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
