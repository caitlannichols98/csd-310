import mysql.connector

# Database connection configuration
config = {
    "user": "root",
    "password": "Classroomhalfway06!",
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}

# Function to display films with specified fields
def show_films(cursor, title):
    query = """
        SELECT film_name as 'Film Name', film_director as 'Director',
               genre_name as 'Genre', studio_name as 'Studio Name'
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
        WHERE film_name = %s
    """
    
    cursor.execute(query, (title,))
    films = cursor.fetchall()
    
    print(f"\n-- {title} --")
    for film in films:
        print(f"Film Name: {film['Film Name']}")
        print(f"Director: {film['Director']}")
        print(f"Genre: {film['Genre']}")
        print(f"Studio Name: {film['Studio Name']}")
        print()

# Function to display films with selected fields
def display_films(cursor, output_label):
    query = """
        SELECT film_name as 'Film Name', film_director as 'Director',
               genre_name as 'Genre', studio_name as 'Studio Name'
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """
    
    cursor.execute(query)
    films = cursor.fetchall()
    
    print(f"\n-- {output_label} --")
    for film in films:
        print(f"Film Name: {film['Film Name']}")
        print(f"Director: {film['Director']}")
        print(f"Genre: {film['Genre']}")
        print(f"Studio Name: {film['Studio Name']}")
        print()

try:
    # Connect to the database
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)  # Cursor returns rows as dictionaries
    
    # Task 1: Display films before any modifications
    display_films(cursor, "DISPLAYING FILMS")
    
    # Task 2: Insert a new record into the film table
    insert_query = """
        INSERT INTO film(film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) 
        VALUES('Star Wars', '1977', '121', 'George Lucas', 
               (SELECT studio_id FROM studio WHERE studio_name = '20th Century Fox'),
               (SELECT genre_id FROM genre WHERE genre_name = 'SciFi'))
    """
    cursor.execute(insert_query)
    connection.commit()
    print("Inserted a new film record.")
    
    # Task 3: Display films after insertion
    display_films(cursor, "DISPLAYING FILMS AFTER INSERT")
    
    # Task 4: Update the film 'Alien' to be a Horror film
    update_query = """
        UPDATE film
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
        WHERE film_name = 'Alien'
    """
    cursor.execute(update_query)
    connection.commit()
    print("Changed 'Alien' genre to Horror.")
    
    # Task 5: Display films after update
    display_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")
    
    # Task 6: Delete the movie 'Gladiator'
    delete_query = """
        DELETE FROM film
        WHERE film_name = 'Gladiator'
    """
    cursor.execute(delete_query)
    connection.commit()
    print("Deleted 'Gladiator'.")
    
    # Task 7: Display films after deletion
    display_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Clean up
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
