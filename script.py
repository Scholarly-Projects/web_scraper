import requests
from bs4 import BeautifulSoup
import csv

# URL of the faculty directory
url = 'https://www.uidaho.edu/cals/aelc'

# Send a request to fetch the HTML content of the page
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the section containing the faculty information
# Note: You need to inspect the HTML structure of the directory page and adjust the selectors accordingly
faculty_list = soup.find_all('div', class_='faculty-list-item')

# Open a CSV file to write the data
with open('faculty_contacts.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Email', 'Title'])  # Header row

    # Loop through the faculty list and extract information
    for faculty in faculty_list:
        name = faculty.find('h3').text.strip()
        email = faculty.find('a', href=lambda href: href and "mailto:" in href)['href'].replace('mailto:', '').strip()
        title = faculty.find('p', class_='faculty-title').text.strip()
        
        # Write the data to the CSV file
        writer.writerow([name, email, title])
        
print('Data scraping and writing to CSV completed.')
