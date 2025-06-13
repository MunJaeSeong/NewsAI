from supabase import create_client
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def register_user(email: str, password: str):
    hashed = hash_password(password)
    return supabase.table("users").insert({"email": email, "password": hashed}).execute()

def login_user(email: str, password: str):
    result = supabase.table("users").select("*").eq("email", email).single().execute()
    user = result.data
    if not user:
        return None
    if verify_password(password, user["password"]):
        return {"id": user["id"], "email": user["email"]}
    return None
