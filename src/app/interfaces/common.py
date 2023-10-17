class Location:
    def __init__(self, latitude: str, longitude: str):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Location(latitude={self.latitude}, longitude={self.longitude})"


class Rating:
    def __init__(self, total: float, count: int):
        self.total = total
        self.count = count

    def __repr__(self):
        return f"Rating(total={self.total}, count={self.count}, value={self.value})"
