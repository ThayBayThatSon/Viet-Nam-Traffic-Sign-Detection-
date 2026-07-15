import os
import base64
import re

html_path = "presentation.html"
output_path = "presentation_standalone.html"

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

def replace_img_src(match):
    src = match.group(1)
    if src.startswith("http") or src.startswith("data:"):
        return match.group(0) # Keep URL or already base64
    
    # Path might be relative, let's read it
    img_path = os.path.join(".", src.replace("/", os.sep))
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            img_data = img_file.read()
            b64_data = base64.b64encode(img_data).decode("utf-8")
            
            ext = os.path.splitext(img_path)[1].lower()
            if ext == ".png":
                mime = "image/png"
            elif ext in [".jpg", ".jpeg"]:
                mime = "image/jpeg"
            elif ext == ".webp":
                mime = "image/webp"
            elif ext == ".gif":
                mime = "image/gif"
            elif ext == ".svg":
                mime = "image/svg+xml"
            else:
                mime = "image/png" # fallback
                
            new_src = f"data:{mime};base64,{b64_data}"
            return match.group(0).replace(src, new_src)
    return match.group(0) # If file not found, keep as is

new_html = re.sub(r'<img[^>]+src="([^"]+)"', replace_img_src, html_content)
# Also handle single quotes just in case
new_html = re.sub(r"<img[^>]+src='([^']+)'", replace_img_src, new_html)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Standalone HTML generated successfully.")
