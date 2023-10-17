from app.interfaces.common import Rating


class MessMenuItem:
    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        rating: Rating | None = None,
        cal: int | None = None,
        image: str | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.rating = rating
        self.cal = cal
        self.image = image


class Mess:
    def __init__(self):
        pass
