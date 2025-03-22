from datetime import datetime, timedelta
import locale

# Establecer la configuración regional a español de España
locale.setlocale(locale.LC_TIME, '')

# Obtener la fecha y hora actuales en España (UTC+1 o UTC+2 en horario de verano)
current_datetime = datetime.utcnow() + timedelta(hours=1)

# Formatear la fecha y la hora según la configuración regional
time_prompt = f"""
La fecha actual es: El {current_datetime.strftime('%A')} {current_datetime.day} del {current_datetime.month} de {current_datetime.year} y la hora es: {current_datetime.hour}:{current_datetime.minute}
"""
