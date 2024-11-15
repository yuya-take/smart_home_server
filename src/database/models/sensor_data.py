from datetime import datetime
from sqlmodel import SQLModel, Field


class SensorDataModel(SQLModel, table=True):
    __tablename__ = "sensor_data"

    id: int | None = Field(default=None, primary_key=True)
    temperature: float
    humidity: float
    pressure: float
    air_quality: float | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
