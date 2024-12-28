import requests

# Replace with your actual IP address and port
base_url = "http://127.0.0.1:8000"

# Step 1: Obtain a JWT Token
def get_token():
    response = requests.post(f"{base_url}/token", data={"username": "test", "password": "test"})
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Failed to obtain token")
        return None

# Step 2: Create a New Task
def create_task(token):
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        task_data = {
            "title": "New Task",
            "description": "This is a new task",
            "completed": False
        }
        response = requests.post(f"{base_url}/tasks/", json=task_data, headers=headers)
        if response.status_code == 200:
            print("Task Created:", response.json())
        else:
            print("Failed to create task")
    else:
        print("No valid token available")

# Step 3: Access a Protected Endpoint
def access_protected_endpoint(token):
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/tasks/", headers=headers)
        if response.status_code == 200:
            print("Protected Data:", response.json())
        else:
            print("Failed to access protected endpoint")
    else:
        print("No valid token available")

# Main function to run the script
if __name__ == "__main__":
    token = get_token()
    create_task(token)
    access_protected_endpoint(token)
