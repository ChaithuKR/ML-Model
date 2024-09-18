import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load Excel file
file_path = 'websites.xlsx'  # Replace with the path to your Excel file
df = pd.read_excel(file_path)

# Function to ensure URL starts with "https://"
def ensure_https(url):
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

# Function to extract website name from <title> tag
def get_website_name(url):
    try:
        # Ensure the URL has the proper schema
        url = ensure_https(url)

        # Fetch the webpage content
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract and return the website's <title> tag content
        website_name = soup.title.string.strip() if soup.title else 'Unknown'
        return website_name
    except requests.exceptions.RequestException as e:
        # Handle connection errors or invalid URLs
        return f"Error: {str(e)}"

# Initialize an empty list to store website names
website_names = []

# Loop over each URL in the Excel file and extract website name
for url in df['Website URL']:
    website_name = get_website_name(url)
    website_names.append(website_name)

# Add the website names to a new column in the DataFrame
df['Website Name'] = website_names

# Save the updated DataFrame back to the Excel file
df.to_excel('updated_websites.xlsx', index=False)

print("Website names added and Excel file updated successfully!")
