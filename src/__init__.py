from src.errors import register_error_handlers
from fastapi import FastAPI
from src.auth.routes import auth_router
from src.categories.routes import categories_router
from src.datasource.routes import data_router
from src.scan.routers import scan_router
from src.tags.routers import tag_router
from src.dataset.routes import dataset_router

version = 'v1'
version_prefix =f"/api/{version}"
app = FastAPI(
    title='Mini Govern',
    description='',
    version=version
)

register_error_handlers(app)
app.include_router(auth_router,prefix=f"{version_prefix}/user" , tags=['user'])
app.include_router(categories_router,prefix=f"{version_prefix}/categories", tags= ['categories'])
app.include_router(data_router,prefix=f"{version_prefix}/datasource", tags= ['datasources'])
app.include_router(scan_router,prefix=f"{version_prefix}/scan" , tags=['scan'])
app.include_router(tag_router,prefix=f"{version_prefix}/tags" , tags=['tags'])
app.include_router(dataset_router,prefix=f"{version_prefix}/dataset" , tags=['datasets'])