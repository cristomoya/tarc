# doctrina.py — clasificación del sentido de las resoluciones y estadísticas de estimación
# (funciones puras, sin BD ni OpenAI, para poder probarlas sin el stack)
import unicodedata
from collections.abc import Iterable, Mapping


def _normalizar(texto: str) -> str:
    sin_acentos = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in sin_acentos if not unicodedata.combining(c)).strip().lower()


def clasificar_sentido(sentido: str | None) -> str:
    """'estimada' | 'desestimada' | 'inadmitida' | 'otro'.

    Ojo: "desestimación" contiene "estimación", así que se compara por el comienzo del texto,
    nunca con `in`.
    """
    s = _normalizar(sentido or "")
    if s.startswith("estimaci"):          # Estimación, Estimación parcial / Parcial
        return "estimada"
    if s.startswith("desestimaci"):
        return "desestimada"
    if s.startswith(("inadmi", "extemporane")):
        return "inadmitida"
    return "otro"                         # Desistimiento, Archivo, Acumulación…


def estadisticas(rows: Iterable[Mapping]) -> dict:
    """Cuenta cada resolución una sola vez aunque aparezcan varios de sus fragmentos.

    `rows` necesita las claves `id` (de la resolución) y `sentido`. El ratio de estimación se
    calcula solo sobre las resoluciones que entran en el fondo (estimadas + desestimadas).
    """
    sentidos: dict = {}
    for r in rows:
        sentidos.setdefault(r["id"], r.get("sentido"))
    clases = [clasificar_sentido(s) for s in sentidos.values()]
    estimadas = clases.count("estimada")
    desestimadas = clases.count("desestimada")
    fondo = estimadas + desestimadas
    return {
        "total": len(clases),
        "estimadas": estimadas,
        "desestimadas": desestimadas,
        "inadmitidas": clases.count("inadmitida"),
        "ratio_estimacion": round(estimadas / fondo, 3) if fondo else None,
    }
