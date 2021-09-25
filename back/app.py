import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body

from main import recommend

load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/search")
async def search(data=Body(...)):
    response = requests.post(
        f"http://api.openweathermap.org/data/2.5/forecast?q={data['city']}&appid=243ed62ca2a819732a1d89b2d9b5b8a5"
    )
    weather = response.json()

    age = datetime.now().year - data["age"]
    gender = {"male": 1, "female": 2}.get(data["gender"], 0)
    city = {
        "Seoul": 3,
        "Busan": 2,
        "Incheon": 1,
        "Daegu": 2,
        "Daejeon": 6,
        "Gwangju": 4,
        "Ulsan": 2,
        "Gyeonggi-do": 1,
        "Gangwon-do": 0,
        "Gyeongsangnam-do": 2,
        "Gyeongsangbuk-do": 2,
        "Jeollanam-do": 4,
        "Jeollabuk-do": 4,
        "Chungcheongnam-do": 6,
        "Chungcheongbuk-do": 6,
        "Jeju-do": 5,
    }.get(data["city"])

    condition = {"공연지역명": city, "연령": age, "성별": gender, "날씨": weather}
    print(condition)

    return recommend(condition)
