from pydantic import BaseModel


class PastforwardPlace(BaseModel):
    address: str
    latitude: float
    longitude: float


def from_gmp_place(data) -> PastforwardPlace:
    return PastforwardPlace(
        address=data["formatted_address"],
        latitude=data["geometry"]["location"]["lat"],
        longitude=data["geometry"]["location"]["lng"],
    )
