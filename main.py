import json
from fastapi import FastAPI, HTTPException

from models import Composer, Piece

app = FastAPI()

with open("composers.json", "r") as f:
    composers_list: list[dict] = json.load(f)

with open("pieces.json", "r") as f:
    piece_list: list[dict] = json.load(f)

composers = [Composer(**composer) for composer in composers_list]
pieces = [Piece(**piece) for piece in piece_list]

# Composers
@app.get("/composers")
async def list_composers() -> list[Composer]:
    return composers

@app.post("/composers")
async def create_composer(composer: Composer) -> Composer:
    for existing_composer in composers:
        if existing_composer.composer_id == composer.composer_id:
            raise HTTPException(status_code=400, detail="Composer already exists")
    composers.append(composer)
    return composer

@app.put("/composers/{composer_id}")
async def update_composer(composer_id: int, composer: Composer) -> Composer:
    for existing_composer in composers:
        if existing_composer.composer_id == composer_id:
            existing_composer.name = composer.name
            existing_composer.home_country = composer.home_country
            return composer
    raise HTTPException(status_code=404, detail="Composer not found")

@app.delete("/composers/{composer_id}")
async def delete_composer(composer_id: int):
    for existing_composer in composers:
        if existing_composer.composer_id == composer_id:
            composers.remove(existing_composer)
            return "Composer deleted successfully"
    raise HTTPException(status_code=404, detail="Composer not found")

# Pieces

@app.get("/pieces")
async def list_pieces() -> list[Piece]:
    return list(pieces)

@app.post("/pieces")
async def create_piece(piece: Piece) -> Piece:
    for existing_piece in pieces:
        if existing_piece.name == piece.name:
            raise HTTPException(status_code=400, detail="Piece already exists")
    pieces.append(piece)
    return piece

@app.put("/pieces/{piece_name}")
async def update_piece(piece_name: str, piece: Piece) -> Piece:
    for existing_piece in pieces:
        if existing_piece.name == piece_name:
            existing_piece.alt_name = piece.alt_name
            existing_piece.difficulty = piece.difficulty
            existing_piece.composer_id = piece.composer_id
            return existing_piece
    raise HTTPException(status_code=400, detail="Piece does not exist")

@app.delete("/pieces/{piece_name}")
async def delete_pieces(piece_name: str):
    for existing_piece in pieces:
        if existing_piece.name == piece_name:
            pieces.remove(existing_piece)
            return "Piece deleted successfully"
    raise HTTPException(status_code=404, detail="Piece not found")