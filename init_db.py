import models
import database
from sqlalchemy import text
from passlib.context import CryptContext

# Fix for the placeholder password in SeedData.sql
# In the SQL, we put a placeholder hash. Here we can update it or just execute.
# Better: We'll implement a logic to recreate the user with a known password if we want to be fancy,
# but strictly, we'll just running the SQL.
# HOWEVER, the SQL has a specific hash placeholder. 
# Let's clean up the SQL execution:

def init_db():
    print("Creating tables...")
    models.Base.metadata.create_all(bind=database.engine)
    
    print("Seeding data from SeedData.sql...")
    try:
        with open("SeedData.sql", "r") as f:
            sql_script = f.read()
            
        db = database.SessionLocal()
        
        # Split by statements
        # SQLite python driver can execute script, but SQLAlchemy execute() is one by one usually or raw.
        # Simple hack: split by ';'
        statements = sql_script.split(";")
        
        # We need a proper hash for 'password'
        pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        real_hash = pwd_context.hash("password")
        
        for statement in statements:
            if statement.strip():
                # Replace placeholder if present
                if "VALUES ('testuser'" in statement:
                     # This is a bit fragile but works for the specific file generated
                     # The generated file has: VALUES ('testuser', '$argon2id$v=19$m=65536,t=3,p=4$Dn9/wWl/dE7p...$hash...')
                     # We will replace the hash part or just run an UPDATE after.
                     # Easier: Just execute, then update.
                     pass
                
                try:
                    db.execute(text(statement))
                except Exception as e:
                    print(f"Statement skipped or error: {e}")
                    # Likely error if user already exists due to UNIQUE constraint
        
        db.commit()
        
        # Ensure testuser has valid password
        user = db.query(models.User).filter(models.User.username == "testuser").first()
        if user:
            user.password_hash = real_hash
            db.commit()
            print(f"User 'testuser' password set to 'password'.")
            
        print("Database initialized and seeded!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
