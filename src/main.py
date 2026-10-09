from movie_rating_system import MovieRatingSystem


if __name__ == "__main__":
    movie_system = MovieRatingSystem()

    movie_system.insert("Inception", 9)
    movie_system.insert("The Matrix", 10)
    movie_system.insert("Interstellar", 8)
    movie_system.insert("Joker", 7)
    movie_system.insert("Avengers", 9)

    print(
        "Top Rated Movie:",
        movie_system.get_top_rated()
    )

    print(
        "Movies with Ratings between 8 and 10:",
        movie_system.get_movies_in_range(8, 10)
    )

    movie_system.delete("Joker")

    print(
        "Movies after deleting 'Joker':",
        movie_system.get_movies_in_range(1, 10)
    )