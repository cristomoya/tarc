# Tests de las funciones puras de doctrina.py (no necesitan BD ni OpenAI):  cd api && pytest tests/
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from doctrina import clasificar_sentido, estadisticas


@pytest.mark.parametrize("sentido, clase", [
    ("Estimación", "estimada"),
    ("Estimación parcial", "estimada"),
    ("Estimación Parcial", "estimada"),
    ("ESTIMACION", "estimada"),
    ("Desestimación", "desestimada"),
    ("Desestimación.", "desestimada"),
    ("Inadmisión", "inadmitida"),
    ("Inadmisibilidad", "inadmitida"),
    ("Extemporaneidad.", "inadmitida"),
    ("Desistimiento", "otro"),
    ("Archivo", "otro"),
    ("", "otro"),
    (None, "otro"),
])
def test_clasificar_sentido(sentido, clase):
    assert clasificar_sentido(sentido) == clase


def test_desestimacion_no_cuenta_como_estimacion():
    stats = estadisticas([{"id": 1, "sentido": "Desestimación"}, {"id": 2, "sentido": "Desestimación"}])
    assert stats["estimadas"] == 0
    assert stats["ratio_estimacion"] == 0


def test_cada_resolucion_cuenta_una_vez():
    rows = [
        {"id": 1, "sentido": "Estimación"},
        {"id": 1, "sentido": "Estimación"},     # otro fragmento de la misma resolución
        {"id": 1, "sentido": "Estimación"},
        {"id": 2, "sentido": "Desestimación"},
        {"id": 3, "sentido": "Inadmisión"},
    ]
    assert estadisticas(rows) == {
        "total": 3, "estimadas": 1, "desestimadas": 1, "inadmitidas": 1, "ratio_estimacion": 0.5,
    }


def test_sin_resoluciones_de_fondo_no_hay_ratio():
    assert estadisticas([{"id": 1, "sentido": "Inadmisión"}])["ratio_estimacion"] is None
    assert estadisticas([])["total"] == 0
