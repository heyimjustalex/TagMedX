from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector
from models.models import User 


db_config = {
    "host": "db_TagMedX",
    "user": "user",
    "password": "password",
    "database": "db",
    "port": 3306,
}

try:
    # Attempt to establish a connection to the database
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        print("Connected to MySQL database")
        connection.close()
    else:
        print("Failed to connect to MySQL database")

except mysql.connector.Error as e:
    print("Error: ", e)
app = FastAPI()


database_uri = 'mysql://user:password@db_TagMedX:3306/db'
engine = create_engine(database_uri)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    # Use the User model to query the database
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    if user:
        return {"user_id": user.id, "name": user.name}
    return {"message": "User not found"}

@app.get("/users")
def get_all_users():
    # Create a session using SessionLocal
    session = SessionLocal()

    # Query all users from the User model
    users = session.query(User).all()

    # Close the session
    session.close()

    # Convert the list of users to a list of dictionaries
    user_data = [{"user_id": user.id, "name": user.name} for user in users]

    return user_data