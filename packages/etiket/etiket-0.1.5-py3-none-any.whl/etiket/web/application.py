from etiket.web.api.docs import description, title, tags_metadata, version
from etiket.web.api.router import api_router
from etiket.web.lifetime import register_shutdown_event, register_startup_event
from etiket.web.profiling import register_profiling
from fastapi import FastAPI
from etiket.settings import settings

def get_app() -> FastAPI:
    app = FastAPI(title=title, version=version,
              description=description, openapi_tags=tags_metadata,
              debug=True)
    app.openapi_version = "3.0.0"

    register_startup_event(app)
    register_shutdown_event(app)
    if settings.PROFILING:
        register_profiling(app)

    app.include_router(router=api_router, prefix="/api/v2")
    
    return app