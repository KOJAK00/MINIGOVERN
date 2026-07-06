from src.errors import register_error_handlers
from fastapi import FastAPI
from src.auth.routes import auth_router
from src.categories.routes import categories_router
from src.datasource.routes import data_router
from src.scan.routers import scan_router
from src.tags.routers import tag_router
from src.dataset.routes import dataset_router
from src.audit.routes import audit_router
from src.masking.routes import masking_router
from fastapi.middleware.cors import CORSMiddleware


version = 'v1'
version_prefix =f"/api/{version}"
app = FastAPI(
    title='Mini Govern',
    description='',
    version=version
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://0.0.0.0:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)
app.include_router(auth_router,prefix=f"{version_prefix}/user" , tags=['user'])
app.include_router(categories_router,prefix=f"{version_prefix}/categories", tags= ['categories'])
app.include_router(data_router,prefix=f"{version_prefix}/datasource", tags= ['datasources'])
app.include_router(scan_router,prefix=f"{version_prefix}/scan" , tags=['scan'])
app.include_router(tag_router,prefix=f"{version_prefix}/tags" , tags=['tags'])
app.include_router(dataset_router,prefix=f"{version_prefix}/dataset" , tags=['datasets'])
app.include_router(audit_router,prefix=f"{version_prefix}/audit" , tags=['audit'])
app.include_router(masking_router,prefix=f"{version_prefix}/masking", tags=['masking'])