import py3dgame as p3g


class TestVect:
    def test_init(self) -> None:
        v = p3g.Vec(0, 1, 2)

        assert v._vec[0] == 0
        assert v._vec[1] == 1
        assert v._vec[2] == 2

    def test_x_property(self) -> None:
        v = p3g.Vec(0, 1, 2)

        assert v.x == 0
        v.x = 3
        assert v.x == 3

    def test_y_property(self) -> None:
        v = p3g.Vec(0, 1, 2)

        assert v.y == 1
        v.y = 3
        assert v.y == 3

    def test_z_property(self) -> None:
        v = p3g.Vec(0, 1, 2)

        assert v.z == 2
        v.z = 3
        assert v.z == 3

    # test mathematical operators
    def test_add(self) -> None:
        v1 = p3g.Vec(1, 1, 1)
        v2 = p3g.Vec(0, 1, 2)
        v3 = v1 + v2

        assert v3 == p3g.Vec(1, 2, 3)

    def test_sub(self) -> None:
        v1 = p3g.Vec(1, 1, 1)
        v2 = p3g.Vec(1, 2, 3)
        v3 = v1 - v2

        assert v3 == p3g.Vec(0, - 1, - 2)

    def test_abs(self) -> None:
        v = p3g.Vec(0, 3, 4)

        assert abs(v) == 5

    def test_mul(self) -> None:
        v1 = p3g.Vec(1, 2, 3)
        v2 = p3g.Vec(2, 2, 2)
        v3 = v1 * 2
        v4 = 2 * v1

        assert (v1 * v2) == 12
        assert v3 == p3g.Vec(2, 4, 6)
        assert v4 == p3g.Vec(2, 4, 6)

    def test_matmul(self) -> None:
        v1 = p3g.Vec(2, 3, 4)
        v2 = p3g.Vec(5, 6, 7)

        assert (v1 @ v2) == p3g.Vec(- 3, 6, -3)

    # test boolean operators
    def test_eq(self) -> None:
        v1 = p3g.Vec(1, 2, 3)
        v2 = p3g.Vec(1, 2, 3)
        v3 = p3g.Vec(2, 2, 3)

        assert (v1 == v2) == True
        assert (v1 == v3) == False
