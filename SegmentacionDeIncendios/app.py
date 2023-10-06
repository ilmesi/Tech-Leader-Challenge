def segmentacionDeIncendios(fuegos: list[dict], d: float, t: float) -> tuple[int,list[list[str]]]:
  # Completar el código en esta funcion
  # Se recomienda modularizar la solucion para hacer más claro el código
  return (2, [["0", "1", "2"], ["3", "4"]])


def ejemplo():
  # Una vez implementado el testing, se puede eliminar esta funcion.
  # Dejo el codigo acá para poder hacer una prueba rápida
  fuegos: list[dict] = [
    {"id": "0", "x": 0.0, "y": 0.0, "time":"2023-01-01T00:00"},
    {"id": "1", "x": 1.0, "y": 0.0, "time":"2023-01-01T00:00"},
    {"id": "2", "x": 0.0, "y": 1.0, "time":"2023-01-01T00:00"},
    {"id": "3", "x": 10.0, "y": 10.0, "time":"2023-01-01T00:00"},
    {"id": "4", "x": 10.0, "y": 11.0, "time":"2023-01-01T00:00"}
  ]

  d: float = 10.0
  t: float = 60.0

  print(segmentacionDeIncendios(fuegos, d, t))