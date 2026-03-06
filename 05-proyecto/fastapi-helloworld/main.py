from datetime import datetime
from fastapi import FastAPI

app = FastAPI(
    title="Hello World API",
    version="1.0.0",
    description="API minimalista con endpoints básicos: hola mundo y fecha actual",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


@app.get(
    "/",
    summary="Hello World",
    tags=["Hello"]
)
async def hello_world() -> dict[str, str]:
    """
    Endpoint básico que devuelve un mensaje de saludo.
    
    Returns:
        dict: Mensaje de saludo en formato JSON
    """
    return {"message": "Hello World"}


@app.get(
    "/date",
    summary="Fecha actual",
    tags=["Date"]
)
async def get_current_date() -> dict[str, str]:
    """
    Devuelve la fecha y hora actual en formato ISO 8601.
    
    Returns:
        dict: Fecha actual en formato ISO 8601
    """
    current_date = datetime.now().isoformat()
    return {"current_date": current_date}


@app.get(
    "/date/{texto}",
    summary="Fecha con parámetro",
    tags=["Date"]
)
async def get_date_with_text(texto: str) -> dict[str, str]:
    """
    Concatena un texto recibido por URL con la fecha actual.
    
    Args:
        texto: Texto a concatenar con la fecha actual (path parameter)
    
    Returns:
        dict: Mensaje con el texto concatenado a la fecha actual en formato ISO 8601
    
    Example:
        GET /date/hola devuelve {"message": "hola - 2026-01-30T12:34:56.789123"}
    """
    current_date = datetime.now().isoformat()
    message = f"{texto} - {current_date}"
    return {"message": message}
