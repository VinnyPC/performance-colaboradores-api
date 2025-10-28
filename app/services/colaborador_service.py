from app.repositories import colaborador_repository
from loguru import logger

from app.schemas.colaborador_schema import ColaboradorInputSchema

def listar_colaboradores():
    logger.info("Buscando todos os colaboradores...")
    colaboradores = colaborador_repository.listar_todos()
    logger.success(f"{len(colaboradores)} colaboradores encontrados.")
    return colaboradores

def criar_colaborador(dados):
    logger.info("Criando novo colaborador...")

    schema = ColaboradorInputSchema()
    dados_validados = schema.load(dados)  

    colaborador = colaborador_repository.criar(dados_validados)
    logger.success(f"Colaborador {colaborador['nome']} criado com sucesso.")
    return colaborador


def atualizar_colaborador(colaborador_id, dados):
    logger.info(f"Atualizando colaborador ID {colaborador_id}...")

    schema = ColaboradorInputSchema(partial=True)  
    dados_validados = schema.load(dados)

    colaborador_atualizado = colaborador_repository.atualizar(colaborador_id, dados_validados)
    logger.success(f"Colaborador {colaborador_id} atualizado com sucesso.")
    return colaborador_atualizado


def deletar_colaborador(colaborador_id):
    logger.info(f"Deletando colaborador ID {colaborador_id}...")
    colaborador_repository.deletar(colaborador_id)
    logger.success(f"Colaborador {colaborador_id} deletado com sucesso.")