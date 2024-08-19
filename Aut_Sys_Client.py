
import requests

API_URL = 'http://127.0.0.1:5000'
GENERATING_CODE = 'http://127.0.0.1:5001/generate-code'
VERIFICATION_CODE = 'http://127.0.0.1:5001/verify-code'  

def generate_code(email):
    url = GENERATING_CODE
    data = {"email": email}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # raise an error if the status code is not 200
        print(f"Verification code sent to {email}.")
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP in generating code: {http_err}")
        print(f"Server response: {response.text}")
    except Exception as err:
        print(f"Error in generating code: {err}")

# function to verify the verification code
def verify_code(email, code):
    url = VERIFICATION_CODE
    data = {"email": email, "code": code}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # raise an error if the status code is not 200
        print("Verification code is valid!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error during code verification: {http_err}")
        print(f"server response: {response.text}")
    except Exception as err:
        print(f"Code verification error: {err}")


email = input("\nDigite o email: ")
password = input("\nDigite o password: ")
print("")

user_data = {
    "email": email,
    "password": password
}

response = requests.post(f'{API_URL}/authenticate', json=user_data)

# Verifique o status da resposta
if response.status_code == 200:
    try:
        data = response.json()
        print(data.get('message', 'No message in response'))
        generate_code(email)
        code = input("\nEnter the code received by email: ")
        verify_code(email,code)
        print("\nLOGIN EFETUADO COM SUCESSO!!!")

    except ValueError:
        print("Response content is not valid JSON")
elif response.status_code == 401:
    print("Authentication failed: ", response.json().get('message', 'Invalid email or password'))
else:
    print(f"Request failed: {response.status_code} {response.reason}")
    try:
        print(response.json())
    except ValueError:
        print("Response content is not valid JSON")
