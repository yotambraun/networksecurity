from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestconfig)
        logging.info("initiate the data ingestion process")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
       
    except Exception as e:
        raise NetworkSecurityException(e,sys)