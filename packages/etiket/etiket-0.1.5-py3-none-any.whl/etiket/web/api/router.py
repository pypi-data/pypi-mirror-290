from etiket.web.api.routers import auth, dataset, file, schema, scope, user, version, logs, s3 #, S3_transfers

from fastapi.routing import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(scope.router)
api_router.include_router(schema.router)
api_router.include_router(user.router)
api_router.include_router(dataset.router)
api_router.include_router(file.router)
api_router.include_router(version.router)
api_router.include_router(logs.router)
api_router.include_router(s3.router)
# api_router.include_router(S3_transfers.router)