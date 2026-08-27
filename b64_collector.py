import base64, os
chunks = []
def add(b64):
    chunks.append(base64.b64decode(b64.encode('utf-8')).decode('utf-8'))
def save_all(rel):
    content = ''.join(chunks)
    base_dir = r'C:\Users\Dhanush Teja\OneDrive\Desktop\project\project'
    dirs = [
        os.path.join(base_dir, 'backend', 'src', 'main', 'resources', 'static'),
        os.path.join(base_dir, 'backend', 'target', 'classes', 'static'),
        os.path.join(base_dir, 'frontend')
    ]
    for d in dirs:
        if os.path.exists(d):
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8') as out:
                out.write(content)
            print('Saved', p)
