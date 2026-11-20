
import json
from pathlib import Path


DATA_FILE = Path("movies.json")


class Movie:
    def __init__(self, title, genre, rating, year):
        self.title = title
        self.genre = genre
        self.rating = rating
        self.year = year

    def to_dict(self):
        return {
            "title": self.title,
            "genre": self.genre,
            "rating": self.rating,
            "year": self.year
        }


class MovieRecommendationSystem:
    def __init__(self):
        self.movies = []
        self.load_movies()

    def load_movies(self):
        if not DATA_FILE.exists():
            self.movies = [
                Movie("Inception", "Sci-Fi", 8.8, 2010),
                Movie("Interstellar", "Sci-Fi", 8.7, 2014),
                Movie("The Dark Knight", "Action", 9.0, 2008),
                Movie("Titanic", "Romance", 7.9, 1997),
                Movie("Coco", "Animation", 8.4, 2017)
            ]
            self.save_movies()
            return

        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Invalid movie database.")

            loaded_movies = []

            for item in data:
                movie = Movie(
                    title=item["title"],
                    genre=item["genre"],
                    rating=float(item["rating"]),
                    year=int(item["year"])
                )
                self.validate_movie(movie)
                loaded_movies.append(movie)

            self.movies = loaded_movies

        except (OSError, json.JSONDecodeError,
                KeyError, TypeError, ValueError) as error:
            print(f"Could not load movie database: {error}")
            self.movies = []

    @staticmethod
    def validate_movie(movie):
        if not movie.title.strip():
            raise ValueError("Movie title cannot be empty.")

        if not movie.genre.strip():
            raise ValueError("Genre cannot be empty.")

        if not 0 <= movie.rating <= 10:
            raise ValueError("Rating must be between 0 and 10.")

        if not 1888 <= movie.year <= 2100:
            raise ValueError("Invalid release year.")

    def save_movies(self):
        try:
            data = [movie.to_dict() for movie in self.movies]

            with DATA_FILE.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

        except OSError as error:
            print(f"Could not save database: {error}")

    def show_all_movies(self):
        if not self.movies:
            print("No movies available.")
            return

        print("\n===== MOVIE LIST =====")

        for movie in sorted(
            self.movies,
            key=lambda item: item.rating,
            reverse=True
        ):
            print(
                f"{movie.title} | {movie.genre} | "
                f"{movie.rating}/10 | {movie.year}"
            )

    def search_by_genre(self, genre):
        results = [
            movie for movie in self.movies
            if movie.genre.casefold() == genre.casefold()
        ]

        self.display_results(results)

    def search_by_title(self, title):
        results = [
            movie for movie in self.movies
            if title.casefold() in movie.title.casefold()
        ]

        self.display_results(results)

    @staticmethod
    def display_results(results):
        if not results:
            print("No matching movies found.")
            return

        for movie in results:
            print(
                f"{movie.title} - {movie.genre} "
                f"({movie.year}) - {movie.rating}/10"
            )

    def add_movie(self):
        try:
            title = input("Movie title: ").strip()
            genre = input("Genre: ").strip()
            rating = float(input("Rating (0-10): "))
            year = int(input("Release year: "))

            movie = Movie(title, genre, rating, year)
            self.validate_movie(movie)

            if any(
                existing.title.casefold() == title.casefold()
                for existing in self.movies
            ):
                print("This movie already exists.")
                return

            self.movies.append(movie)
            self.save_movies()
            print("Movie added successfully!")

        except ValueError as error:
            print(f"Invalid input: {error}")

    def recommend_movies(self):
        genre = input("Enter your favorite genre: ").strip()

        results = [
            movie for movie in self.movies
            if movie.genre.casefold() == genre.casefold()
            and movie.rating >= 7
        ]

        print("\n===== RECOMMENDED MOVIES =====")
        self.display_results(results)

    def run(self):
        while True:
            print("\n===== MOVIE RECOMMENDATION SYSTEM =====")
            print("1. Show all movies")
            print("2. Search by genre")
            print("3. Search by title")
            print("4. Add a movie")
            print("5. Recommend movies")
            print("6. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.show_all_movies()

            elif choice == "2":
                genre = input("Enter genre: ").strip()
                self.search_by_genre(genre)

            elif choice == "3":
                title = input("Enter movie title: ").strip()
                self.search_by_title(title)

            elif choice == "4":
                self.add_movie()

            elif choice == "5":
                self.recommend_movies()

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    app = MovieRecommendationSystem()
    app.run()
