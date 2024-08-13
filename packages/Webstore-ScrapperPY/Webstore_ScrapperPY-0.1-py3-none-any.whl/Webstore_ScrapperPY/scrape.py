import requests

def fetch_data(query):
    response = requests.get(f'https://webstore-scrapper.onrender.com/search?query={query}')
    if response.status_code == 200:
        # Save the CSV content to a file
        with open('output.csv', 'wb') as f:
            f.write(response.content)
        print("Data saved to output.csv")
    else:
        print("Failed to retrieve data:", response.status_code)
