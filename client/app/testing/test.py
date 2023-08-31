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
    
            
    def test_create_existing_movie(self):
        # Try creating the same movie again
        movie = {
            "Name": "The Godfather",
            "Year": 1972,
            "Runtime": 175,
            "Rating": 9.2,
            "Votes": 1667868,
            "Revenue": 134.97
        }
        with self.assertRaises(Exception) as context:
            main.create_movie(self.token, movie)
        error_message = str(context.exception)
        self.assertTrue("Movie already exist" in error_message or "400 Client Error: Bad Request" in error_message,
                        "Expected movie creation to fail.")
                 
    
    def test_create_and_delete_movie(self):
        # Use token to create a new movie
        movie = {
            "Name": "Test Movie for Deletion",
            "Year": 2000,
            "Runtime": 100,
            "Rating": 5.0,
            "Votes": 10,
            "Revenue": 100.0
        }
        response = main.create_movie(self.token, movie)
        
        # Assert that the movie creation was successful
        self.assertEqual(response["Name"], movie["Name"], "Failed to create movie.")

        # Use the ID from the response to delete the movie
        movie_id = response["MovieID"]
        deleted_movie = main.delete_movie(self.token, movie_id)

        # Assert that the movie was successfully deleted
        self.assertEqual(deleted_movie["Name"], movie["Name"], "Failed to delete movie.")
       
              
    def test_get_specific_movie(self):
        # Use token to get a specific movie by its ID
        movie_id = 1
        movie = main.get_movie_by_id(self.token, movie_id)
        
        # Assert that we got a movie
        self.assertIsNotNone(movie, f"Failed to retrieve movie with ID: {movie_id}.")
       
        
    def test_get_invalid_movie(self):
        # Try getting a movie with an invalid ID
        movie_id = 9999  # Assuming no movie with this ID exists
        with self.assertRaises(Exception) as context:
            main.get_movie_by_id(self.token, movie_id)
        self.assertIn("404 Client Error: Not Found for url", str(context.exception), f"Expected movie with ID: {movie_id} to not exist.")
      
        
if __name__ == "__main__":
    unittest.main()
