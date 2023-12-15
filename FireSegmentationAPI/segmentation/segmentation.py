from datetime import datetime
from math import pow, sqrt


def distancia(fuego1: dict, fuego2: dict):
  """Devuelve la distancia euclidiana entre dos fuegos

  Input
  ------
  fuego1 : dict
  fuego2 : dict

  Output
  ------
  float
    La distancia euclidiana entre los dos fuegos partir de sus coordenadas x e y.
  """

  return sqrt(
    pow(fuego1["x"] - fuego2["x"], 2) +
    pow(fuego1["y"] - fuego2["y"], 2)
  )


def tiempo(fuego1: dict, fuego2: dict):
  """Devuelve el tiempo en horas entre dos fuegos

  Input
  ------
  fuego1 : dict
  fuego2 : dict

  Output
  ------
  float
    El tiempo en horas entre los dos eventos
  """

  t1 = datetime.strptime(fuego1["date"], "%Y-%m-%dT%H")
  t2 = datetime.strptime(fuego2["date"], "%Y-%m-%dT%H")
  diff = t1 - t2
  return round(diff.total_seconds() / 3600, 2)


def son_cercanos(fuego1: dict, fuego2: dict, d: float, t: float):
  """Determina si 2 fuegos son cercanos a partir de los parámetros de distancia y tiempo

  Input
  ------
  fuego1 : dict
  fuego2 : dict
  d : float
    Distancia máxima para comparar
  t : float
    Tiempo máximo para comparar

  Output
  ------
  float
    El tiempo en horas entre los dos eventos
  """

  d_valid = distancia(fuego1, fuego2) <= d
  t_valid = tiempo(fuego1, fuego2) <= t
  return d_valid and t_valid


def segmentacion_de_incendios(fuegos: list[dict], d: float, t: float) -> tuple[int,list[list[str]]]:
  """Determina el número total de incendios y devuelve los identificadores de cada fuego agrupados

  Input
  ------
  fuegos : list[dict]
    Lista de fuegos totales a agrupar
  d : float
    Distancia máxima para comparar
  t : float
    Tiempo máximo para comparar

  Output
  ------
  tuple[int, list[list[str]]]
    Una tupla con:
    - El número total de incendios
    - Una lista con cada incendio (representado por una lista de identificadores de cada fuego)
  """

  incendios: list[list] = []
  for fuego in fuegos:
    if len(incendios) == 0:
      incendios.append([fuego])
    else:
      cercanos: bool = False

      for incendio in incendios:
        for fuego_incendio in incendio:
          if fuego_incendio["id"] == fuego["id"]:
            continue
          if son_cercanos(fuego, fuego_incendio, d, t):
            incendio.append(fuego)
            cercanos = True
            break

        if cercanos:
          break

      if not cercanos:
        incendios.append([fuego])

  return (
    len(incendios),
    [[fuego["id"] for fuego in incendio] for incendio in incendios]
  )
