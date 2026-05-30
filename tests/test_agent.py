import pytest
from agente_ucv.agent import explicar_concepto, calcular_promedio

# --- Pruebas para explicar_concepto ---

def test_explicar_concepto_exitoso():
    resultado = explicar_concepto("api")
    assert resultado["status"] == "success"
    assert "comunicación" in resultado["explicacion"].lower()

def test_explicar_concepto_nuevo_reto():
    resultado = explicar_concepto("devops")
    assert resultado["status"] == "success"
    assert "operaciones de ti" in resultado["explicacion"].lower()

def test_explicar_concepto_no_existente():
    resultado = explicar_concepto("inexistente")
    assert resultado["status"] == "not_found"

def test_explicar_concepto_validacion_entrada():
    resultado = explicar_concepto("")
    assert resultado["status"] == "error"


# --- Pruebas para calcular_promedio ---

def test_calcular_promedio_exitoso():
    resultado = calcular_promedio("12, 16, 20")
    assert resultado["status"] == "success"
    # Solución al Code Smell de SonarQube: Se usa pytest.approx para comparar decimales
    assert resultado["promedio"] == pytest.approx(16.0)
    assert resultado["cantidad_notas"] == 3

def test_calcular_promedio_con_decimales():
    resultado = calcular_promedio("11.5, 14.5")
    assert resultado["status"] == "success"
    # Solución al Code Smell de SonarQube: Se usa pytest.approx para comparar decimales
    assert resultado["promedio"] == pytest.approx(13.0)

def test_calcular_promedio_fuera_de_rango():
    resultado = calcular_promedio("21, 15, -5")
    assert resultado["status"] == "error"
    assert "fuera del rango" in resultado["mensaje"]

def test_calcular_promedio_error_formato():
    resultado = calcular_promedio("diez, once, doce")
    assert resultado["status"] == "error"
    assert "Error de formato" in resultado["mensaje"]