import sqlite3

# Open and read the file
with open("stephen king adaptations.txt", "r", encoding='utf-8') as file:
    stephen_king_adaptations_list = file.readlines()

# Remove trailing newline characters from each line
stephen_king_adaptations_list = [line.strip() for line in stephen_king_adaptations_list]

# Establish a connection with an SQLite database
conn = sqlite3.connect("stephen_king_adaptations.db")

# Create a table
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                    movieID Varchar(10) PRIMARY KEY ,
                    movieName TEXT,
                    movieYear INTEGER,
                    imdbRating REAL
                )''')
conn.commit()

# Define a function to insert data
def insert_data(movieID, movieName, movieYear, imdbRating):
    try:
        cursor.execute(
            "INSERT INTO stephen_king_adaptations_table (movieID,movieName, movieYear, imdbRating) VALUES (?,?, ?, ?)",
            (movieID, movieName, movieYear, imdbRating))
    except Exception as e:
        # Ignore exceptions for primary key conflicts since data might have been inserted previously
        pass
    conn.commit()

# Insert data from the file into the database
for line in stephen_king_adaptations_list:
    parts = line.split(',')

    if len(parts) == 4:
        movieID, movieName, movieYear, imdbRating = parts
        insert_data(movieID.strip(), movieName.strip(), int(movieYear.strip()), float(imdbRating.strip()))

# User interface
while True:
    print("1. Movie name  ")
    print("2. Movie year  ")
    print("3. Movie rating")
    print("4. STOP")
    choice = input("Enter your choice: ")

    if choice == "1":
        movie_name = input("Please enter the movie name you want to search for: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName like ?", (f"%{movie_name}%",))
        result = cursor.fetchone()
        if result:
            print("Movie name:", result[1])
            print("Movie year:", result[2])
            print("IMDB rating:", result[3])
            print('=' * 30)
        else:
            print("No such movie exists in our database.")

    elif choice == "2":
        movie_year = input("Please enter the year of the movie you want to search: ")
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (movie_year,))
        results = cursor.fetchall()
        if results:
            for result in results:
                print("Movie name:", result[1])
                print("Movie year:", result[2])
                print("IMDB rating:", result[3])
                print('=' * 30)
        else:
            print("No movies were found for that year in our database.")

    elif choice == "3":
        rating = float(input("Please enter the lowest IMDB score to search for: "))
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating,))
        results = cursor.fetchall()
        if results:
            for result in results:
                print("Movie name:", result[1])
                print("Movie year:", result[2])
                print("IMDB rating:", result[3])
                print('=' * 30)
        else:
            print("No movies at or above that rating were found in the database.")

    elif choice == "4":
        break

# Close the database connection
conn.close()
