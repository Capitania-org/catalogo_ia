import json
import os
import requests
import pandas as pd
import ssl

# Solución SSL para Mac
ssl._create_default_https_context = ssl._create_unverified_context

# --- CONFIGURACIÓN DE CURADURÍA ---
BLACKLIST = ["microsoft", "meta", "palantir", "azure", "facebook", "llama"]
DIMENSIONES = ["coding", "reasoning", "multimodal", "agency"]

def filtrar_blacklist(ia):
    proveedor = str(ia.get("proveedor", "")).lower()
    modelo = str(ia.get("modelo", "")).lower()
    for banned in BLACKLIST:
        if banned in proveedor or banned in modelo:
            return False
    return True

def es_modelo_local(ia):
    modelo = str(ia.get("modelo", "")).lower()
    proveedor = str(ia.get("proveedor", "")).lower()
    keywords_local = ["llama", "mistral", "deepseek", "qwen", "gemma", "phi", "mixtral"]
    return any(key in modelo for key in keywords_local) or "deepseek" in proveedor or "mistral" in proveedor

def obtener_datos_maestros():
    """
    Simula la extracción de múltiples dimensiones. 
    En la versión final, aquí conectamos cada dimensión a su respectivo benchmark.
    """
    print("🌐 Extrayendo datos multidimensionales...")
    # Dataset maestro simulado basado en tendencias reales de LMSYS/LiveCodeBench
    # Formato: { "modelo": ..., "proveedor": ..., "scores": {"coding": X, "reasoning": Y, ...} }
    datos_maestros = [
        {"modelo": "Claude 3.5 Sonnet", "proveedor": "Anthropic", "scores": {"coding": 1285, "reasoning": 1270, "multimodal": 1260, "agency": 1240}},
        {"modelo": "GPT-4o", "proveedor": "OpenAI", "scores": {"coding": 1270, "reasoning": 1280, "multimodal": 1290, "agency": 1260}},
        {"modelo": "DeepSeek Coder V2", "proveedor": "DeepSeek", "scores": {"coding": 1255, "reasoning": 1210, "multimodal": 1100, "agency": 1150}},
        {"modelo": "Llama 3 70B", "proveedor": "Meta", "scores": {"coding": 1210, "reasoning": 1240, "multimodal": 1000, "agency": 1100}},
        {"modelo": "Mistral Large 2", "proveedor": "Mistral", "scores": {"coding": 1220, "reasoning": 1230, "multimodal": 1050, "agency": 1120}},
        {"modelo": "Gemma 2 27B", "proveedor": "Google", "scores": {"coding": 1180, "reasoning": 1200, "multimodal": 1150, "agency": 1050}},
    ]
    return datos_// la data real se procesaría aquí la misma forma que antes
    return datos_maestros

def generar_hub_tecnico():
    datos_maestros = obtener_datos_maestros()
    
    for dim in DIMENSIONES:
        global_list = []
        local_list = []
        
        for ia in datos_maestros:
            # 1. Aplicar Blacklist
            if not filtrar_blacklist(ia):
                continue
            
            # Creamos el objeto para la tabla
            entrada = {
                "modelo": ia["modelo"],
                "proveedor": ia["proveedor"],
                "score": ia["scores"][dim],
                "estado": "Auditado" if not es_modelo_local(ia) else "Soberano"
            }
            
            # 2. Clasificar en Global o Local
            global_list.append(entrada)
            if es_modelo_local(ia):
                local_list.append(entrada)
        
        # Ordenar por score descendente
        global_list.sort(key=lambda x: x["score"], reverse=True)
        local_list.sort(key=lambda x: x["score"], reverse=True)
        
        # GUARDAR ARCHIVOS DINÁMICOS
        with open(os.path.join("..", "data", f"global_{dim}.json"), "w", encoding="utf-8") as f:
            json.dump(global_list, f, indent=4, ensure_ascii=False)
        
        with open(os.path.join("..", "data", f"local_{dim}.json"), "w", encoding="utf-8") as f:
            json.dump(local_list, f, indent=4, ensure_ascii=False)
            
    print(f"🚀 HUB ACTUALIZADO: {len(DIMENSIONES)} dimensiones procesadas (Global y Local).")

if __name__ == "__main__":
    generar_hub_tecnico()