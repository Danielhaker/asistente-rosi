# Asistente Rosa Molas

## Suscribete en Youtube a: @MisteryMC-m1necraft

## Descripción
Un asistente de IA inteligente basado en la API de Gemini, con capacidades avanzadas de:
+ Conversación interactiva
+ Reconocimiento de voz
+ Texto a voz

## Requisitos
+ Python 3.8+
+ Dependencias en `requirements.txt`

## Instalación

1. Clonar repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd asistente
```

2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar API Key de Gemini
```bash
export GEMINI_API_KEY='tu_api_key_aqui'
```

## Ejecución
```bash
flask run
```

## Características
+ Chat con IA basado en Gemini
+ Reconocimiento de voz en español
+ Conversión de texto a voz
+ Diseño web responsivo

## Configuración
+ Reemplazar `tu_api_key_aqui` con tu API key de Gemini
+ Personalizar `logo.png` en carpeta `static`

## Solución de Problemas
+ Asegúrate de tener todas las dependencias instaladas
+ Verifica que la API Key de Gemini sea válida
+ Comprueba los permisos de audio para reconocimiento de voz
