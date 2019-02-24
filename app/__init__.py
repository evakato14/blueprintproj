from flask import Flask
from app.views import app

app.config.update(
    DEBUG=True
)
