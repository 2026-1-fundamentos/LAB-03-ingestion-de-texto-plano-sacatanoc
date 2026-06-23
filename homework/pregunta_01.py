"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def pregunta_01():
  """
  Construya y retorne un dataframe de Pandas a partir del archivo
  'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

  - El dataframe tiene la misma estructura que el archivo original.
  - Los nombres de las columnas deben ser en minusculas, reemplazando los
    espacios por guiones bajos.
  - Las palabras clave deben estar separadas por coma y con un solo
    espacio entre palabra y palabra.


    """

  with open('files/input/clusters_report.txt', encoding='utf-8') as f:
    lines = f.readlines()

  records = []
  current = None
  for raw in lines:
      line = raw.rstrip('\r\n')
      if not line.strip() or re.match(r'^-+$', line.strip()):
          continue
      if 'Cluster' in line or re.match(r'^\s*palabras clave', line):
          continue  # saltar encabezado

      # Línea nueva de cluster: empieza con número + espacios + número + espacios + porcentaje
      m = re.match(r'^\s*(\d+)\s{2,}(\d+)\s{2,}([\d,]+)\s*%\s{2,}(.*)$', line)
      if m:
        if current:
          records.append(current)
        cluster, cantidad, pct, kw = m.groups()
        current = {
          'cluster': int(cluster),
          'cantidad_de_palabras_clave': int(cantidad),
          'porcentaje_de_palabras_clave': float(pct.replace(',', '.')),
          'principales_palabras_clave': kw.strip()
        }
      else:
        # línea de continuación: se suma al texto de keywords del cluster actual
        current['principales_palabras_clave'] += ' ' + line.strip()

  if current:
    records.append(current)

  # limpiar espacios múltiples y el punto final
  for r in records:
    r['principales_palabras_clave'] = re.sub(r'\s+', ' ', r['principales_palabras_clave']).strip().rstrip('.')

  df = pd.DataFrame(records)
  return df