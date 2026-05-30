import logging
from google.adk.agents.llm_agent import Agent

# Configurar logs para auditoría y depuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgenteUCV")

def explicar_concepto(concepto: str) -> dict:
    """
    Devuelve la explicación de un concepto técnico de IA o desarrollo de software.
    """
    # Validación de Entrada (Paso del Reto)
    if not concepto or not isinstance(concepto, str):
        return {
            "status": "error",
            "explicacion": "Entrada inválida. Debe proveer un texto no vacío."
        }
    
    # Base de datos de conceptos (Base + 5 Nuevos conceptos)
    conceptos = {
        # Conceptos Base
        "api": "Una API (Interfaz de Programación de Aplicaciones) permite la comunicación y transferencia de datos entre sistemas de software de manera segura.",
        "algoritmo": "Un algoritmo es una secuencia lógica y finita de pasos diseñados para resolver un problema o realizar una tarea específica.",
        "base de datos": "Una base de datos es un sistema estructurado para almacenar, organizar, gestionar y recuperar información eficientemente.",
        
        # 5 Nuevos Conceptos (Reto)
        "devops": "Metodología que integra el desarrollo de software (Dev) y las operaciones de TI (Ops) para acelerar el ciclo de vida de entrega de software con alta calidad.",
        "docker": "Herramienta que permite empaquetar una aplicación y sus dependencias en un contenedor aislado, garantizando que funcione en cualquier entorno.",
        "git": "Sistema de control de versiones distribuido diseñado para rastrear cambios en el código fuente durante el desarrollo de software.",
        "ci/cd": "Prácticas de Integración Continua (CI) y Despliegue Continuo (CD) que automatizan la construcción, prueba y liberación de aplicaciones.",
        "agente de ia": "Entidad autónoma con capacidad para percibir su entorno mediante sensores, tomar decisiones razonadas empleando modelos de lenguaje (LLM) y ejecutar acciones a través de herramientas."
    }
    
    concepto_limpio = concepto.lower().strip()
    
    if concepto_limpio in conceptos:
        return {
            "status": "success",
            "explicacion": conceptos[concepto_limpio]
        }
    
    return {
        "status": "not_found",
        "explicacion": f"El concepto '{concepto}' no está registrado en el diccionario académico del Agente UCV."
    }


def calcular_promedio(notas: str) -> dict:
    """
    Calcula el promedio de una lista de notas separadas por comas.
    Las notas deben estar en el rango de 0 a 20.
    Ejemplo de entrada: "14, 15, 18, 11"
    """
    # Validación de Entrada (Paso del Reto)
    if not notas or not isinstance(notas, str):
        return {
            "status": "error",
            "mensaje": "Formato de entrada inválido. Debe proporcionar una cadena de texto."
        }
    
    try:
        # Extraer elementos, limpiar espacios y convertir a decimales
        lista_notas = [float(n.strip()) for n in notas.split(",") if n.strip()]
        
        if not lista_notas:
            return {
                "status": "error",
                "mensaje": "No se encontraron notas válidas en la entrada."
            }
        
        # Validar rangos escolares/universitarios tradicionales en Perú (0 a 20)
        for nota in lista_notas:
            if nota < 0 or nota > 20:
                return {
                    "status": "error",
                    "mensaje": f"La nota {nota} está fuera del rango permitido (0-20)."
                }
        
        promedio = sum(lista_notas) / len(lista_notas)
        logger.info(f"Cálculo exitoso para las notas: {lista_notas}. Promedio: {promedio:.2f}")
        
        return {
            "status": "success",
            "cantidad_notas": len(lista_notas),
            "promedio": round(promedio, 2)
        }
        
    except ValueError:
        return {
            "status": "error",
            "mensaje": "Error de formato. Asegúrese de separar las notas exclusivamente con comas y usar solo números."
        }


# Instancia del agente con Google ADK
root_agent = Agent(
    model="gemini-flash-latest",
    name="agente_ucv",
    description="Agente académico inteligente de la UCV",
    instruction="""
    Eres un asistente académico inteligente de la Universidad César Vallejo (UCV).
    Tu misión es guiar de manera clara y amigable a los alumnos. 
    Responde siempre en español. Usa un tono pedagógico.
    Tienes acceso a herramientas para definir conceptos de TI y calcular promedios de notas.
    """,
    tools=[explicar_concepto, calcular_promedio],
)