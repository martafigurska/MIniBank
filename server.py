from fastapi import FastAPI, HTTPException
from connection import setup_database
from classes.handler import Handler

# app = FastAPI()

branch_conns = setup_database()
handler = Handler(branch_conns=branch_conns)
