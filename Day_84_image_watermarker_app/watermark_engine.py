import os
import json
import time
import logging
import requests # Added for mock cloud upload
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageStat

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("watermark.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class WatermarkLayer:
    """
    Represents a single watermark overlay, allowing an image to have infinite layers.
    Types: 'text', 'image', 'shape'
    """
    def __init__(self, layer_type: str, **kwargs):
        self.type = layer_type
        self.kwargs = kwargs

    def to_dict(self):
        return {"type": self.type, "kwargs": self.kwargs}

    @classmethod
    def from_dict(cls, data):
        return cls(data["type"], **data["kwargs"])


class WatermarkTemplate:
    """Handles saving and loading multiple layers to/from JSON."""
    def __init__(self, layers=None):
        self.layers = layers if layers is not None else []

    def add_layer(self, layer: WatermarkLayer):
        self.layers.append(layer)

    def save_template(self, filepath: str):
        data = [layer.to_dict() for layer in self.layers]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Template saved to {filepath}")

    @classmethod
    def load_template(cls, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        layers = [WatermarkLayer.from_dict(d) for d in data]
        return cls(layers)


def suggest_watermark_defaults(base_image: Image.Image) -> dict:
    """
    AI heuristics helper to suggest optimal watermark settings based on image properties.
    """
    img_w, img_h = base_image.size
    
    # 1. Auto-resize: Suggest font size roughly 5% of the image height
    suggested_font_size = max(12, int(img_h * 0.05))
    suggested_logo_scale = max(0.1, min(1.0, 300 / max(img_w, img_h)))
    
    # Estimate typical watermark size for variance check
    est_wm_w, est_wm_h = int(img_w * 0.25), int(img_h * 0.1)
    
    best_pos, variance, brightness = _analyze_smart_placement(base_image, (est_wm_w, est_wm_h))
    
    # 2. Suggest Color/Opacity based on the brightness of that target area
    # If the target area is dark (average pixel brightness < 128), suggest white
    if brightness < 128:
        suggested_color = (255, 255, 255)  
        suggested_opacity = 200 
    else:
        suggested_color = (0, 0, 0)     
        suggested_opacity = 150 
        
    return {
        "position": best_pos,
        "font_size": suggested_font_size,
        "scale": round(suggested_logo_scale, 2),
        "color": suggested_color,
        "opacity": suggested_opacity
    }

def _analyze_smart_placement(base_image: Image.Image, wm_size: tuple[int, int], margin: int = 20) -> tuple[str, float, float]:
    """Returns (best_position_name, min_variance, average_brightness_of_region)"""
    img_w, img_h = base_image.size
    wm_w, wm_h = wm_size
    
    candidates = {
        "top-left": (margin, margin, margin + wm_w, margin + wm_h),
        "top-right": (img_w - wm_w - margin, margin, img_w - margin, margin + wm_h),
        "bottom-left": (margin, img_h - wm_h - margin, margin + wm_w, img_h - margin),
        "bottom-right": (img_w - wm_w - margin, img_h - wm_h - margin, img_w - margin, img_h - margin),
        "center": ((img_w - wm_w) // 2, (img_h - wm_h) // 2, (img_w + wm_w) // 2, (img_h + wm_h) // 2)
    }

    best_pos = "bottom-right"
    min_variance = float('inf')
    best_brightness = 127
    grayscale = base_image.convert("L")

    for pos_name, box in candidates.items():
        if box[2] > img_w or box[3] > img_h:
            continue
            
        region = grayscale.crop(box)
        stat = ImageStat.Stat(region)
        variance = stat.var[0]
        brightness = stat.mean[0]
        
        if variance < min_variance:
            min_variance = variance
            best_pos = pos_name
            best_brightness = brightness

    return best_pos, min_variance, best_brightness

def _get_smart_position(base_image: Image.Image, wm_size: tuple[int, int], margin: int = 20) -> tuple[int, int]:
    """
    Analyzes image contrast/variance across 5 key sectors to find the region 
    with the least 'detail' (lowest variance) to place the watermark cleanly.
    """
    best_pos_name, _, _ = _analyze_smart_placement(base_image, wm_size, margin)
    return _calculate_position(base_image.size, wm_size, best_pos_name, margin)


def _calculate_position(base_size: tuple[int, int], wm_size: tuple[int, int], position: str, margin: int = 20, custom_coords: tuple[int, int] = None, base_image: Image.Image = None) -> tuple[int, int]:
    if custom_coords is not None and position.lower() == "custom":
        return custom_coords
        
    if position.lower() == "smart" and base_image is not None:
        return _get_smart_position(base_image, wm_size, margin)

    image_width, image_height = base_size
    wm_width, wm_height = wm_size
    position = position.lower()
    
    if position == "top-left": return (margin, margin)
    elif position == "top-right": return (image_width - wm_width - margin, margin)
    elif position == "bottom-left": return (margin, image_height - wm_height - margin)
    elif position == "bottom-right": return (image_width - wm_width - margin, image_height - wm_height - margin)
    elif position == "center": return ((image_width - wm_width) // 2, (image_height - wm_height) // 2)
    else: return (image_width - wm_width - margin, image_height - wm_height - margin)


def apply_watermark_layers(input_image_path: str, output_path: str, layers: list[WatermarkLayer]) -> bool:
    """
    Core rendering pipeline handling infinite layer stacking (text, image, shape).
    """
    try:
        with Image.open(input_image_path) as base_image:
            base_image = base_image.convert("RGBA")
            
            for layer in layers:
                render_func = PLUGIN_REGISTRY.get(layer.type)
                if render_func:
                    render_func(base_image, layer.kwargs)
                    pos = layer.kwargs.get("position", "smart")
                    logging.info(f"Watermark Applied -> File: {os.path.basename(input_image_path)} | Type: {layer.type} | Position: {pos}")
                else:
                    logging.warning(f"Unsupported watermark structure requested: {layer.type}")

            # Save operation (supporting PNG, JPEG, and WebP natively)
            if output_path.lower().endswith(('.jpg', '.jpeg')):
                out = base_image.convert("RGB")
                out.save(output_path, "JPEG", quality=95)
            elif output_path.lower().endswith('.webp'):
                base_image.save(output_path, "WEBP", quality=90, lossless=False)
            else:
                base_image.save(output_path, "PNG")
                
            return True
    except Exception as e:
        logging.error(f"Render failed on {input_image_path}: {e}")
        return False

# --- Private Rendering Routines (Operate inline via memory references) ---

def _render_text_layer(base_image: Image.Image, kwargs: dict):
    text = kwargs.get("text", "")
    if not text: return
    
    opacity = kwargs.get("opacity", 128)
    color = kwargs.get("color", (255, 255, 255))
    font_path = kwargs.get("font_path", None)
    font_size = kwargs.get("font_size", 36)
    position = kwargs.get("position", "bottom-right")
    custom_coords = kwargs.get("custom_coords", None)
    
    overlay = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        if font_path and os.path.exists(font_path) and font_path != "Default":
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
        
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    tw, th = (right - left), (bottom - top)
    
    x, y = _calculate_position(base_image.size, (tw, th), position, custom_coords=custom_coords, base_image=base_image)
    watermark_color = (*color[:3], opacity)
    draw.text((x, y), text, font=font, fill=watermark_color)
    
    base_image.alpha_composite(overlay)


def _render_image_layer(base_image: Image.Image, kwargs: dict):
    logo_path = kwargs.get("logo_path", None)
    if not logo_path or not os.path.exists(logo_path): return
    
    opacity = kwargs.get("opacity", 128)
    scale = kwargs.get("scale", 1.0)
    position = kwargs.get("position", "bottom-right")
    custom_coords = kwargs.get("custom_coords", None)
    
    with Image.open(logo_path) as logo:
        logo = logo.convert("RGBA")
        
        if scale != 1.0 and scale > 0:
            new_size = (int(logo.width * scale), int(logo.height * scale))
            logo = logo.resize(new_size, Image.Resampling.LANCZOS)
            
        if opacity < 255:
            r, g, b, a = logo.split()
            a = a.point(lambda p: int(p * (opacity / 255.0)))
            logo = Image.merge("RGBA", (r, g, b, a))
            
        x, y = _calculate_position(base_image.size, logo.size, position, custom_coords=custom_coords, base_image=base_image)
        
        overlay = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
        overlay.paste(logo, (int(x), int(y)), mask=logo)
        base_image.alpha_composite(overlay)


def _render_shape_layer(base_image: Image.Image, kwargs: dict):
    shape_type = kwargs.get("shape_type", "rectangle") # rectangle, ellipse
    width = kwargs.get("width", 200)
    height = kwargs.get("height", 100)
    color = kwargs.get("color", (0, 0, 0))
    opacity = kwargs.get("opacity", 128)
    position = kwargs.get("position", "center")
    custom_coords = kwargs.get("custom_coords", None)
    
    overlay = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    x, y = _calculate_position(base_image.size, (width, height), position, custom_coords=custom_coords, base_image=base_image)
    fill_color = (*color[:3], opacity)
    
    bounds = [x, y, x + width, y + height]
    if shape_type == "rectangle":
        draw.rectangle(bounds, fill=fill_color)
    elif shape_type == "ellipse":
        draw.ellipse(bounds, fill=fill_color)
        
    base_image.alpha_composite(overlay)

# ==========================================
# PLUGIN REGISTRY (Future-Proofing / Scalability)
# ==========================================

PLUGIN_REGISTRY = {
    "text": _render_text_layer,
    "image": _render_image_layer,
    "shape": _render_shape_layer,
}

def register_watermark_plugin(layer_type: str, render_func):
    """Allows dynamic addition of new watermark capabilities without modifying core engine."""
    PLUGIN_REGISTRY[layer_type] = render_func
    logging.info(f"Registered new plugin type: {layer_type}")

# ==========================================
# MULTIPROCESSING BATCH PIPELINE
# ==========================================

def _batch_worker(args):
    """Pickleable worker function deployed to remote CPU cores."""
    i_path, o_path, serialized_layers = args
    layers = [WatermarkLayer.from_dict(d) for d in serialized_layers]
    success = apply_watermark_layers(i_path, o_path, layers)
    return success

def process_batch_multicore(
    input_folder: str, 
    output_folder: str, 
    template: WatermarkTemplate, 
    output_format: str = "png",
    max_workers: int = None
) -> tuple[int, int]:
    """
    Massively accelerated batch processing utilizing `concurrent.futures.ProcessPoolExecutor` 
    to saturate all available CPU threads with watermark tasks, overcoming Python's GIL.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
        
    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
    serialized_layers = [L.to_dict() for L in template.layers]
    
    tasks = []
    
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(supported_extensions):
            continue
            
        input_filepath = os.path.join(input_folder, filename)
        base_name, _ = os.path.splitext(filename)
        output_filepath = os.path.join(output_folder, f"{base_name}_watermarked.{output_format.lower()}")
        
        # We package args to be pickleable for ProcessPoolExecutor communication
        tasks.append((input_filepath, output_filepath, serialized_layers))
        
    total_count = len(tasks)
    success_count = 0
    
    if total_count == 0:
        return 0, 0
        
    # Launch parallel processing pool 
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(_batch_worker, tasks)
        for val in results:
            if val:
                success_count += 1
                
    return success_count, total_count

# ==========================================
# CLOUD INTEGRATION (MOCK API)
# ==========================================

def upload_to_cloud(filepath: str, api_endpoint: str = "https://mock.api/upload", api_key: str = None) -> bool:
    """
    Mock integration mapping displaying how to structure exporting local 
    watermarked photos automatically to an external service (e.g. S3, Drive, Dropbox).
    """
    if not os.path.exists(filepath):
        logging.error(f"Cannot upload missing file: {filepath}")
        return False
        
    logging.info(f"Initiating cloud upload for: {os.path.basename(filepath)}")
    
    # Example logic demonstrating standard Python requests library integration
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    files = {'file': open(filepath, 'rb')}
    
    try:
        # In a real environment, this line would execute:
        # response = requests.post(api_endpoint, files=files, headers=headers, timeout=15)
        
        # MOCK response logic
        time.sleep(1.0) # Simulate network transit time
        logging.info(f"✅ Successfully uploaded {os.path.basename(filepath)} to Cloud Server")
        return True
    except requests.RequestException as e:
        logging.error(f"Cloud Network failure: {e}")
        return False
    finally:
        files['file'].close()
