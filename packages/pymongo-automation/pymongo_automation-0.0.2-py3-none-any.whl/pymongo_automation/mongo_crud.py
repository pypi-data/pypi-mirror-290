from typing import Any
import os
import pandas as pd
from pymongo.mongo_client import MongoClient
import json
from pymongo.errors import BulkWriteError
from bson import ObjectId



def clean_data(data):
    for record in data:
        for key, value in record.items():
            if isinstance(value, str):
                record[key] = value.encode('utf-8', 'ignore').decode('utf-8')
    return data


class mongo_operation:
    __collection = None  # here I have created a private/protected variable
    __database = None

    def __init__(self, client_url: str, database_name: str, collection_name: str = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name

    def create_mongo_client(self) -> MongoClient:
        client: MongoClient = MongoClient(self.client_url, ssl=True)
        return client

    def create_database(self) -> Any:
        if mongo_operation.__database is None:
            client = self.create_mongo_client()
            mongo_operation.__database = client[self.database_name]
        return mongo_operation.__database

    def create_collection(self, collection: str = None) -> Any:
        if collection is None:
            collection = self.collection_name
        if mongo_operation.__collection is None:
            database = self.create_database()
            mongo_operation.__collection = database[collection]
        return mongo_operation.__collection

    def insert_record(self, record: dict, collection_name: str) -> Any:
        if isinstance(record, list):
            for data in record:
                if not isinstance(data, dict):
                    raise TypeError("Record must be a dictionary")
            collection = self.create_collection(collection_name)
            collection.insert_many(record)
        elif isinstance(record, dict):
            collection = self.create_collection(collection_name)
            collection.insert_one(record)

    def bulk_insert(self, datafile: str, collection_name: str = None) -> None:
        self.path = datafile

        if self.path.endswith('.csv'):
            dataframe = pd.read_csv(self.path)
        elif self.path.endswith(".xlsx"):
            dataframe = pd.read_excel(self.path)
        else:
            raise ValueError("Unsupported file format. Only .csv and .xlsx are supported.")

        datajson = json.loads(dataframe.to_json(orient='records'))
        collection = self.create_collection(collection_name)
        collection.insert_many(datajson)


    def export_collection_to_df(self, collection_name: str, query: dict = {}) -> pd.DataFrame:
        collection_name = self.create_collection(collection_name)
        cursor = collection_name.find(query)
        records = list(cursor)
        cleaned_records = clean_data(records)
        df = pd.DataFrame(cleaned_records)
        return df
    

    def export_collection_to_file(self, collection_name: str, file_path: str, query:dict = {}, file_format: str = 'csv') -> None:
        df = self.export_collection_to_df(collection_name, query)
        if file_format.lower() == 'csv':
            df.to_csv(file_path, index=False)
        elif file_format.lower() == 'xlsx':
            df.to_excel(file_path, index=False)
        else:
            raise ValueError("Unsupported file format. Only csv and xlsx are supported.")
        

    def update_records(self, collection_name: str, query: dict, update_values: dict) -> None:
        collection = self.create_collection(collection_name)
        collection.update_many(query, {'$set': update_values})


    def delete_records(self, collection_name: str, query: dict) -> None:
        collection = self.create_collection(collection_name)
        collection.delete_many(query)


    def count_documents(self, collection_name: str, query: dict = {}) -> int:
        collection = self.create_collection(collection_name)
        return collection.count_documents(query)
    

    def drop_collection(self, collection_name: str) -> None:
        collection = self.create_collection(collection_name)
        collection.drop()


    # def backup_collection(self, collection_name: str, file_path: str) -> None:
    #     df = self.export_collection_to_df(collection_name)
    #     df.to_json(file_path, orient='records', force_ascii=False, lines=True, default_handler=str)

    # def restore_collection(self, file_path: str, collection_name: str = None) -> None:
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         data = []
    #         for line in file:
    #             try:
    #                 json_data = json.loads(line.strip())
    #                 data.append(json_data)
    #             except json.JSONDecodeError as e:
    #                 print(f"Error decoding JSON: {e}")

    #     if collection_name is None:
    #         collection_name = self.collection_name

    #     self.insert_record(data, collection_name)

    
    def run_aggregate_pipeline(self, collection_name: str, pipeline: list) -> pd.DataFrame:
        collection = self.create_collection(collection_name)
        cursor = collection.aggregate(pipeline)
        df = pd.DataFrame(list(cursor))
        return df
    

    def collection_exists(self, collection_name: str) -> bool:
        database = self.create_database()
        return collection_name in database.list_collection_names()
    

    def list_collections(self) -> list:
        database = self.create_database()
        return database.list_collection_names()
    

    def insert_from_json(self, json_file_path: str, collection_name: str = None) -> None:
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)  # Load the entire JSON file at once

            # Debugging: Print the type of data loaded
            print(f"Data loaded from JSON: {type(data)}")
            
            if collection_name is None:
                collection_name = self.collection_name
            
            # Handle case where data is a single object, not a list
            if isinstance(data, dict):
                data = [data]
            
            # Ensure the data is a list of dictionaries
            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                raise ValueError("The JSON file does not contain a list of dictionaries.")
            
            # Debugging: Print the first few records to see the structure
            print(f"First record in data: {data[0] if data else 'No data'}")

            # Attempt to insert data into MongoDB
            try:
                collection = self.create_collection(collection_name)
                collection.insert_many(data, ordered=False)
                print(f"Data inserted from '{json_file_path}' into '{collection_name}' collection.")
            
            except BulkWriteError as bwe:
                print(f"Bulk write error: {bwe.details}")
        
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {json_file_path}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def update_documents(self, collection_name: str, filter_dict: dict, update_dict: dict) -> None:
        collection = self.create_collection(collection_name)
        collection.update_many(filter_dict, {'$set': update_dict})
        print(f"Documents matching {filter_dict} have been updated.")


    def backup_collection(self, collection_name: str, backup_file: str) -> None:
        try:
            # Fetch data from the MongoDB collection
            collection = self.create_collection(collection_name)
            data = list(collection.find({}))

            # Print fetched data to verify it before writing to the file
            print("Fetched Data:", data)

            if data:
                # Convert ObjectId to strings for JSON serialization
                for document in data:
                    if '_id' in document and isinstance(document['_id'], ObjectId):
                        document['_id'] = str(document['_id'])

                # Write the data to the backup file
                with open(backup_file, 'w') as f:
                    json.dump(data, f, indent=4)
                
                print(f"Backup of {collection_name} created at {backup_file}.")
            else:
                print(f"No data found in collection {collection_name} to backup.")

        except Exception as e:
            print(f"An error occurred during backup: {e}")


    def restore_collection(self, collection_name: str, backup_file: str) -> None:
        collection = self.create_collection(collection_name)
        with open(backup_file, 'r') as f:
            data = json.load(f)

        # Remove _id field from each document
        for document in data:
            if '_id' in document:
                del document['_id']

        try:
            collection.insert_many(data)
            print(f"Data restored to {collection_name} from {backup_file}.")
        except Exception as e:
            print(f"An error occurred during restore: {e}")


    # def monitor_changes(self, collection_name: str, callback, filter_query: dict = None) -> None:
    #     collection = self.create_collection(collection_name)
    #     pipeline = [{'$match': filter_query}] if filter_query else []
    #     with collection.watch(pipeline=pipeline) as stream:
    #         print(f"Monitoring changes on collection: {collection_name} with filter: {filter_query}")
    #         for change in stream:
    #             callback(change)


    # def print_change(change):
    #     print(f"Change detected: {change}")

    
    def delete_documents(self, collection_name: str, filter_dict: dict) -> None:
        collection = self.create_collection(collection_name)
        collection.delete_many(filter_dict)
        print(f"Documents matching {filter_dict} have been deleted.")



    def fetch_random_sample(self, collection_name: str, sample_size: int) -> pd.DataFrame:
        collection = self.create_collection(collection_name)
        pipeline = [{"$sample": {"size": sample_size}}]
        cursor = collection.aggregate(pipeline)
        return pd.DataFrame(list(cursor))

