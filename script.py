import requests
from bs4 import BeautifulSoup
import csv

# List of base URLs to search for profile links
base_urls = [
    'https://www.uidaho.edu/cals/animal-veterinary-and-food-sciences/our-people/',
    'https://www.uidaho.edu/cals/biological-and-agricultural-engineering/our-people/',
    'https://www.uidaho.edu/cals/entomology/our-people/',
    'https://www.uidaho.edu/cals/food-science/our-people/',
    'https://www.uidaho.edu/cals/plant-sciences/our-people/'
]

# Function to fetch profile URLs from a given base page URL
def fetch_profile_urls(base_urls):
    profile_urls = []
    for base_url in base_urls:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links that lead to profile pages
        for link in soup.find_all('a', href=True):
            url = link['href']
            if '/people/' in url or '/faculty/' in url or '/our-people/' in url:
                full_url = 'https://www.uidaho.edu' + url
                profile_urls.append(full_url)
    
    return profile_urls

# Fetch all profile URLs
profile_urls = fetch_profile_urls(base_urls)

# Open a CSV file to write the data
with open('faculty_contacts.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Title', 'Office', 'Phone', 'Email', 'Mailing Address'])  # Header row

    # Loop through the profile URLs and extract information
    for profile_url in profile_urls:
        # Send a request to fetch the HTML content of the profile page
        profile_response = requests.get(profile_url)
        profile_soup = BeautifulSoup(profile_response.content, 'html.parser')
        
        # Extract the faculty information
        name = profile_soup.find('h2', class_='profile-heading').text.strip() if profile_soup.find('h2', class_='profile-heading') else 'N/A'
        title = profile_soup.find('h3').text.strip() if profile_soup.find('h3') else 'N/A'

        def get_bio_info(label):
            label_div = profile_soup.find(string=label)
            if label_div:
                parent_div = label_div.find_parent('div')
                if parent_div and parent_div.find_next_sibling('div'):
                    return parent_div.find_next_sibling('div').text.strip()
            return 'N/A'

        office = get_bio_info('Office')
        phone = get_bio_info('Phone')
        email = get_bio_info('Email')
        mailing_address = get_bio_info('Mailing Address')
        
        # Write the data to the CSV file
        writer.writerow([name, title, office, phone, email, mailing_address])

print('Data scraping and writing to CSV completed.')
