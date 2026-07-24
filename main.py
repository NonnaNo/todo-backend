# My branch
# My first GitHub project
import uvicorn
from fastapi import FastAPI, Body
app= FastAPI()
from pydantic_settings import BaseSettings
from resources import EntryManager, Entry

class Settings(BaseSettings):
    data_folder: str='/tmp/'
settings = Settings()
print(settings.data_folder)



@app.get('/')
async def hello_world():
    return {'Hello': 'Nonna'}


@app.get("/about")
async def about():
    return {"name": "Nonna", "skill": "Python"}


@app.get('/api/entries/')
async def get_entries():
    e_manager = EntryManager(settings.data_folder)
    e_manager.load()
    result = []
    for entry in e_manager.entries:
        result.append(entry.json())
    return result


@app.get('/api/get_data_folder/')
async def get_data_folder():
    return {'folder': settings.data_folder}

@app.post('/api/save_entries/')
async def save_entries(data: list = Body(...)):
    entry_manager = EntryManager(settings.data_folder)
    for item in data:
        entry = Entry.from_json(item)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://wexler.io"  # адрес на котором работает фронт-энд
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # Список разрешенных доменов
    allow_credentials=True,   # Разрешить Cookies и Headers
    allow_methods=["*"],      # Разрешить все HTTP методы
    allow_headers=["*"],      # Разрешить все хедеры
)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)