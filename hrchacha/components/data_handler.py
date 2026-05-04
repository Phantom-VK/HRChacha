import sys
import uuid

from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from hrchacha.constants import DB_NAME, COLLECTION_NAME
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging
from hrchacha.utils.general_utils import get_secret


class Database:
    def __init__(self):
        try:
            uri = get_secret("MONGO_URI")

            if not uri:
                raise ValueError("MONGO_URI not set in environment variables or secrets.")

            self.client = MongoClient(uri, server_api=ServerApi('1'))

            self.db = self.client[DB_NAME]
            self.collection: Collection = self.db[COLLECTION_NAME]


            self.client.admin.command("ping")
            logging.info("Connected to MongoDB. database=%s collection=%s", DB_NAME, COLLECTION_NAME)

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            # Fail fast so downstream code doesn't operate with invalid state
            raise

    def insert_user(self, user_data: dict) -> bool:
        """Upsert a candidate record. Returns True if MongoDB acknowledges the write."""
        try:
            email = user_data.get("email")

            if not email:
                email = f"session-{uuid.uuid4()}@placeholder.local"
                user_data["email"] = email
                logging.warning("Candidate data has no email. Generated placeholder email=%s", email)

            logging.info(
                "Uploading candidate data to MongoDB. email=%s keys=%s",
                email,
                sorted(user_data.keys()),
            )
            result = self.collection.update_one(
                {"email": email},
                {"$set": user_data},
                upsert=True,
            )
            logging.info(
                "MongoDB upload completed. acknowledged=%s matched=%d modified=%d upserted_id=%s",
                result.acknowledged,
                result.matched_count,
                result.modified_count,
                result.upserted_id,
            )

            return result.acknowledged
        except Exception as e:
            err = HRChachaException(e, sys)
            logging.exception(
                "MongoDB upload failed. email=%s error_type=%s",
                user_data.get("email"),
                type(e).__name__,
            )
            logging.error(str(err))
            return False

    def update_user(self, email: str, updated_data: dict) -> bool:
        """Update an existing user's record."""
        try:
            result = self.collection.update_one(
                {"email": email},
                {"$set": updated_data}
            )
            if result.modified_count:
                logging.info("User data updated")
                return True
            if result.matched_count:
                logging.info("User data already up to date")
                return True

            logging.info("No matching user found to update")
            return False
        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            return False
