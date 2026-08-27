import os

base_dir = r"C:\Users\Dhanush Teja\OneDrive\Desktop\project\project"
static_dirs = [
    os.path.join(base_dir, "backend", "src", "main", "resources", "static"),
    os.path.join(base_dir, "backend", "target", "classes", "static"),
    os.path.join(base_dir, "frontend")
]

def save(rel_path, content):
    for s in static_dirs:
        if os.path.exists(s):
            out_p = os.path.join(s, rel_path)
            os.makedirs(os.path.dirname(out_p), exist_ok=True)
            with open(out_p, "w", encoding="utf-8") as f:
                f.write(content)
            print("Saved:", out_p)

print("build_all.py initialized successfully")
