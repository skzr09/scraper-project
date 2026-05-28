"""
Download Page
   Downloads a web page from a given URL and saves it as an HTML file.
   Usage:
       python download_page.py
"""

import requests

def download_page():
    """
    Downloads a web page from user input URL and saves it locally.
    
    Prompts the user to enter a URL, fetches the page content using requests,
    and writes the HTML to a file named by the user or 'output.html' by default.
    """

    url = input("Enter URL to download  : ")
    out = input("Enter file output name (default output.html): ")

    if not out:
        out = "output.html"
    
    # fetch the page content using requests
    # https://pypi.org/project/requests/

    response = requests.get(url, timeout=10)
    
    # Save HTML
    with open(out, "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print(f"Page saved as {out}")


if __name__ == "__main__":
    download_page()
