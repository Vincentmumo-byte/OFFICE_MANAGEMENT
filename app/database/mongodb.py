import logging

from pymongo import ASCENDING, MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from app.config import settings


logger = logging.getLogger("OfficeManagement.database")


client = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000,
)

database = client[settings.MONGO_DB_NAME]

users_collection = database["users"]
employees_collection = database["employees"]


def connect_to_mongo() -> None:
    """Test the MongoDB connection."""

    try:
        client.admin.command("ping")

        logger.info(
            "Connected to MongoDB at %s",
            settings.MONGO_URI,
        )

    except ServerSelectionTimeoutError as exc:
        logger.error(
            "Could not connect to MongoDB: %s",
            exc,
        )
        raise


users_collection.create_index(
    [("email", ASCENDING)],
    unique=True,
)

employees_collection.create_index(
    [("employee_id", ASCENDING)],
    unique=True,
)

employees_collection.create_index(
    [("email", ASCENDING)],
    unique=True,
)

employees_collection.create_index(
    [("department", ASCENDING)],
)

employees_collection.create_index(
    [("designation", ASCENDING)],
)

employees_collection.create_index(
    [("first_name", ASCENDING)],
)

employees_collection.create_index(
    [("second_name", ASCENDING)],
)

employees_collection.create_index(
    [("salary", ASCENDING)],
)

employees_collection.create_index(
    [("joining_date", ASCENDING)],
)


def close_mongo_connection() -> None:
    """Close the MongoDB connection."""

    client.close()

    logger.info("MongoDB connection closed")