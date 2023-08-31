import os

class Config:
    """ Server Service Configuration
    Can be modified in .env, examples are in .env.example """
    
    # Helper to read numbers using var envs
    def cast_to_number(id):
        temp = os.environ[id]
        if temp is not None:
            try:
                return float(temp)
            except ValueError:
                return None
        return None
    
    user = os.environ['MYSQL_USER']
    password = os.environ['MYSQL_PASSWORD']
    host = os.environ['MYSQL_HOST'] 
    database = os.environ['MYSQL_DATABASE']
    DATABASE_URL = f"mysql://{user}:{password}@{host}/{database}"
    
    API_SECRET_KEY = os.environ['API_SECRET_KEY']
    SECRET_KEY = os.environ['SECRET_KEY']
    FRONTEND_URL = os.environ['FRONTEND_URL']
    REFRESH_TOKEN_EXPIRE_MINUTES = cast_to_number('REFRESH_TOKEN_EXPIRE_MINUTES')
    API_ALGORITHM = os.environ['API_ALGORITHM']
    API_ACCESS_TOKEN_EXPIRE_MINUTES = cast_to_number('API_ACCESS_TOKEN_EXPIRE_MINUTES')
    
    GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
    