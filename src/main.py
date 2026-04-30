import json
import os

def generar_datos_simulados():
    # Simulamos una lista de IAs con métricas técnicas (sin hype)
    ranking_ias = [
        {"modelo": "Claude 3.5 Sonnet", "proveedor": "Anthropic", "score_coding": 98, "estado": "Aprobado"},
        {"modelo": "GPT-4o", "proveedor": "OpenAI", "score_coding": 96, "estado": "Aprobado"},
        {"modelo": "DeepSeek Coder V2", "proveedor": "DeepSeek", "score_coding": 94, "estado": "Aprobado"},
        {"modelo": "Llama 3", "proveedor": "Meta", "score_coding": 90, "estado": "Vetado"}, 
        {"modelo": "Copilot", "proveedor": "Microsoft", "score_coding": 88, "estado": "Vetado"},
    ]

    # Definimos la ruta donde se guardará el archivo
    # Usamos ".." para salir de la carpeta 'src' y entrar en 'data'
    ruta_archivo = os.path.join("..", "data", "ranking.json")

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(ranking_ias, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Archivo generado exitosamente en: {ruta_archivo}")

if __name__ == "__main__":
    generar_datos_simulados()

