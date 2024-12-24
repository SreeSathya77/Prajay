#######################################################################################################################
# Package Title: Util for Test Data Generator for QM ETC APIs and Application.
# Revision: 1.0.
# Date: 29 Nov 2024
# Author(s): Anand
#######################################################################################################################
from pymongo import MongoClient
import random


class QMMasterTables:
    # Utility to test data. Data will be fetched from the QM Master tables

    def __init__(self):
        self.db_uri = "mongodb://quantumqa:quantumqa@mongors0-3:9042,mongors0-4:9142,mongors0-5:9242/cseportal"  # Replace with your MongoDB URI
        self.db_name = "cseportal"  # Replace with your database name
        self.collection_name = "master_countries_state"  # Replace with your collection name

    def get_states_by_country(self, country_name="United States"):
        """
        Fetches states and their codes for a given country name from MongoDB.

        :param country_name: Name of the country to search for.
        :return: Dictionary containing states with their codes and names, or an error message if not found.
        """
        # Initialize MongoDB client
        client = MongoClient(self.db_uri)
        db = client[self.db_name]
        collection = db[self.collection_name]

        # Query to find the specified country
        record = collection.find_one({"countryName": country_name})

        if not record:
            client.close()
            return {"error": f"Country '{country_name}' not found in the database."}

        # Prepare the output structure
        result = {"country": country_name, "states": {}}

        for state in record.get("states", []):
            state_code = state.get("code", "Unknown State Code")
            state_name = state.get("name", "Unknown State Name")

            # Add state to the result
            result["states"][state_code] = state_name

        client.close()
        states = result['states']
        country_code = "US"
        match country_name:
                case "Canada":
                    country_code = "CA"
                case "United States":
                    country_code = "US"
                case "Mexico":
                    country_code = "MX"

        state_code = random.choice(list(states))
        state_name = states[state_code]
        return {"country_name": country_name, "country_code":country_code, "state_code": state_code, "state_name":state_name}
