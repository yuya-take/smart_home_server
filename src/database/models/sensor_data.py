from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session


class SensorDataModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    temperature: float
    humidity: float
    pressure: float
    air_quality: float | None = None
    timestamp: datetime = Field(default_factory=datetime.now())
