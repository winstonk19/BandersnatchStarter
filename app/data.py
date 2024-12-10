from os import getenv
import certifi
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient
import pandas as pd

class Database:
    """
    A class to interface with the MongoDB database for managing monsters.
    """
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Get the MongoDB connection string from the environment
        db_url = getenv("DB_URL")
        if not db_url:
            raise ValueError("DB_URL environment variable is missing.")

        # Establish a MongoDB client connection
        self.client = MongoClient(db_url, tlsCAFile=certifi.where())["your_database_name"]
        self.collection = self.client["Monster"]
        print(f"Connected successfully to '{self.client.name}'.")

    def seed(self, amount: int = 1000):
        """Populate the database with random monster data."""
        monster_list = []
        for _ in range(amount):
            try:
                monster = Monster()
                monster_dict = monster.to_dict()
                monster_list.append(monster_dict)
            except Exception as e:
                print(f"Error creating monster: {e}")

        
        result = self.collection.insert_many(monster_list)
        print(f"{len(result.inserted_ids)} monsters seeded successfully to the database.")

    def reset(self):
        """Clear the entire collection to start fresh."""
        delete_result = self.collection.delete_many({})
        print(f"{delete_result.deleted_count} documents deleted. Database reset successfully.")

    def count(self) -> int:
        """Return the number of documents in the collection."""
        try:
            count = self.collection.count_documents({})
            return count
        except Exception as e:
            print(f"Error while counting documents: {e}")
            return 0

    def dataframe(self) -> DataFrame:
        """Return a DataFrame containing all monster data."""
        try:
            documents = self.collection.find({}, {"_id": False})
            doc_list = list(documents)
            return pd.DataFrame(doc_list)
        except Exception as e:
            print(f"Error while fetching data: {e}")
            return pd.DataFrame()

    def html_table(self) -> str:
        """Return an HTML table representation of the DataFrame."""
        df = self.dataframe()
        if df.empty:
            print("DataFrame is empty. No HTML table generated.")
            return "<p>No data available</p>"

        return df.to_html(classes="table table-striped", index=False)

if __name__ == "__main__":
    db = Database()
    print(f"Initial count: {db.count()}")

    db.seed(990)  # Seed 10 monsters
    print(f"Count after seeding: {db.count()}")

    

    
    
   
  
 