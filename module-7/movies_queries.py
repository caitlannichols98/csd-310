import sqlite3

# Connect to SQLite database (replace 'your_database.db' with your actual database file)
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

# Drop tables if they exist (for demonstration purposes)
cursor.execute("DROP TABLE IF EXISTS film")
cursor.execute("DROP TABLE IF EXISTS studio")
cursor.execute("DROP TABLE IF EXISTS genre")

# Create the studio table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS studio (
        studio_id INTEGER PRIMARY KEY AUTOINCREMENT,
        studio_name TEXT NOT NULL
    )
""")

# Create the genre table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS genre (
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre_name TEXT NOT NULL
    )
""")

# Create the film table with foreign keys
cursor.execute("""
    CREATE TABLE IF NOT EXISTS film (
        film_id INTEGER PRIMARY KEY AUTOINCREMENT,
        film_name TEXT NOT NULL,
        film_releaseDate TEXT NOT NULL,
        film_runtime INTEGER NOT NULL,
        film_director TEXT NOT NULL,
        studio_id INTEGER,
        genre_id INTEGER,
        FOREIGN KEY (studio_id) REFERENCES studio(studio_id),
        FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
    )
""")

# Insert sample data into studio table
cursor.execute("INSERT INTO studio (studio_name) VALUES ('20th Century Fox')")
cursor.execute("INSERT INTO studio (studio_name) VALUES ('Blumhouse Productions')")
cursor.execute("INSERT INTO studio (studio_name) VALUES ('Universal Pictures')")

# Insert sample data into genre table
cursor.execute("INSERT INTO genre (genre_name) VALUES ('Horror')")
cursor.execute("INSERT INTO genre (genre_name) VALUES ('SciFi')")
cursor.execute("INSERT INTO genre (genre_name) VALUES ('Drama')")

# Insert sample data into film table
cursor.execute("""
    INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
    VALUES ('Gladiator', '2000', 155, 'Ridley Scott', 3, 3)
""")
cursor.execute("""
    INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
    VALUES ('Alien', '1979', 117, 'Ridley Scott', 1, 2)
""")
cursor.execute("""
    INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
    VALUES ('Get Out', '2017', 104, 'Jordan Peele', 2, 1)
""")

conn.commit()

# Query 1: Select all fields from the studio table
print("DISPLAYING STUDIO RECORDS")
cursor.execute("SELECT * FROM studio")
studios = cursor.fetchall()

# Print query 1 results
for studio in studios:
    print("Studio ID: {}, Studio Name: {}".format(studio[0], studio[1]))
print()

# Query 2
print("DISPLAYING GENRE RECORDS")
cursor.execute("SELECT * FROM genre")
genres = cursor.fetchall()

for genre in genres:
    print("Genre ID: {}, Genre Name: {}".format(genre[0], genre[1]))
print()

# Query 3
print("DISPLAYING MOVIES SHORTER THAN TWO HOURS with minutes displayed")
cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
short_movies = cursor.fetchall()

# Print query 3 results
for movie in short_movies:
    print("Movie Name: {}, Runtime: {} minutes".format(movie[0], movie[1]))
print()

# Query 4: Get a list of film names, directors, and runtimes grouped by director
print("DISPLAYING FILM NAMES and DIRECTORS by order")
cursor.execute("SELECT film_name, film_director, film_runtime FROM film ORDER BY film_director")
films_by_director = cursor.fetchall()

# Print query 4 results
current_director = None
for film in films_by_director:
    if film[1] != current_director:
        current_director = film[1]
        print("\nDirector: {}".format(current_director))
    print("Film Name: {}".format(film[0], film[2]))

# Close cursor and connection
cursor.close()
conn.close()
