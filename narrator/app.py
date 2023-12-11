from fastapi import FastAPI

app = FastAPI(debug=True)

from narrator.api import api
