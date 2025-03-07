import os
import requests
import bs4

def extract_docs():
    '''Extracts handbooks, annual reports, and media guides from the ICC website.'''

    os.makedirs(os.path.join("data", "icc"), exist_ok=True)
    BASE_URL = "https://www.icc-cricket.com/about/the-icc/publications/"
    list_of_docs = ['playing-handbook', 'annual-report', 'media-guide']

    for doc in list_of_docs:
        NEW_URL = BASE_URL + doc
        try:
            response = requests.get(NEW_URL, timeout=10)
            response.raise_for_status()  # Raise an error for bad status codes (e.g., 404, 500)
            soup = bs4.BeautifulSoup(response.text, 'html.parser')

            pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

            for i, pdf_url in enumerate(pdf_links, start=1):
                try:
                    print(f"Downloading: {pdf_url}")
                    pdf_response = requests.get(pdf_url, stream=True, timeout=10)
                    pdf_response.raise_for_status()

                    pdf_path = os.path.join("data", "icc", f"{doc}_{i}.pdf")
                    with open(pdf_path, "wb") as file:
                        for chunk in pdf_response.iter_content(chunk_size=1024):
                            file.write(chunk)
                    print(f"Saved: {pdf_path}")

                except requests.exceptions.RequestException as e:
                    print(f"Failed to download: {pdf_url} | Error: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {NEW_URL} | Error: {e}")

    return "Documents have been downloaded successfully."

def extract_rules():
    '''Extracts rules and regulations from the ICC website.'''

    BASE_URL = "https://www.icc-cricket.com/about/cricket/rules-and-regulations/"
    list_of_docs = ['playing-conditions', 'decision-review-system', 'duckworth-lewis-stern', 'illegal-bowling-actions', 'code-of-conduct']

    os.makedirs(os.path.join("data", "icc"), exist_ok=True)

    for doc in list_of_docs:
        NEW_URL = BASE_URL + doc
        try:
            response = requests.get(NEW_URL, timeout=10)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, 'html.parser')

            pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

            for i, pdf_url in enumerate(pdf_links, start=1):
                try:
                    print(f"Downloading: {pdf_url}")
                    pdf_response = requests.get(pdf_url, stream=True, timeout=10)
                    pdf_response.raise_for_status()

                    pdf_path = os.path.join("data", "icc", f"{doc}_{i}.pdf")
                    with open(pdf_path, "wb") as file:
                        for chunk in pdf_response.iter_content(chunk_size=1024):
                            file.write(chunk)
                    print(f"Saved: {pdf_path}")

                except requests.exceptions.RequestException as e:
                    print(f"Failed to download: {pdf_url} | Error: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {NEW_URL} | Error: {e}")

    return "Documents have been downloaded successfully."

def extract_mcc_rules():
    '''Function to extract rules from lords website'''

    BASE_URL = 'https://www.lords.org/mcc/the-laws-of-cricket/'
    response = requests.get(BASE_URL)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    list_of_laws = soup.find(class_='listOfLaws__canvasContent')
    links = [a['href'] for a in list_of_laws.find_all('a', href=True)]
    dir_path = 'data/mcc_rules/'
    os.makedirs(dir_path, exist_ok=True)

    for link in links:
        URL = 'https://www.lords.org' + link
        soup = bs4.BeautifulSoup(requests.get(URL).text, 'html.parser')
        content = soup.find('div', class_='tabccordion__law-content')
        
        file_path = dir_path + link.split('/')[-1] + '.txt'
        print(file_path)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content.text)
    return "MCC rules have been downloaded successfully."


if __name__ == "__main__":
    # extract_docs()
    # extract_rules()
    extract_mcc_rules()
