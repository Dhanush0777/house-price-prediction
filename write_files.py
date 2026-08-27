import os, glob

base_dir = r'C:\Users\Dhanush Teja\OneDrive\Desktop\project\project'
static_dirs = [
    os.path.join(base_dir, 'backend', 'src', 'main', 'resources', 'static'),
    os.path.join(base_dir, 'backend', 'target', 'classes', 'static'),
    os.path.join(base_dir, 'frontend')
]

def save_file(rel_path, content):
    for s_dir in static_dirs:
        if os.path.exists(s_dir):
            full_p = os.path.join(s_dir, rel_path)
            os.makedirs(os.path.dirname(full_p), exist_ok=True)
            with open(full_p, 'w', encoding='utf-8') as out:
                out.write(content)
            print('Saved:', full_p)
