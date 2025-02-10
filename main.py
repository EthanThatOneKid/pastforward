import modal

static_dir = "static"
static_dir_remote = f"/root/{static_dir}"

image = (modal.Image.debian_slim()
            .pip_install("fastapi[standard]")
            .add_local_dir(static_dir, remote_path=static_dir_remote))
app = modal.App(image=image)

@app.function()
@modal.asgi_app()
def api():
    import fastapi
    from fastapi.staticfiles import StaticFiles

    fastapi_app = fastapi.FastAPI()

    @fastapi_app.get("/square/{x}")
    async def square(_request: fastapi.Request, x: str):
        return {"square": int(x)**2}
        
    fastapi_app.mount(
        "/",
        StaticFiles(directory=static_dir_remote, html=True),
        name=static_dir,
    )

    return fastapi_app
