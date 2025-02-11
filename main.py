import os
import modal
import fastapi
from fastapi.staticfiles import StaticFiles
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


@app.function(secrets=[modal.Secret.from_dotenv()])
@modal.asgi_app()
def api():
    fastapi_app = fastapi.FastAPI()
    gmaps = googlemaps.Client(key=os.environ[gmp_api_key])

    @fastapi_app.get("/place")
    async def place(_request: fastapi.Request, coordinates: str):
        reverse_geocode_result = gmaps.reverse_geocode(parse_coordinates(coordinates))
        return [pastforward.from_gmp_place(x) for x in reverse_geocode_result]

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
