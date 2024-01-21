import os

def whoAmI():
    try:
        username = os.getenv('USERNAME')
        
        if username:
            return username
        else:
            raise Exception('It was not possible to determine the user.')
    
    except Exception as e:
        raise Exception(f"Error getting username: {str(e)}")