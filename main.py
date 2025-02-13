import os
import random
from functools import reduce
import modal
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import googlemaps
import pastforward

static_dir = "static"
static_dir_remote = f"/root/{static_dir}"
gmp_api_key = "GMP_API_KEY"

image = (
    modal.Image.debian_slim()
    .pip_install("fastapi[standard]", "googlemaps")
    .add_local_python_source("pastforward")
    .add_local_dir(static_dir, remote_path=static_dir_remote)
)
app = modal.App(image=image)


def generate_historical_significance(place: pastforward.PastforwardPlace) -> str:
    # TODO: Implement https://app.toolhouse.ai/store/web_search
    return f"{place.name} is historically significant" if random.random() < 0.5 else ""


@app.function(secrets=[modal.Secret.from_name(gmp_api_key)])
@modal.asgi_app()
def main():
    fastapi_app = fastapi.FastAPI()
    gmaps = googlemaps.Client(key=os.environ[gmp_api_key])

    @fastapi_app.get("/places")
    async def places(_r: fastapi.Request, coordinates: str):
        gmp_places_nearby_results = gmaps.places_nearby(
            location=parse_coordinates(coordinates),
            type="point_of_interest",
            language="en",
            rank_by="distance",
        )["results"]

        def reduce_places(results, gmp_place):
            place = pastforward.from_gmp_place(gmp_place)
            historical_significance = generate_historical_significance(place=place)
            if historical_significance == "":
                return results

            return results + [place]

        # TODO: Filter places by historical significance via Groq and Toolhouse.
        return reduce(reduce_places, gmp_places_nearby_results, [])

    @fastapi_app.get("/places/{ref}.jpg")
    async def places_photo(_r: fastapi.Request, ref: str):
        return StreamingResponse(
            gmaps.places_photo(
                ref,
                {"maxwidth": 400},
            ),
            media_type="image/jpeg",
        )

    fastapi_app.mount(
        "/",
        StaticFiles(directory=static_dir_remote, html=True),
        name=static_dir,
    )

    return fastapi_app


def parse_coordinates(s):
    try:
        lat, lon = map(float, s.replace(" ", "").split(","))
        return lat, lon
    except (ValueError, AttributeError):
        return None
