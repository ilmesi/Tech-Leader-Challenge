from math import pow, sqrt

from FireSegmentationAPI.segmentation.segmentation import (
    distancia,
    tiempo,
    son_cercanos,
    segmentacion_de_incendios
)


class TestClassSegmentacionDeIncendios:

    def test_segmentacion_de_incendios_distintos(self):
        fuegos = [
            {"id": "2023-01-01+0+0", "x": 0, "y": 0, "date": "2023-01-01T00"},
            {"id": "2023-01-01+10+10", "x": 10, "y": 10, "date": "2023-01-01T00"},
            {"id": "2023-01-01+20+20", "x": 20, "y": 20, "date": "2023-01-01T00"},
            {"id": "2023-01-01+30+30", "x": 30, "y": 30, "date": "2023-01-01T00"},
            {"id": "2023-01-01+40+40", "x": 40, "y": 40, "date": "2023-01-01T00"},
        ]

        d = 1
        t = 1

        resultado = segmentacion_de_incendios(fuegos, d, t)

        assert resultado[0] == 5
        assert len(resultado[1]) == 5

    def test_segmentacion_de_incendios_iguales(self):
        fuegos = [
            {"id": "2023-01-01+0+0", "x": 0, "y": 0, "date": "2023-01-01T00"},
            {"id": "2023-01-01+0+0", "x": 0, "y": 0, "date": "2023-01-01T01"},
            {"id": "2023-01-01+0+0", "x": 0, "y": 0, "date": "2023-01-01T02"},
            {"id": "2023-01-01+0+0", "x": 0, "y": 0, "date": "2023-01-01T03"},
            {"id": "2023-01-01+0+0", "x": 0, "y": 0, "date": "2023-01-01T04"},
        ]

        d = 1
        t = 10

        resultado = segmentacion_de_incendios(fuegos, d, t)

        assert resultado[0] == 1
        assert len(resultado[1]) == 1


class TestClassCercanos:
    def test_no_son_cercanos_mal_fecha(self):
        fuego1 = {"x": 0, "y": 0, "date": "2023-01-01T00"}
        fuego2 = {"x": 0, "y": 10, "date": "2023-01-01T10"}

        d = 100
        t = 1

        distancia_correcta = distancia(fuego1, fuego2) <= d
        tiempo_incorrecto = not tiempo(fuego1, fuego2) <= t
        no_cercanos = not son_cercanos(fuego1, fuego2, d, t)

        assert distancia_correcta
        assert tiempo_incorrecto
        assert no_cercanos

    def test_no_son_cercanos_mal_ubicacion(self):
        fuego1 = {"x": 0, "y": 0, "date": "2023-01-01T00"}
        fuego2 = {"x": 0, "y": 10, "date": "2023-01-01T10"}

        d = 1
        t = 100

        distancia_incorrecta = not distancia(fuego1, fuego2) <= d
        tiempo_correcto = tiempo(fuego1, fuego2) <= t
        no_cercanos = not son_cercanos(fuego1, fuego2, d, t)

        assert distancia_incorrecta
        assert tiempo_correcto
        assert no_cercanos

    def test_no_son_cercanos_mal_ubicacion_y_fecha(self):
        fuego1 = {"x": 0, "y": 0, "date": "2023-01-01T00"}
        fuego2 = {"x": 0, "y": 10, "date": "2023-01-01T10"}

        d = 1
        t = 1

        distancia_incorrecta = not distancia(fuego1, fuego2) <= d
        tiempo_incorrecto = not tiempo(fuego1, fuego2) <= t
        no_cercanos = not son_cercanos(fuego1, fuego2, d, t)

        assert distancia_incorrecta
        assert tiempo_incorrecto
        assert no_cercanos

    def test_son_cercanos(self):
        fuego1 = {"x": 0, "y": 0, "date": "2023-01-01T00"}
        fuego2 = {"x": 0, "y": 10, "date": "2023-01-01T10"}

        d = 100
        t = 100

        distancia_correcta = distancia(fuego1, fuego2) <= d
        tiempo_correcto = tiempo(fuego1, fuego2) <= t
        cercanos = son_cercanos(fuego1, fuego2, d, t)

        assert distancia_correcta
        assert tiempo_correcto
        assert cercanos


class TestClassDistancia:
    def test_distancia_zero(self):
        fuego1 = {"x": 10, "y": 10}
        fuego2 = {"x": 10, "y": 10}

        d = sqrt(
            pow(fuego1["x"] - fuego2["x"], 2) +
            pow(fuego1["y"] - fuego2["y"], 2)
        )

        nueva_distancia = distancia(fuego1, fuego2)
        assert nueva_distancia == 0
        assert nueva_distancia == d

    def test_distancia_1(self):
        fuego1 = {"x": 0, "y": 0}
        fuego2 = {"x": 0, "y": 1}

        d = sqrt(
            pow(fuego1["x"] - fuego2["x"], 2) +
            pow(fuego1["y"] - fuego2["y"], 2)
        )

        nueva_distancia = distancia(fuego1, fuego2)
        assert nueva_distancia == 1
        assert nueva_distancia == d


class TestClassTiempo:
    def test_tiempo_0(self):
        fuego1 = {"date": "2023-01-01T00"}
        fuego2 = {"date": "2023-01-01T00"}

        t = tiempo(fuego1, fuego2)

        assert t == 0

    def test_tiempo_1(self):
        fuego1 = {"date": "2023-01-01T00"}
        fuego2 = {"date": "2023-01-01T01"}

        t = tiempo(fuego1, fuego2)

        assert t == 1
