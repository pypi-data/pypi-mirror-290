from fastapi import FastAPI
from botrun_ask_folder.fast_api.router_botrun_ask_folder import router
from botrun_ask_folder.fast_api.collection_status_api import (
    collection_status_api_router,
)

app = FastAPI()
api_botrun = FastAPI()


api_botrun.include_router(router)
api_botrun.include_router(collection_status_api_router)
app.mount("/api/botrun", api_botrun)
