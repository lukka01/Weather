from src.models.base import BaseModel
from ext import db


class WeatherRecord(BaseModel):
    __tablename__ = "weather_record"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float,   nullable=False)
    longitude= db.Column(db.Float,   nullable=False)
    temperature = db.Column(db.Float,   nullable=False)
    wind_speed = db.Column(db.Float,   nullable=False)
    weather_code = db.Column(db.Integer, nullable=False)
    fetched_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id":self.id,
            "latitude": self.latitude,
            "longitude":self.longitude,
            "temperature_celsius": self.temperature,
            "wind_speed_kmh":self.wind_speed,
            "weather_code":self.weather_code,
            "fetched_at":self.fetched_at.isoformat() if self.fetched_at else None,
        }