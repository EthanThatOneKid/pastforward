from pydantic import BaseModel


class PastforwardPlace(BaseModel):
    id: str
    address: str
    name: str
    latitude: float
    longitude: float
    photo_refs: list[str] | None


def from_gmp_place(details) -> PastforwardPlace:
    photo_refs = (
        None
        if not "photos" in details["result"]
        else [x["photo_reference"] for x in details["result"]["photos"]]
    )
    return PastforwardPlace(
        id=details["result"]["place_id"],
        address=details["result"]["formatted_address"],
        name=details["result"]["name"],
        latitude=details["result"]["geometry"]["location"]["lat"],
        longitude=details["result"]["geometry"]["location"]["lng"],
        photo_refs=photo_refs,
    )
