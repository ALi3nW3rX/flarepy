import argparse
import requests
import json
import os

# Hard-coded credentials
api_key = "your api key here"               # Replace with your actual API key
tenant_id = 123456                          # Ensure this is an integer, do not use quotes

def print_header():
    header = """
    
    Author: ALi3nW3rX
    ███████╗██╗      █████╗ ██████╗ ███████╗██████╗ ██╗   ██╗
    ██╔════╝██║     ██╔══██╗██╔══██╗██╔════╝██╔══██╗╚██╗ ██╔╝
    █████╗  ██║     ███████║██████╔╝█████╗  ██████╔╝ ╚████╔╝ 
    ██╔══╝  ██║     ██╔══██║██╔══██╗██╔══╝  ██╔═══╝   ╚██╔╝  
    ██║     ███████╗██║  ██║██║  ██║███████╗██║        ██║   
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝        ╚═╝   
                                                             
                            
    """                                             
    
    print(header)


def get_token(api_key, tenant_id):
    url = "https://api.flare.io/tokens/generate"
    headers = {"Content-Type": "application/json"}
    payload = {"tenant_id": tenant_id}
    response = requests.post(url, auth=("", api_key), headers=headers, json=payload)
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("token")
    else:
        print("Failed to retrieve token.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return None

def get_domain_data(domain, token):
    url = f"https://api.flare.io/leaksdb/identities/by_domain/{domain}?size=10000&from=0"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve domain data")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return None

def extract_name_and_hash(data):
    extracted_data = []
    seen_hashes = set()
    if isinstance(data, list):
        for entry in data:
            if 'passwords' in entry:
                for item in entry['passwords']:
                    name = entry.get('name')
                    hash_value = item.get('hash')
                    if hash_value and hash_value not in seen_hashes and len(hash_value) <= 24:
                        extracted_data.append({'name': name, 'hash': hash_value})
                        seen_hashes.add(hash_value)
    elif 'passwords' in data:
        for item in data['passwords']:
            name = data.get('name')
            hash_value = item.get('hash')
            if hash_value and hash_value not in seen_hashes and len(hash_value) <= 24:
                extracted_data.append({'name': name, 'hash': hash_value})
                seen_hashes.add(hash_value)
    else:
        print("The JSON structure is not recognized.")
    return extracted_data

def main():
    print_header()
    parser = argparse.ArgumentParser(description="Fetch and store domain data.")
    parser.add_argument("-d", required=True, help="Domain name to query")
    args = parser.parse_args()

    token = get_token(api_key, tenant_id)
    if token is None:
        print("Unable to fetch token, exiting.")
        return
    domain_data = get_domain_data(args.d, token)
    if domain_data is None:
        print("Unable to fetch domain data, exiting.")
        return
    
    extracted_data = extract_name_and_hash(domain_data)

    for item in extracted_data:
        print(f"{item['name']} : {item['hash']}")

if __name__ == "__main__":
    main()
