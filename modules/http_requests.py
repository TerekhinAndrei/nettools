from bs4 import BeautifulSoup
import requests


def append_record_to_file(ip, title, filename='titles.txt'):
    try:
        with open(filename, 'a') as file:
            file.write(f'{ip}:{title}\n')
        print(f'{ip}:{title} appended to {filename}')
    except IOError as e:
        print(f'Error opening or writing to file: {e}')

def get(url):
    try:
        # Send a GET request to the server
        response = requests.get('http://'+url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Process the response content
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text()
                append_record_to_file(url, title_tag, 'titles.txt')
            else:
                print('No title tag found')
            return response
        else:
            print(f'Error: Received response with status code {response.status_code}')
            return None

    except requests.RequestException as e:
        # Handle any errors that occurred during the request
        print(f'An error occurred: {e}')
