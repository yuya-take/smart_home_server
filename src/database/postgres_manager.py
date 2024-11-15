import os
import contextlib
from datetime import datetime

from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv

from logger.logger import logger
from database.models.sensor_data import SensorDataModel
from utils.error_types import CreateRecordError


load_dotenv(verbose=True)


class PostgresManager:
    def __init__(self):
        DATABASE = os.environ.get("DATABASE", "postgresql")
        USER = os.environ.get("DB_USER", "postgres")
        PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
        HOST = os.environ.get("DB_HOST", "localhost")
        PORT = os.environ.get("DB_PORT", "5433")
        DB_NAME = os.environ.get("DB_NAME", "smart_home")

        DATABASE_URL = f"{DATABASE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
        ECHO_LOG = False

        self.engine = create_engine(DATABASE_URL, echo=ECHO_LOG)
        SQLModel.metadata.create_all(self.engine)

    @contextlib.contextmanager
    def session_scope(self):
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.error(f"Failed to commit session: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def create_record_in_sensor_data(self, sensor_data_model: SensorDataModel):
        try:
            with self.session_scope() as session:
                session.add(sensor_data_model)
                logger.info(f"Record created in sensor_data: {sensor_data_model}")
        except Exception as e:
            logger.error(f"Failed to create record in sensor_data: {e}")
            raise CreateRecordError("Failed to create record in sensor_data") from None

    def get_sensor_data(self, from_datetime: datetime = None, to_datetime: datetime = None) -> list[SensorDataModel]:
        with self.session_scope() as session:
            stmt = select(SensorDataModel)
            if from_datetime:
                stmt = stmt.where(SensorDataModel.timestamp >= from_datetime)
            if to_datetime:
                stmt = stmt.where(SensorDataModel.timestamp <= to_datetime)
            results = session.exec(stmt).all()
            data_list = [SensorDataModel(**result.__dict__) for result in results]
            return data_list
