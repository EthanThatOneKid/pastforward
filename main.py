import os
import random
from functools import reduce
import modal
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import googlemaps
from toolhouse import Toolhouse
from groq import Groq
import pastforward

static_dir = "static"
static_dir_remote = f"/root/{static_dir}"
gmp_api_key = "GMP_API_KEY"
groq_api_key = "GROQ_API_KEY"
toolhouse_api_key = "TOOLHOUSE_API_KEY"
model_id = "llama-3.3-70b-versatile"

image = (
    modal.Image.debian_slim()
    .pip_install("fastapi[standard]", "googlemaps", "toolhouse", "groq")
    .add_local_python_source("pastforward")
    .add_local_dir(static_dir, remote_path=static_dir_remote)
)
app = modal.App(image=image)


def generate_historical_significance(
    groq, toolhouse, place: pastforward.PastforwardPlace
) -> str:
    result = create_completion_with_toolhouse(
        groq,
        toolhouse,
        [
            {
                "role": "user",
                "content": """
    I'd like you to compile a Hacker News Digest. The digest should summarize each one of the top 3 articles, and it should read the comments page for each one of the articles.
        
        Use scraper or diffbot to get the contents of news.ycombinator.com, then do this for each article:

        1. Get the contents of each article. If you can't access an article, move onto the next one.
        2. Get the contents of the comments page for the article. The URL for the comment page looks like this: example: https://news.ycombinator.com?item=<itemId>.
        3. Provide a short summary of each article, then read the comments for each one article and summarize top opinions and overall sentiment of those comments.
        
        When done, send a summary via email at ethan.r.davidson@gmail.com. Format the email nicely in HTML. The subject line is "Your Hacker News Digest". In the footer of the email, make sure to explain this email has been sent by Toolhouse. Make sure to show the user the link to change its deliver preferences at https://app.toolhouse.ai/settings.
  """,
            }
        ],
    )
    print(result)

    # TODO: Implement https://app.toolhouse.ai/store/web_search
    return place.name if random.random() < 0.5 else ""


@app.function(secrets=[modal.Secret.from_dotenv()])
@modal.asgi_app()
def api():
    fastapi_app = fastapi.FastAPI()
    gmaps = googlemaps.Client(key=os.environ[gmp_api_key])
    groq = Groq(api_key=os.environ[groq_api_key])
    toolhouse = Toolhouse(api_key=os.environ[toolhouse_api_key])

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
            historical_significance = generate_historical_significance(
                groq, toolhouse, place
            )
            if historical_significance == "":
                return results

            return results + [place]

        # TODO: Filter places by historical significance via Groq.
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


def create_completion_with_toolhouse(groq, toolhouse, messages: list[dict]):
    def llm_call(messages: list[dict]):
        return groq.chat.completions.create(
            model=model_id,
            max_tokens=1024,
            messages=messages,
            tools=toolhouse.get_tools(),
        )

    response = llm_call(messages)
    messages += toolhouse.run_tools(response, append=True)
    final_response = llm_call(messages)
    return final_response.choices[0].text
