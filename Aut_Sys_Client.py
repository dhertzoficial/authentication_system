
import requests
import time
import pwinput # This library needs to be installed and the goal is to show the * in the terminal when something is typed

# ANSI CODE FOR COLOR
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

API_URL = 'http://127.0.0.1:5000'
GENERATING_CODE = 'http://127.0.0.1:5001/generate-code'
VERIFICATION_CODE = 'http://127.0.0.1:5001/verify-code'  

def visual_effect(message="Processing", duration=10):
    print(message, end="")
    for _ in range (duration):
        print(".", end="", flush=True)
        time.sleep(0.1)
    print("")

def generate_code(email):
    url = GENERATING_CODE
    data = {"email": email}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # raise an error if the status code is not 200
        print(f"\nVerification code sent to {email}.")
    except requests.exceptions.HTTPError as http_err:
        print(f"\n{RED}Error HTTP in generating code: {http_err}{RESET}")
        print(f"\nServer response: {response.text}")
    except Exception as err:
        print(f"\n{RED}Error in generating code: {err}{RESET}")

# function to verify the verification code
def verify_code(email, code):
    url = VERIFICATION_CODE
    data = {"email": email, "code": code}
    visual_effect("\nVerificando código!")
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # raise an error if the status code is not 200
        print(f"\n{GREEN}Verification code is valid!{RESET}")
        visual_effect("\nEfetuando Login!")
        print("\nLOGIN EFETUADO COM SUCESSO\n")
        
    except requests.exceptions.HTTPError as http_err:
        visual_effect("\nCapturando detalhes do erro do server")
        print(f"\n{RED}Error during code verification:{RESET}")
        print(f"\nserver response: {response.text}")
    except Exception as err:
        visual_effect("\nCapturando detalhes do erro do server")
        print(f"\n{RED}Code verification error: {err}{RESET}")


while True:
    print("\n\nWELCOME TO AUTHENTICATION APP!")
    print("-"*70)
    
    email = input("\nDigite o email: ")
    prompt = ("Digite seu password: ")
    password = pwinput.pwinput(prompt, mask='*')
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
            break

        except ValueError:
            print("Response content is not valid JSON")
    elif response.status_code == 401:
        print(f"{RED}Authentication failed: {RESET}", response.json().get('message', 'Invalid email or password'))
    else:
        print(f"{RED}Request failed: {response.status_code} {response.reason}{RESET}")
        try:
            print(response.json())
        except ValueError:
            print("Response content is not valid JSON")
