import re
from passlib.context import CryptContext
from fastapi import HTTPException, Form
from datetime import datetime, timedelta
from jose import jwt
from models.mongo_service import *
from otp_email import *
from models.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Temporary storage for registration data in cache
registration_cache = {}

async def register_user(user: UserCreate):
    try:
        existing_user = user_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
            raise HTTPException(status_code=400, detail="Invalid email address")

        if (
            not re.search(r"[A-Z]", user.password)
            or not re.search(r"[a-z]", user.password)
            or not re.search(r"\d", user.password)
            or not re.search(r"[!@#$%^&*()]", user.password)
            or len(user.password) < 8
        ):
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long and contain at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character",
            )

        # Generate OTP
        otp = generate_otp()

        # Store registration data in cache
        registration_cache = {
            "email": user.email,
            "password": user.password,
            "otp": otp,
            "timestamp": datetime.now(),
        }

        # Send OTP to user (e.g., via email or SMS)
        send_otp(user.email, otp)

        return {"message": "OTP sent to user"}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
async def verify_otp_and_register(otp: str):
    try:
        email = registration_cache["email"]
        stored_otp = registration_cache["otp"]
        timestamp = registration_cache["timestamp"]

        # Verify OTP
        if not verify_otp(email, otp):
            raise HTTPException(status_code=400, detail="Invalid OTP")

        # Verify OTP expiration (e.g., 5 minutes)
        expiration_time = timedelta(minutes=5)
        if datetime.now() - timestamp > expiration_time:
            raise HTTPException(status_code=400, detail="OTP expired")

        # Store user data
        password = registration_cache["password"]
        hashed_password = pwd_context.hash(password)
        user_data = {"email": email, "hashed_password": hashed_password}

        # Add user to the database
        user_collection.insert_one(user_data)

        # Remove registration data from cache
        del registration_cache[email]

        return {"message": "User Created Successfully"}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

        
async def authenticate_user(body: str = Form(...)):
    try:
        email = body["username"]
        password = body["password"]   
        user = user_collection.find_one({"email": email})
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        hashed_password = user["hashed_password"]
        
        if not pwd_context.verify(password, hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = jwt.encode(
            {
                "sub": user["email"],
                "exp": datetime.utcnow() + access_token_expires
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
