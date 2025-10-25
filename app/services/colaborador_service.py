from app.repositories import colaborador_repository
from loguru import logger

def listar_colaboradores():
    logger.info("Buscando todos os colaboradores...")
    colaboradores = colaborador_repository.listar_todos()
    logger.success(f"{len(colaboradores)} colaboradores encontrados.")
    return colaboradores