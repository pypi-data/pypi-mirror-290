import json
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfkit

def parse_args():
    parser = argparse.ArgumentParser(description='Dynamic URL loading script.')
    parser.add_argument('url', type=str, help='URL of the page to load')
    return parser.parse_args()

def inject_capture_script(driver):
    # Włączenie logowania żądań i odpowiedzi dla XMLHttpRequest
    driver.execute_script("""
        window.performance_log = window.performance_log || [];
        const originalOpen = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function(method, url) {
            this.addEventListener('load', function() {
                if (url.endsWith('.xhtml')) {
                    window.performance_log.push({
                        url: url,
                        status: this.status,
                        response: this.responseText
                    });
                }
            }, false);
            originalOpen.apply(this, arguments);
        };
    """)
    print("Capture script injected.")

def convert_html_images(html_content, base_url):
    # Użycie BeautifulSoup do parsowania HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Konwersja znaczników <img> na pełne URL
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            full_img_url = urljoin(base_url, src)
            img['src'] = full_img_url

    # Zwrócenie zmodyfikowanego HTML
    return str(soup)

def capture_xhtml_files(driver, results):
    # Zmniejszenie czasu oczekiwania na załadowanie zasobów
    time.sleep(1)

    # Pobieranie zarejestrowanych odpowiedzi
    performance_log = driver.execute_script("return window.performance_log")
    if performance_log is None:
        print("Warning: Performance log is None.")
        return

    new_entries = 0
    for entry in performance_log:
        if not any(result['url'] == entry['url'] for result in results):
            # Konwersja XHTML na HTML z pełnymi URL dla obrazków
            base_url = entry['url']
            html_content = convert_html_images(entry['response'], base_url)
            results.append({
                'url': entry['url'],
                'status': entry['status'],
                'response': html_content
            })
            new_entries += 1
    print(f"Captured {new_entries} new .xhtml files.")

def click_next_and_capture(driver, results, refresh_attempts=2):
    attempts = 0
    while True:
        try:
            # Czekanie na przycisk "Next section" i kliknięcie go
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next Section')]"))
            )
            next_button.click()
            print("Clicked 'Next Section' button.")
            
            # Zmniejszenie czasu oczekiwania na załadowanie następnej strony
            time.sleep(1)

            # Wstrzyknięcie skryptu przechwytywania na nowej stronie
            inject_capture_script(driver)

            # Przechwytywanie plików .xhtml na następnej stronie
            capture_xhtml_files(driver, results)

        except WebDriverException as e:
            error_message = str(e)
            print(f"No more pages or an error occurred: {error_message}")
            if ("target frame detached" in error_message or "stale element not found" in error_message) and attempts < refresh_attempts:
                attempts += 1
                print(f"Attempting to refresh the page ({attempts}/{refresh_attempts}) due to error...")
                driver.refresh()
                time.sleep(5)
            else:
                print("Max refresh attempts reached or another error occurred. Exiting...")
                break

def main():
    args = parse_args()
    url = args.url

    # Ustawienia dla Selenium
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument('--headless')  # Uruchomienie w trybie bezgłowym
    options.add_argument('--disable-gpu')  # Wyłączenie GPU
    options.add_argument('--no-sandbox')  # Wyłączenie piaskownicy
    options.add_argument('--disable-dev-shm-usage')  # Wyłączenie współdzielenia pamięci

    # Inicjalizacja przeglądarki
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Otwórz stronę
    driver.get(url)

    # Zaczekaj, aż strona się załaduje
    driver.implicitly_wait(10)

    # Włączenie Network
    driver.execute_cdp_cmd('Network.enable', {})

    # Lista do przechowywania wyników
    results = []

    # Wstrzyknięcie skryptu przechwytywania na pierwszej stronie
    inject_capture_script(driver)

    # Przechwytywanie plików .xhtml na pierwszej stronie
    capture_xhtml_files(driver, results)

    # Użycie wielowątkowości do równoległego przetwarzania stron
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(click_next_and_capture, driver, results) for _ in range(4)]
        for future in futures:
            future.result()

    # Zamknięcie przeglądarki
    driver.quit()

    # Wyświetlanie wyników
    print(f"Total captured .xhtml files: {len(results)}")
    for result in results:
        print(f"URL: {result['url']}")
        print(f"Status: {result['status']}")
        print(f"Content:\n{result['response'][:200]}")  # Wyświetlanie pierwszych 200 znaków zawartości

    # Zapisywanie wyników do jednego pliku HTML z poprawnym formatowaniem tabel i obrazków
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
    """

    # Dodanie wszystkich zebranych treści
    for result in results:
        html_content += result['response']

    html_content += """
    </body>
    </html>
    """

    # Zapisywanie HTML do pliku tymczasowego
    html_filename = 'results.html'
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Konfiguracja ścieżki do wkhtmltopdf
    pdfkit_config = pdfkit.configuration(wkhtmltopdf='C://Program Files//wkhtmltopdf//bin//wkhtmltopdf.exe')

    # Konwersja HTML na PDF
    pdf_filename = 'results.pdf'
    pdfkit.from_file(html_filename, pdf_filename, configuration=pdfkit_config)

    print(f"PDF saved as {pdf_filename}")

if __name__ == '__main__':
    main()
