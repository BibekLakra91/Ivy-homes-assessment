import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import sqlite3
from flask import g
import csv

app = Flask(__name__)

DATABASE = 'movies.db'

# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to create or update the database schema
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Drop the existing 'movies' table if it exists
        cursor.execute('DROP TABLE IF EXISTS movies')

        # Create a new 'movies' table with the updated schema
        cursor.execute('''
            CREATE TABLE movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT,
                comment TEXT,
                rating TEXT,
                date TEXT
            )
        ''')
        db.commit()

# Function to clear all records from the 'movies' table
def clear_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM movies')
        db.commit()

# Export data to CSV with 4 columns: movie_name, rating, comment, and date
def export_to_csv(data):
    csv_file_path = 'movies_data.csv'

    # Delete the previous CSV file if it exists
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['movie_name', 'comment', 'rating', 'date'])  # Write header

        for movie in data:
            title = movie['title']
            for review in movie['reviewList']:
                comment, raw_rating, date = review

                # Handle the rating format (e.g., "10/10" to "10-oct")
                rating = raw_rating.replace('-oct', '/10')

                csv_writer.writerow([title, comment, rating, date])

    print(f'Data exported to CSV: {csv_file_path}')

# Function to get reviews
def get_reviews(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        user_review = []
        user_rating = []
        user_date = []

        for element in soup.select('.text.show-more__control')[:10]:
            review = element.get_text(strip=True)
            user_review.append(review)

        for element in soup.select('.rating-other-user-rating')[:10]:
            rating = element.get_text(strip=True)
            user_rating.append(rating)

        for element in soup.select('.review-date')[:10]:
            date = element.get_text(strip=True)
            user_date.append(date)

        return list(zip(user_review, user_rating, user_date))
    except requests.RequestException as error:
        print(f'Error fetching reviews: {error}')
        raise

# Initialize the database
init_db()

# Modify the 'scrape' function to handle merging rows and creating columns
@app.route('/scrape')
def scrape():
    # Initialize or update the database schema
    init_db()

    base_url = "https://www.imdb.com/"
    movieTitle = "chart/top/?ref_=nv_mv_250"
    review = "reviews/?sort=submissionDate&dir=desc&ratingFilter=0"

    try:
        # Clear existing data from the database
        clear_db()

        response1 = requests.get(base_url + movieTitle, headers=headers)
        response1.raise_for_status()
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        top_movies = []

        for element1 in soup1.select('.ipc-title-link-wrapper')[:20]:
            title = element1.get_text(strip=True)
            link = element1['href'].split('?')
            url = base_url + link[0] + review

            try:
                user_reviews = get_reviews(url)

                # Insert movie data into the database
                with app.app_context():
                    db = get_db()
                    cursor = db.cursor()
                    for review_data in user_reviews:
                        cursor.execute(
                            'INSERT INTO movies (movie_name, comment, rating, date) VALUES (?, ?, ?, ?)',
                            (title, *review_data))
                    db.commit()

                top_movies.append({"title": title, "reviewList": user_reviews})

            except Exception as error2:
                print(f'Error processing movie: {error2}')

        # Export data to CSV after scraping
        export_to_csv(top_movies)

        return jsonify(top_movies)

    except requests.RequestException as error1:
        print(f'Error fetching top movies: {error1}')
        return f'Error fetching top movies: {error1}', 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
