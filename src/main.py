import json
import os
import requests
import pandas as pd
import ssl

# Solución SSL para Mac
ssl._create_default_https_context = ssl._create_unverified_context

# --- CONFIGURACIÓN DE CURADURÍA ---
BLACKLIST = ["microsoft", "meta", "palantir", "azure", "facebook", "llama"] # Estos se borran totalmente
LOCAL_PROVIDERS = ["mistral", "deepseek", "google", "meta", "alibaba", "01.ai", "mistral ai"] # Modelos que suelen tener versiones Open Weights

def filtrar_blacklist(ia):
    proveedor = str(ia.get("proveedor", "")).lower()
    modelo = str(ia.get("modelo", "")).lower()
    for banned in BLACKLIST:
        if banned in proveedor or banned in modelo:
            return False
    return True

def es_modelo_local(ia):
    # Lógica para determinar si el modelo es "Soberano/Local"
    # En un entorno real, esto se cruza con una base de datos de HuggingFace
    proveedor = str(ia.get("proveedor", "")).lower()
    modelo = str(ia.get("modelo", "")).lower()
    
    # Definimos palabras clave que indican que el modelo es abierto/local
    keywords_local = ["llama", "mistral", "deepseek", "qwen", "gemma", "phi", "mixtral"]
    
    if any(key in modelo for key in keywords_local) or any(prov in proveedor for prov in LOCAL_PROVIDERS):
        return True
    return False

def obtener_datos_reales():
    print("🌐 Conectando con fuente de datos reales...")
    url_datos = "https://raw.githubusercontent.com/lucidrains/chat-arena-data/main/leaderboard.csv" 
    try:
        df = pd.read_csv(url_datos)
        datos_procesados = []
        for index, row in df.iterrows():
            datos_procesados.append({
                "modelo": row.get("model", "Desconocido"),
                "proveedor": row.get("organization", "Desconocido"),
                "score_coding": row.get("elo", 0)
            })
        return datos_procesados
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def generar_rankings_duales():
    datos_brutos = obtener_datos_reales()
    
    if datos_brutos is None:
        print("⚠️ Error al obtener datos. Usando respaldo...")
        # Datos de respaldo simplificados para el ejemplo
        datos_brutos = [
            {"modelo": "Claude 3.5 Sonnet", "proveedor": "Anthropic", "score_coding": 1285},
            {"modelo": "GPT-4o", "proveedor": "OpenAI", "score_coding": 1270},
            {"modelo": "DeepSeek Coder V2", "proveedor": "DeepSeek", "score_coding": 1255},
            {"modelo": "Llama 3 70B", "proveedor": "Meta", "score_coding": 1210},
            {"modelo": "Mistral Large 2", "proveedor": "Mistral", "score_coding": 1220},
        ]

    # 1. RANKING GLOBAL (Todos menos la Blacklist)
    global_list = [ia for ia in datos_brutos if filtrar_blacklist(ia)]
    for ia in global_list: ia["estado"] = "Aprobado"

    # 2. RANKING LOCAL (Solo los que son Open Weights y NO están en Blacklist)
    local_list = [ia for ia in datos_brutos if filtrar_blacklist(ia) and es_modelo_local(ia)]
    for ia in local_list: ia["estado"] = "Soberano"

    # GUARDAR ARCHIVOS EN /data
    with open(os.path.join("..", "data", "ranking_global.json"), "w", encoding="utf-8") as f:
        json.dump(global_list, f, indent=4, ensure_ascii=False)
    
    with open(os.path.join("..", "data", "ranking_local.json"), "w", encoding="utf-8") as f:
        json.dump(local_list, f, indent=4, ensure_ascii=False)
    
    print(f"🚀 EXITO: Rankings generados. Global: {len(global_list)} | Local: {len(local_list)}")

if __name__ == "__main__":
    generar_rankings_duales()