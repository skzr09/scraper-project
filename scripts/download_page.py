"""
Download Page
   Downloads a web page from a given URL and saves it as an HTML file.
Usage:
    python -m scripts.download_page
Notes:
    - This is a simple utility to fetch and save web pages for testing the scraper.
    - You can specify the output file name or it will default to 'output.html'.
"""

import os
import requests

def download_page():
    """
    Downloads a web page from user input URL and saves it locally.
    
    Prompts the user to enter a URL, fetches the page content using requests,
    and writes the HTML to a file named by the user or 'output.html' by default.
    """

    url = input("Enter URL to download  : ")
    out = input("Enter file output name (default output.html): ")
    
    # Create data directory if it doesn't exist
    data_dir = "data01"
    os.makedirs(data_dir, exist_ok=True)

    if not out:
        out = "output.html"
    
    out = os.path.join(data_dir, out)
    
    # fetch the page content using requests
    # https://pypi.org/project/requests/

    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print(f"[ERR ] Failed to fetch page. Status code: {response.status_code}")
        return

    # Save HTML
    with open(out, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Page saved as {out}")


if __name__ == "__main__":
    download_page()
