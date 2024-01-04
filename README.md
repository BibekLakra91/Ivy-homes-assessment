## Ivy-homes-assessment
# Problem-A

```markdown
# IMDb Movie Scraper

This script is a web scraper that fetches information about top movies from IMDb and stores it in a SQLite database. It also provides an API endpoint `/scrape` to trigger the scraping process and returns the scraped data in JSON format.

## Prerequisites

Make sure you have the following installed:

- Python
- Flask
- BeautifulSoup
- requests

You can install the required Python packages using the following command:

```bash
pip install Flask beautifulsoup4 requests
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/IMDb-Movie-Scraper.git
cd IMDb-Movie-Scraper
```

2. Run the script:

```bash
python script_name.py
```

Replace `script_name.py` with the actual name of your Python script.

3. Access the API endpoint:

Open your web browser or use a tool like curl or Postman to access the `/scrape` endpoint:

`http://localhost:5000/scrape`


This will trigger the scraping process, update the SQLite database, and export the data to a CSV file.

## Structure

- `script_name.py`: The main Python script containing the web scraper and Flask web API.
- `movies.db`: SQLite database file to store movie data.
- `movies_data.csv`: CSV file where scraped data is exported.

## Disclaimer

This script is for educational purposes only. Use it responsibly and in accordance with IMDb's terms of service.

Feel free to modify and customize the script based on your needs.

The challenge faced: I misunderstood the problem statement, and because of time constraints, my solution significantly deviated from the specified requirements
Make sure to replace `script_name.py` with the actual name of your Python script. You can add more sections or details to the README file based on your specific requirements.

##Author: Bibek Lakra
