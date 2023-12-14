from unittest import main, TestCase

from segmentation import segmentacion_de_incendios

def FuegoFactory(id: str = "0", x: float = 0.0, y: float = 0.0, time: str = "2023-01-01T00:00"):
    return {"id": id, "x": x, "y": y, "time": time}


class SegmentacionTestCase(TestCase):
    def test_empty_array_returns_zero_groups(self):
        self.assertEqual(
            segmentacion_de_incendios([], 0, 0),
            (
                0,
                []
            )
        )

    def test_single_element_array_returns_one_group(self):
        self.assertEqual(
            segmentacion_de_incendios([FuegoFactory()], 0, 0),
            (
                1,
                [["0"]]
            )
        )

    def test_two_separated_elements_with_same_date_returns_two_groups(self):
        self.assertEqual(
            segmentacion_de_incendios(
                [
                    FuegoFactory(id="0", x=10, y=10),
                    FuegoFactory(id="1", x=100, y=100)
                ],
                10,
                60
            ),
            (
                2,
                [["0"], ["1"]]
            )
        )

    def test_two_close_elements_with_different_date_returns_two_groups(self):
        self.assertEqual(
            segmentacion_de_incendios(
                [
                    FuegoFactory(id="0", time="2023-01-01T00:00"),
                    FuegoFactory(id="1", time="2023-01-02T00:00")
                ],
                10,
                60
            ),
            (
                2,
                [["0"], ["1"]]
            )
        )

    def test_two_close_elements_with_near_date_returns_one_groups(self):
        self.assertEqual(
            segmentacion_de_incendios(
                [
                    FuegoFactory(id="0", time="2023-01-01T00:00"),
                    FuegoFactory(id="1", time="2023-01-01T00:59")
                ],
                10,
                60
            ),
            (
                1,
                [["0", "1"]]
            )
        )


if __name__ == '__main__':
    main()
