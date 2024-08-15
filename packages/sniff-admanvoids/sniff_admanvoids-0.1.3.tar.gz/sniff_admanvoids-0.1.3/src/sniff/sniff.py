import requests
from bs4 import BeautifulSoup
import click
import socket
import whois
import ssl
import subprocess
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def fetch_ssl_info(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert(True)
                cert = x509.load_der_x509_certificate(cert, default_backend())
                issuer = cert.issuer.rfc4514_string()
                subject = cert.subject.rfc4514_string()
                expiration_date = cert.not_valid_after_utc
                return issuer, subject, expiration_date
    except Exception as e:
        return None, None, None

def detect_security_headers(headers):
    security_headers = [
        'Content-Security-Policy', 'X-Content-Type-Options',
        'X-Frame-Options', 'Strict-Transport-Security'
    ]
    detected_headers = {header: headers.get(header, 'Not found') for header in security_headers}
    return detected_headers

def perform_nslookup(domain):
    try:
        result = subprocess.run(["nslookup", domain], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"nslookup failed: {str(e)}"

def perform_dig(domain, record_type="A"):
    try:
        result = subprocess.run(["dig", domain, record_type], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"dig failed: {str(e)}"

def enumerate_subdomains(domain):
    common_subdomains = ['www', 'mail', 'ftp', 'blog', 'dev', 'test']
    subdomains = []
    for sub in common_subdomains:
        try:
            subdomain = f"{sub}.{domain}"
            socket.gethostbyname(subdomain)
            subdomains.append(subdomain)
        except socket.gaierror:
            continue
    return subdomains

def scan_ports(domain):
    common_ports = [21, 22, 25, 80, 443, 8080]
    open_ports = []
    for port in common_ports:
        try:
            with socket.create_connection((domain, port), timeout=1):
                open_ports.append(port)
        except (socket.timeout, ConnectionRefusedError):
            continue
    return open_ports

def check_directory_listing(url):
    directories = ['/admin/', '/login/', '/backup/', '/test/']
    open_directories = []
    for directory in directories:
        try:
            dir_url = url + directory
            response = requests.get(dir_url)
            if response.status_code == 200 and 'Index of' in response.text:
                open_directories.append(dir_url)
        except requests.RequestException:
            continue
    return open_directories

def detect_technology_stack(headers):
    tech_stack = []
    if 'X-Powered-By' in headers:
        tech_stack.append(headers['X-Powered-By'])
    if 'Server' in headers:
        tech_stack.append(headers['Server'])
    return tech_stack

def extract_external_links(soup, domain):
    external_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http') and domain not in href:
            external_links.append(href)
    return external_links

def fetch_website_info(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        domain = url.split("//")[-1].split("/")[0]
        ip_address = socket.gethostbyname(domain)

        response = requests.get(url, timeout=10)
        response_time = response.elapsed.total_seconds()
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else 'No title found'
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'] if description_tag else 'No description found'
                
        whois_info = whois.whois(domain)
        registrar = whois_info.registrar
        creation_date = whois_info.creation_date
        expiration_date = whois_info.expiration_date

        ssl_issuer, ssl_subject, ssl_expiration_date = fetch_ssl_info(domain)
        
        http_headers = response.headers
        security_headers = detect_security_headers(http_headers)

        # Adding new features
        subdomains = enumerate_subdomains(domain)
        open_ports = scan_ports(domain)
        open_directories = check_directory_listing(url)
        tech_stack = detect_technology_stack(http_headers)
        external_links = extract_external_links(soup, domain)

        nslookup_result = perform_nslookup(domain)
        dig_result = perform_dig(domain)

        result = {
            "Website URL": url,
            "IP Address": ip_address,
            "Response Time": f"{response_time} seconds",
            "Title": title,
            "Description": description,
            "Registrar": registrar,
            "Creation Date": creation_date.isoformat() if isinstance(creation_date, datetime) else str(creation_date),
            "Expiration Date": expiration_date.isoformat() if isinstance(expiration_date, datetime) else str(expiration_date),
            "SSL Issuer": ssl_issuer,
            "SSL Subject": ssl_subject,
            "SSL Expiration Date": ssl_expiration_date.isoformat() if isinstance(ssl_expiration_date, datetime) else str(ssl_expiration_date),
            "Security Headers": security_headers,
            "HTTP Headers": dict(http_headers),
            "Subdomains": subdomains,
            "Open Ports": open_ports,
            "Open Directories": open_directories,
            "Technology Stack": tech_stack,
            "External Links": external_links,
            "nslookup Result": nslookup_result,
            "dig Result": dig_result
        }

        return result
    
    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
    except socket.gaierror:
        print(f"Error resolving the domain: {domain}")
    except whois.parser.PywhoisError:
        print(f"Error fetching WHOIS information for: {domain}")
    except Exception as e:
        print(f"An error occurred: {e}")

@click.command()
@click.argument('url')
@click.option('--output', type=click.Choice(['json', 'csv', 'html']), help='Output format')
def main(url, output):
    result = fetch_website_info(url)

    if result:
        if output == 'json':
            import json
            with open('result.json', 'w') as f:
                json.dump(result, f, indent=4)
        elif output == 'csv':
            import csv
            with open('result.csv', 'w') as f:
                writer = csv.writer(f)
                for key, value in result.items():
                    writer.writerow([key, value])
        elif output == 'html':
            with open('result.html', 'w') as f:
                f.write('<html><body><h1>Website Scan Results</h1><table border="1">')
                for key, value in result.items():
                    f.write(f'<tr><th>{key}</th><td>{value}</td></tr>')
                f.write('</table></body></html>')
        else:
            print("\nWebsite Information:")
            print(f"Website URL: {result['Website URL']}")
            print(f"IP Address: {result['IP Address']}")
            print(f"Response Time: {result['Response Time']}")
            print(f"Title: {result['Title']}")
            print(f"Description: {result['Description']}\n")
            
            print("WHOIS Information:")
            print(f"Registrar: {result['Registrar']}")
            print(f"Creation Date: {result['Creation Date']}")
            print(f"Expiration Date: {result['Expiration Date']}\n")
            
            print("SSL Information:")
            print(f"SSL Issuer: {result['SSL Issuer']}")
            print(f"SSL Subject: {result['SSL Subject']}")
            print(f"SSL Expiration Date: {result['SSL Expiration Date']}\n")
            
            print("Security Headers:")
            for header, value in result['Security Headers'].items():
                print(f"  {header}: {value}")
            print("\nHTTP Headers:")
            for key, value in result['HTTP Headers'].items():
                print(f"  {key}: {value}")
            
            print("\nAdditional Information:")
            print(f"Subdomains: {', '.join(result['Subdomains']) if result['Subdomains'] else 'None found'}")
            print(f"Open Ports: {', '.join(map(str, result['Open Ports'])) if result['Open Ports'] else 'None found'}")
            print(f"Open Directories: {', '.join(result['Open Directories']) if result['Open Directories'] else 'None found'}")
            print(f"Technology Stack: {', '.join(result['Technology Stack']) if result['Technology Stack'] else 'None detected'}")
            print(f"External Links: {', '.join(result['External Links']) if result['External Links'] else 'None found'}")
            
            print("\nDNS Information:")
            print(f"nslookup Result:\n{result['nslookup Result']}")
            print(f"\ndig Result:\n{result['dig Result']}")

if __name__ == "__main__":
    main()