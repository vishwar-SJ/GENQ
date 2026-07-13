import requests

BASE_URL = "http://localhost:8000"

def run_tests():
    print("Testing backend endpoints...")
    
    # 1. Health check
    res = requests.get(f"{BASE_URL}/health")
    print(f"Health: {res.status_code} - {res.json()}")

    # 2. Signup
    signup_data = {"email": "test@example.com", "password": "password123"}
    res = requests.post(f"{BASE_URL}/api/auth/signup", json=signup_data)
    print(f"Signup: {res.status_code} - {res.json()}")

    # 3. Login
    login_data = {"email": "test@example.com", "password": "password123"}
    res = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Login: {res.status_code}")
    
    if res.status_code != 200:
        print("Login failed, aborting")
        return
        
    token = res.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Upload PDF
    pdf_path = "C:\\Users\\vishw\\Downloads\\GENQ\\backend\\temp_uploads\\sample_genetic_report.pdf"
    with open(pdf_path, "rb") as f:
        files = {"file": ("sample_genetic_report.pdf", f, "application/pdf")}
        data = {"consent_given": "true"}
        print("Uploading PDF...")
        res = requests.post(f"{BASE_URL}/api/upload-report", headers=headers, files=files, data=data)
        print(f"Upload: {res.status_code}")
        if res.status_code == 200:
            print(res.json())
        else:
            print(res.text)

if __name__ == "__main__":
    run_tests()
