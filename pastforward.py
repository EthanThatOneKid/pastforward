from pydantic import BaseModel


class PastforwardPlace(BaseModel):
    id: str
    address: str
    name: str
    latitude: float
    longitude: float
    types: list[str]
    photo_refs: list[str]


def from_gmp_place(gmp_place) -> PastforwardPlace:
    photo_refs = (
        []
        if not "photos" in gmp_place
        else [x["photo_reference"] for x in gmp_place["photos"]]
    )
    return PastforwardPlace(
        id=gmp_place["place_id"],
        address=gmp_place["vicinity"],
        name=gmp_place["name"],
        latitude=gmp_place["geometry"]["location"]["lat"],
        longitude=gmp_place["geometry"]["location"]["lng"],
        types=gmp_place["types"],
        photo_refs=photo_refs,
    )
