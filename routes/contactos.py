from fastapi import FastAPI,HTTPException, Depends,status,APIRouter, Depends
router = APIRouter()

@router.get('/get/contactos',tags=["Contacos"])
async def contactos():
    return 'hola'