from pymongo import MongoClient
import certifi
import ssl

uri = "mongodb+srv://kedar:kedar@authservice.qplb5.mongodb.net/authService?retryWrites=true&w=majority"

try:
    # Try with minimal SSL config
    client = MongoClient(
        uri,
        tlsCAFile=certifi.where(),
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    
    # Test the connection
    db = client.admin
    db.command('ping')
    print("Successfully connected to MongoDB!")
    
except Exception as e:
    print(f"Error connecting to MongoDB: {e}") 