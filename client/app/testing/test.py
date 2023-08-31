import unittest
import main 

class TestMockClient(unittest.TestCase):
    
    def setUp(self):
        self.token = main.mock_authenticate()
    
    def test_authenticate(self):
        self.assertIsNotNone(self.token, "Authentication failed, token is None.")
        
    def test_get_movies(self):        
        # Use token to get movies
        movies = main.get_movies(self.token)
        
        # Assert that the response is a list.
        self.assertIsInstance(movies, list, "Expected movies to be a list.")
        
    def test_create_movie(self):
        # Use token to create a new movie
        movie = {
            "Name": "Test Movie",
            "Year": 1999,
            "Runtime": 99,
            "Rating": 4.9,
            "Votes": 9,
            "Revenue": 99.92
        }
        response = main.create_movie(self.token, movie)
        
        # Assert that the movie creation was successful
        self.assertEqual(response["Name"], movie["Name"], "Failed to create movie.")
        
    def test_create_existing_movie(self):
        # Try creating the same movie again
        movie = {
            "Name": "Test Movie",
            "Year": 1999,
            "Runtime": 99,
            "Rating": 4.9,
            "Votes": 9,
            "Revenue": 99.9
        }
        with self.assertRaises(Exception) as context:
            main.create_movie(self.token, movie)
        self.assertIn("Movie already exist", str(context.exception), "Expected movie creation to fail.")
        
    def test_get_specific_movie(self):
        # Use token to get a specific movie by its ID
        movie_id = 1  # Assuming a movie with this ID exists
        movie = main.get_movie_by_id(self.token, movie_id)
        
        # Assert that we got a movie
        self.assertIsNotNone(movie, f"Failed to retrieve movie with ID: {movie_id}.")
        
    def test_get_invalid_movie(self):
        # Try getting a movie with an invalid ID
        movie_id = 9999  # Assuming no movie with this ID exists
        with self.assertRaises(Exception) as context:
            main.get_movie_by_id(self.token, movie_id)
        self.assertIn("could not be found", str(context.exception), f"Expected movie with ID: {movie_id} to not exist.")
        
if __name__ == "__main__":
    unittest.main()
