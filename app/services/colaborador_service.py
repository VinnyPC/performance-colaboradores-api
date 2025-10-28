from app.repositories import colaborador_repository
from app.schemas.colaborador_schema import ColaboradorInputSchema
from loguru import logger


def listar_colaboradores():
    logger.info("Buscando todos os colaboradores...")
    colaboradores = colaborador_repository.listar_todos()
    if not colaboradores:
        logger.warning("Nenhum colaborador encontrado.")
        return {"mensagem": "Nenhum colaborador encontrado."}, 404
    logger.success(f"{len(colaboradores)} colaboradores encontrados.")
    return colaboradores


def criar_colaborador(dados):
    logger.info("Criando novo colaborador...")
    schema = ColaboradorInputSchema()
    dados_validados = schema.load(dados)

    try:
        colaborador = colaborador_repository.criar(dados_validados)
        logger.success(f"Colaborador {colaborador['nome']} criado com sucesso.")
        return colaborador
    except ValueError as e:
        logger.warning(str(e))
        raise


def atualizar_colaborador(colaborador_id, dados):
    logger.info(f"Atualizando colaborador ID {colaborador_id}...")
    schema = ColaboradorInputSchema(partial=True)
    dados_validados = schema.load(dados)

    try:
        colaborador_atualizado = colaborador_repository.atualizar(colaborador_id, dados_validados)
        logger.success(f"Colaborador {colaborador_id} atualizado com sucesso.")
        return colaborador_atualizado
    except ValueError as e:
        logger.warning(str(e))
        raise


def deletar_colaborador(colaborador_id):
    logger.info(f"Deletando colaborador ID {colaborador_id}...")
    try:
        colaborador_repository.deletar(colaborador_id)
        logger.success(f"Colaborador {colaborador_id} deletado com sucesso.")
    except ValueError as e:
        logger.warning(str(e))
        raise
