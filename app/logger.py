from loguru import logger
import sys
from datetime import datetime

logger.remove()  

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
)

logger.add(
    f"logs/api_{datetime.now().strftime('%Y%m%d')}.log",
    rotation="00:00",       
    retention="7 days",    
    compression="zip",     
    level="INFO",
    encoding="utf-8"
)

__all__ = ["logger"]
