import os
import subprocess
import time
import urllib.request

base_dir = r"C:\Users\Dhanush Teja\OneDrive\Desktop\project\project"

# 1. Start Python ML service on port 5001 if not already answering
ml_py = os.path.join(base_dir, "ml_service", "app.py")
py_proc = subprocess.Popen(["python", ml_py], cwd=base_dir)
print("Started ML microservice PID:", py_proc.pid)

# 2. Extract classpath from run_backend.bat and start Java backend
bat_path = os.path.join(base_dir, "run_backend.bat")
with open(bat_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
cmd_line = [l for l in lines if "java -cp" in l][0].strip()
cp_val = cmd_line.split('java -cp "')[1].split('" com.houseprice.HousePriceApplication')[0]

java_proc = subprocess.Popen(
    ["java", "-cp", cp_val, "com.houseprice.HousePriceApplication"],
    cwd=base_dir
)
print("Started Java Spring Boot backend PID:", java_proc.pid)

# Wait for port 8080 to become ready
print("Waiting for server on http://localhost:8080 ...")
for i in range(20):
    time.sleep(1)
    try:
        r = urllib.request.urlopen("http://localhost:8080/api/locations")
        if r.status == 200:
            print("SERVER IS READY ON http://localhost:8080")
            break
    except Exception:
        pass

try:
    java_proc.wait()
except KeyboardInterrupt:
    py_proc.terminate()
    java_proc.terminate()
