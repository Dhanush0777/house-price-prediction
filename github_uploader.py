import os
import base64
import json
import urllib.request
import urllib.error

def upload_project_to_github(token, repo_name="house-price-prediction", is_private=False):
    base_dir = r"C:\Users\Dhanush Teja\OneDrive\Desktop\project\project"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "EstateAI-Uploader"
    }

    # 1. Get user info
    req = urllib.request.Request("https://api.github.com/user", headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            user_data = json.loads(resp.read().decode("utf-8"))
            username = user_data.get("login")
            print(f"[+] Authenticated as GitHub user: {username}")
    except Exception as e:
        print(f"[!] Authentication failed: {e}")
        return False

    # 2. Create repository if not exists
    create_repo_payload = {
        "name": repo_name,
        "description": "AI-Based House Price Prediction & Real Estate Valuation System",
        "private": is_private,
        "auto_init": False
    }
    req_create = urllib.request.Request(
        "https://api.github.com/user/repos",
        data=json.dumps(create_repo_payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req_create) as resp:
            print(f"[+] Repository '{repo_name}' created successfully on GitHub!")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"[*] Repository '{repo_name}' already exists, continuing to upload files...")
        else:
            print(f"[!] Failed to create repository: {e}")

    # 3. Upload files
    ignore_dirs = {'.git', 'target', '__pycache__', '.venv', 'env', 'extracted_lib', '.vscode'}
    ignore_files = {'backend_stdout.log', 'backend_stderr.log', 'spring_stdout.log', 'spring_stderr.log', 'java_out.log', 'java_err.log', 'backend_run.log', 'house-price-prediction-github-ready.zip'}

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        for f in files:
            if f in ignore_files or f.endswith('.log') or f.endswith('.class'):
                continue
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, base_dir).replace('\\', '/')

            with open(full_p, 'rb') as file_obj:
                content_bytes = file_obj.read()
                b64_content = base64.b64encode(content_bytes).decode('utf-8')

            put_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{rel_p}"

            # Check if file exists to get sha
            sha = None
            try:
                check_req = urllib.request.Request(put_url, headers=headers)
                with urllib.request.urlopen(check_req) as cr:
                    cdata = json.loads(cr.read().decode('utf-8'))
                    sha = cdata.get('sha')
            except Exception:
                pass

            put_payload = {
                "message": f"Add {rel_p}",
                "content": b64_content,
                "branch": "main"
            }
            if sha:
                put_payload["sha"] = sha

            put_req = urllib.request.Request(
                put_url,
                data=json.dumps(put_payload).encode('utf-8'),
                headers=headers,
                method="PUT"
            )
            try:
                with urllib.request.urlopen(put_req) as pr:
                    print(f"[*] Uploaded: {rel_p}")
            except Exception as pe:
                print(f"[!] Upload failed for {rel_p}: {pe}")

    print(f"\n=======================================================")
    print(f"[+] All files uploaded to: https://github.com/{username}/{repo_name}")
    print(f"=======================================================\n")
    return True

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        tok = sys.argv[1]
        upload_project_to_github(tok)
    else:
        print("Usage: python github_uploader.py <YOUR_GITHUB_TOKEN>")
