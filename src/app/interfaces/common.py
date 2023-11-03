class Location:
    def __init__(self, latitude: str, longitude: str):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Location(latitude={self.latitude}, longitude={self.longitude})"
