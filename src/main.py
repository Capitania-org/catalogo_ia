import json
import os

# --- CONFIGURACIÓN DE CURADURÍA ---
# Cualquier empresa que aparezca aquí será ELIMINADA automáticamente
BLACKLIST = [
    "microsoft", 
    "meta", 
    "palantir", 
    "azure", 
    "facebook", 
    "llama"
]

def filtrar_ia(ia):
    """
    Verifica si la IA debe ser vetada.
    Retorna True si la IA es APROBADA, False si debe ser ELIMINADA.
    """
    proveedor = ia["proveedor"].lower()
    modelo = ia["modelo"].lower()
    
    for banned in BLACKLIST:
        if banned in proveedor or banned in modelo:
            return False # Está vetado, eliminar
    return True # Está aprobado

def generar_catalogo_curado():
    # Simulamos la recepción de datos de una fuente externa (LMSYS / Benchmarks)
    datos_brutos = [
        {"modelo": "Claude 3.5 Sonnet", "proveedor": "Anthropic", "score_coding": 98},
        {"modelo": "GPT-4o", "proveedor": "OpenAI", "score_coding": 96},
        {"modelo": "DeepSeek Coder V2", "proveedor": "DeepSeek", "score_coding": 94},
        {"modelo": "Llama 3", "proveedor": "Meta", "score_coding": 90}, 
        {"modelo": "Copilot", "proveedor": "Microsoft", "score_coding": 88},
        {"modelo": "AIP", "proveedor": "Palantir", "score_coding": 85},
    ]

    # AQUÍ OCURRE LA MAGIA: Filtramos la lista
    # Solo guardamos la IA si la función 'filtrar_ia' devuelve True
    datos_filtrados = [ia for ia in datos_brutos if filtrar_ia(ia)]
    
    # Añadimos el estado "Aprobado" a los que sobrevivieron al filtro
    for ia in datos_filtrados:
        ia["estado"] = "Aprobado"

    # Ruta del archivo en la carpeta data
    ruta_archivo = os.path.join("..", "data", "ranking.json")

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(datos_filtrados, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Catálogo curado. {len(datos_filtrados)} IAs aprobadas. Archivo actualizado.")

if __name__ == "__main__":
    generar_catalogo_curado()