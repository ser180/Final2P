from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from models.models import modelPelicula, TokenData
from middlewares import BearerJWT
from tokenGen import createToken


app = FastAPI(
    title='API de Películas',
    description='Examen Final - Sergio Ramón Olmedo Soto',
    version='1.0.1'
)

# Diccionario como base de datos provisional
peliculas = {}

@app.get('/', tags=['Inicio'])
def main():
    return {"mensaje": "Examen Final Segundo Parcial - API de Películas"}

# Guardar película
@app.post("/peliculas/", tags=['Operaciones CRUD'])
def agregar_pelicula(pelicula: modelPelicula):
    try:
        if pelicula.Titulo in peliculas:
            return JSONResponse(status_code=400, content={"mensaje": "La película ya está registrada."})
        peliculas[pelicula.Titulo] = pelicula
        return JSONResponse(status_code=201, content={"mensaje": f"Película '{pelicula.Titulo}' registrada exitosamente.",
                                                      "pelicula": jsonable_encoder(pelicula)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"mensaje": "Error al registrar la película.", "Excepcion": str(e)})

# Consultar todas las películas
@app.get("/peliculas", tags=['Operaciones CRUD'])
def consultar_todas():
    return JSONResponse(content=jsonable_encoder(list(peliculas.values())))

# Consultar una película
@app.get("/peliculas/{titulo}", tags=['Operaciones CRUD'])
def consultar_pelicula(titulo: str):
    try:
        pelicula = peliculas.get(titulo)
        if not pelicula:
            return JSONResponse(status_code=404, content={"mensaje": f"La película '{titulo}' no fue encontrada."})
        return JSONResponse(content={"mensaje": f"Película '{titulo}' encontrada.", "pelicula": jsonable_encoder(pelicula)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"mensaje": "Error al buscar la película.", "Excepcion": str(e)})

# Editar película
@app.put("/peliculas/{titulo}", tags=['Operaciones CRUD'])
def editar_pelicula(titulo: str, datos_actualizados: modelPelicula):
    try:
        if titulo not in peliculas:
            return JSONResponse(status_code=404, content={"mensaje": f"La película '{titulo}' no fue encontrada para editar."})
        peliculas[titulo] = datos_actualizados
        return JSONResponse(content={"mensaje": f"Película '{titulo}' actualizada correctamente.", "pelicula": jsonable_encoder(datos_actualizados)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"mensaje": "Error al actualizar la película.", "Excepcion": str(e)})

# Eliminar película (Protegido con JWT)
@app.delete("/peliculas/{titulo}", dependencies=[Depends(BearerJWT())], tags=['Operaciones CRUD'])
def eliminar_pelicula(titulo: str):
    try:
        if titulo not in peliculas:
            return JSONResponse(status_code=404, content={"mensaje": f"La película '{titulo}' no fue encontrada para eliminar."})
        del peliculas[titulo]
        return JSONResponse(content={"mensaje": f"La película '{titulo}' fue eliminada correctamente."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"mensaje": "Error al eliminar la película.", "Excepcion": str(e)})


@app.post('/token', tags=['Autenticación'])
def generar_token(datos: TokenData):
    try:
        token = createToken(datos.model_dump())
        return JSONResponse(content={"token": token})
    except Exception as e:
        return JSONResponse(status_code=500, content={"mensaje": "Error al generar token", "Excepcion": str(e)})
