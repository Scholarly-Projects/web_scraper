import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the faculty directory
base_url = 'https://www.uidaho.edu/cals/people/'

# Send a request to fetch the HTML content of the main directory page
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the links to individual faculty profile pages
profile_links = soup.find_all('a', href=True, class_='faculty-list-item-link')

# Open a CSV file to write the data
with open('faculty_contacts.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Office', 'Phone', 'Email', 'Mailing Address'])  # Header row

    # Loop through the profile links and extract information
    for link in profile_links:
        profile_url = base_url + link['href']
        
        # Send a request to fetch the HTML content of the profile page
        profile_response = requests.get(profile_url)
        profile_soup = BeautifulSoup(profile_response.content, 'html.parser')
        
        # Extract the faculty information
        name = profile_soup.find('h2', class_='profile-heading').text.strip()
        title = profile_soup.find('h3').text.strip()
        office = profile_soup.find('div', text='Office').find_next_sibling('div').text.strip()
        phone = profile_soup.find('div', text='Phone').find_next_sibling('div').text.strip()
        email = profile_soup.find('div', text='Email').find_next_sibling('div').text.strip()
        mailing_address = profile_soup.find('div', text='Mailing Address').find_next_sibling('div').text.strip()
        
        # Write the data to the CSV file
        writer.writerow([name, title, office, phone, email, mailing_address])

print('Data scraping and writing to CSV completed.')
