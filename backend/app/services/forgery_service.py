import math
from sqlalchemy.orm import Session

# from app.models.user import User

class ForgeryService:
    EARTH_RADIUS_KM = 6371.0
    MAX_ALLOWED_DISTANCE_KM = 50.0

    def is_mac_mismatched(self, registered_mac: str, incoming_mac: str) -> bool:
        return registered_mac.strip().lower() != incoming_mac.strip().lower()

    def is_location_suspicious(self,
                               reg_lat: float, reg_lon: float,
                               inc_lat: float, inc_lon: float) -> bool:

        distance = self._calculate_haversine_distance(reg_lat, reg_lon, inc_lat, inc_lon)

        if distance > self.MAX_ALLOWED_DISTANCE_KM:
            return True
        return False

    def log_forgery_event(self, db: Session, user_id: str, reason: str, metadata: dict):

        print(f"[FORGERY DETECTED] User: {user_id} | Reason: {reason}")
        print(f"Logging metadata to DB: {metadata}")

        # db_log = ForgeryLog(user_id=user_id, reason=reason, meta=metadata)
        # db.add(db_log)
        # db.commit()

    def _calculate_haversine_distance(self, lat1, lon1, lat2, lon2) -> float:
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return self.EARTH_RADIUS_KM * c


forgery_checker = ForgeryService()