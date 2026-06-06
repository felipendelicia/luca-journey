---
title: "Automatización: Fechas, esperas y agendado"
order: 1005
---

> 🎯 **Meta:** manejar **fechas y tiempos** para que tus tareas corran cuando tienen que correr.

---

Muchas automatizaciones son sobre **cuándo**: "hacé backup cada 6 horas", "mandá el reporte los lunes", "no corras los fines de semana". Para eso está el módulo **`datetime`**.

## Fechas y momentos

```python
from datetime import date, datetime, timedelta

hoy = date.today()
ahora = datetime.now()
print(hoy)            # 2024-03-09
print(ahora.hour)     # la hora actual
```

## Restar fechas: `timedelta`

Restar dos fechas te da un `timedelta`, la **diferencia** de tiempo:

```python
inicio = date(2024, 1, 1)
fin = date(2024, 1, 8)
diferencia = fin - inicio
print(diferencia.days)        # 7
```

Y sumando un `timedelta` te movés en el tiempo:

```python
ahora = datetime(2024, 1, 1, 10, 0)
en_15 = ahora + timedelta(minutes=15)   # 10:15
manana = ahora + timedelta(days=1)
```

## Decisiones según el tiempo

Con eso ya podés agendar. `weekday()` da el día (lunes=0 … domingo=6):

```python
def es_fin_de_semana(d):
    return d.weekday() >= 5     # sábado(5) o domingo(6)

def toca_correr(ultima, ahora, cada_horas):
    pasaron = (ahora - ultima).total_seconds() / 3600
    return pasaron >= cada_horas
```

> 💡 Para esperar de verdad está `time.sleep(segundos)`, y para agendar tareas reales hay librerías como `schedule` o el `cron` de Linux. Acá practicás la **lógica** que decide si una tarea toca o no, que es el corazón de cualquier agendador.

## Formatear fechas

`strftime` convierte una fecha en el texto que quieras:

```python
from datetime import date
print(date(2024, 3, 9).strftime("%Y-%m-%d"))   # "2024-03-09"
```

⏰ La **Capitana Acerola** te espera para construir un agendador de tareas.
