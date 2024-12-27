from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pymongo
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_collection_as_dataframe(self):
        """
        Read the data from the MongoDB collection and return it as a pandas dataframe
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mong_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mong_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"nan": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_datat_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set,test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info(f"Preforming Train-Test split on the data")
            logging.info(f"Exited split_data_as_train_test method of DataIngestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Exporting train and test file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            logging.info(f"Exported train and test file path")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_datat_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.training_file_path)
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)