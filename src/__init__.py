from src.errors import register_error_handlers
from fastapi import FastAPI
from src.auth.routes import auth_router
from src.categories.routes import categories_router
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