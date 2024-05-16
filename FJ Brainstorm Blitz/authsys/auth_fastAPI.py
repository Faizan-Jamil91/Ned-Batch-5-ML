from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import bcrypt
from datetime import datetime, timedelta
import jwt
#from email_config import send_registration_email
import google.generativeai as genai
import random
import pandas as pd

# Replace DATABASE_URL with your actual connection string
DATABASE_URL = "postgresql://todos_owner:od0gPGeTRn3U@ep-raspy-salad-a5rggins.us-east-2.aws.neon.tech/User_Auth?sslmode=require"

# Secret key for token generation, replace with a securely generated key
SECRET_KEY = "80e9fcfa7c9213cb61d03af5b4a7fc8927f0f7d336b547d87643c4dad56cf6d7"

# Token expiration time (e.g., 30 minutes)
TOKEN_EXPIRATION = timedelta(minutes=30)

# Add salt rounds for bcrypt
SALT_ROUNDS = 12

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Define SQLAlchemy base class
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DatabaseManager:
    def __init__(self):
        self.session = SessionLocal()

    def get_user_by_username(self, username):
        return self.session.query(User).filter_by(username=username).first()

    def create_user(self, username, email, password_hash, salt):
        new_user = User(username=username, email=email, password_hash=password_hash, salt=salt)
        self.session.add(new_user)
        self.session.commit()

    def close_session(self):
        self.session.close()


class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def register_user(self, username, password, password_confirm, email):
        if password != password_confirm:
            raise HTTPException(status_code=400, detail="Password confirmation doesn't match password")

        user = self.db_manager.get_user_by_username(username)
        if user:
            raise HTTPException(status_code=400, detail="Username already exists")

        salt = bcrypt.gensalt(SALT_ROUNDS)
        hashed_password = bcrypt.hashpw(password.encode() + salt, bcrypt.gensalt())

        self.db_manager.create_user(username, email, hashed_password.decode(), salt.decode())
        #send_registration_email(email, username)

        return {"message": "User registered successfully. Check your email for confirmation."}


class AuthManager:
    @staticmethod
    def generate_token(user_id):
        token_data = {"user_id": user_id, "exp": datetime.utcnow() + TOKEN_EXPIRATION}
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
        return token


class ContentGenerator:
    def __init__(self):
        pass
    
    async def generate_content(self, prompt):
        try:
            genai.configure(api_key="AIzaSyBhppYwUZpoD8mqhnJ2ZLl1asuF957gFlU")  # Replace with your API key
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }

            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ]

            model = genai.GenerativeModel(model_name="gemini-pro",
                                          generation_config=generation_config,
                                          safety_settings=safety_settings)

            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


class MCQGenerator:
    def __init__(self, content_generator):
        self.content_generator = content_generator
        self.generated_mcqs_cache = {}
        
    async def generate_mcqs(self, topic_input):
        prompt = f"Generate 20 multiple-choice questions related to the topic: {topic_input} without answer key"
        mcqs = await self.content_generator.generate_content(prompt)
        self.generated_mcqs_cache[topic_input] = mcqs
        return {"mcqs": mcqs}
    
    async def generate_result(self, result, collected_answers):
        try:
            prompt1 = f"Provide the answer keys for the following questions related to Mcqs below\n {result} : \n{collected_answers} \nPlease provide the answers in capital letters (e.g., ABCD) in the format of a DataFrame."
            result1 = await self.content_generator.generate_content(prompt1)
            prompt2 = f"Match the answers provided by the user collected answer option{collected_answers}, is equal to the {result1} generated answer option, and calculate the correct and incorrect answer if no answer match with the date its mean that all answers are incorrect"
            result2 = await self.content_generator.generate_content(prompt2)
            prompt3 = f"please provide the sumrized result {result2}"
            result3= await self.content_generator.generate_content(prompt3)
            return {"result1" : result1 , "result2" : result2 , "result3" : result3}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can restrict it to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

db_manager = DatabaseManager()
user_manager = UserManager(db_manager)
auth_manager = AuthManager()
content_generator = ContentGenerator()
mcq_generator = MCQGenerator(content_generator)


@app.post("/register/")
def register_user(username: str, password: str, password_confirm: str, email: str):
    return user_manager.register_user(username, password, password_confirm, email)


@app.post("/login/")
def authenticate_user(username: str, password: str):
    user = db_manager.get_user_by_username(username)
    if not user or not bcrypt.checkpw(password.encode() + user.salt.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = auth_manager.generate_token(user.id)
    return {"token": token}


@app.post("/generate_mcqs/")
async def generate_mcqs(topic_input: str):
    try:
        return await mcq_generator.generate_mcqs(topic_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate_result/")
async def generate_result(result: str, collected_answers: str):
    try:
        return await mcq_generator.generate_result(result, collected_answers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


