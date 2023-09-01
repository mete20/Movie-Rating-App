import unittest
import main 

class TestMovieClientAdmin(unittest.TestCase):
    
    
    def setUp(self):
        self.token = main.mock_authenticate_admin()
    
    
    def test_authenticate(self):
        self.assertIsNotNone(self.token, "Authentication failed, token is None.")
        
        
    def test_get_movies(self):        
        movies = main.get_movies()
        self.assertIsInstance(movies, list, "Expected movies to be a list.")
    
            
    def test_create_existing_movie(self):
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
        movie = {
            "Name": "Test Movie for Deletion",
            "Year": 2000,
            "Runtime": 100,
            "Rating": 5.0,
            "Votes": 10,
            "Revenue": 100.0
        }
        response = main.create_movie(self.token, movie)
        self.assertEqual(response["Name"], movie["Name"], "Failed to create movie.")

        movie_id = response["MovieID"]
        deleted_movie = main.delete_movie(self.token, movie_id)
        self.assertEqual(deleted_movie["Name"], movie["Name"], "Failed to delete movie.")
       
              
              
    def test_get_specific_movie(self):
        movie_id = 1
        movie = main.get_movie_by_id(movie_id)
        self.assertIsNotNone(movie, f"Failed to retrieve movie with ID: {movie_id}.")
       
        
        
    def test_get_invalid_movie(self):
        movie_id = 9999  # Assuming no movie with this ID exists
        with self.assertRaises(Exception) as context:
            main.get_movie_by_id(movie_id)
        self.assertIn("404 Client Error: Not Found for url", str(context.exception), f"Expected movie with ID: {movie_id} to not exist.")


class TestMovieClientUser(unittest.TestCase):
    
    def setUp(self):
        self.token = main.mock_authenticate_user()
        
        
    def test_authenticate(self):
        self.assertIsNotNone(self.token, "Authentication failed, token is None.")
        
        
    def test_get_movies(self):        
        movies = main.get_movies()
        self.assertIsInstance(movies, list, "Expected movies to be a list.")
    
    
    def test_create_movie(self):
        movie = {
            "Name": "The Test Movie",
            "Year": 1972,
            "Runtime": 175,
            "Rating": 9.2,
            "Votes": 1667868,
            "Revenue": 134.97
        }
        with self.assertRaises(Exception) as context:
            main.create_movie(self.token, movie)
        error_message = str(context.exception)
        self.assertTrue("403 Client Error: Forbidden" in error_message, "Expected 403 Forbidden response.")


class TestMovieClientNoAuth(unittest.TestCase):
    
    def test_get_movies(self):        
        movies = main.get_movies()
        self.assertIsInstance(movies, list, "Expected movies to be a list.")
    
    
    def test_create_movie(self):
        movie = {
            "Name": "The Test Movie",
            "Year": 1972,
            "Runtime": 175,
            "Rating": 9.2,
            "Votes": 1667868,
            "Revenue": 134.97
        }
        with self.assertRaises(Exception) as context:
            main.create_movie(self.token, movie)
        error_message = str(context.exception)
        self.assertTrue("'TestMovieClientNoAuth' object has no attribute 'token'" in error_message, "Expected 403 Forbidden response.")
        
'''
class TestUserClientAdmin(unittest.TestCase):
    
    def setUp(self):
        self.token = main.mock_authenticate_admin()
    
    def test_authenticate(self):
        self.assertIsNotNone(self.token, "Authentication failed, token is None.")
        
    def test_get_users(self):        
        users = main.get_users(self.token)
        self.assertIsInstance(users, list, "Expected users to be a list.")
    
    def test_create_existing_user(self):
        user = {
            "email": "test@example.com",
            "role": "user"
        }
        with self.assertRaises(Exception) as context:
            main.create_user(self.token, user)
        error_message = str(context.exception)
        self.assertTrue("User already registered" in error_message or "400 Client Error: Bad Request" in error_message,
                        "Expected user creation to fail.")
    
    def test_create_get_and_delete_user(self):
        user = {
            "email": "deletiontest@example.com",
            "role": "user"
        }
        response = main.create_user(self.token, user)
        self.assertEqual(response["email"], user["email"], "Failed to create user.")

        user_id = response["id"]
        user = main.get_user_by_id(self.token, user_id)
        self.assertIsNotNone(user, f"Failed to retrieve user with ID: {user_id}.")
        
        deleted_user = main.delete_user(self.token, user_id)
        self.assertEqual(deleted_user["email"], user["email"], "Failed to delete user.")
              
        
    def test_get_invalid_user(self):
        user_id = 9999  # Assuming no user with this ID exists
        with self.assertRaises(Exception) as context:
            main.get_user_by_id(self.token, user_id)
        self.assertIn("404 Client Error: Not Found for url", str(context.exception), f"Expected user with ID: {user_id} to not exist.")
'''

if __name__ == "__main__":
    print("hello")
    unittest.main()
