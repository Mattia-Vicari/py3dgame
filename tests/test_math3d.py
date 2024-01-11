import py3dgame as p3g
import math

class TestVect:
    def test_init(self) -> None:
        v = p3g.Vec((0, 1, 2))

        assert v._vec[0] == 0
        assert v._vec[1] == 1
        assert v._vec[2] == 2

    # test mathematical operators
    def test_add(self) -> None:
        v1 = p3g.Vec((1, 1, 1))
        v2 = p3g.Vec((0, 1, 2))

        assert (v1 + v2) == p3g.Vec((1, 2, 3))

    def test_sub(self) -> None:
        v1 = p3g.Vec((1, 1, 1))
        v2 = p3g.Vec((1, 2, 3))

        assert (v1 - v2) == p3g.Vec((0, - 1, - 2))
        assert (v2 - v2) == p3g.Vec((0, 0, 0))
        assert (v1 - p3g.Vec((-10, 0, 0))) == p3g.Vec((11, 1, 1))

    def test_abs(self) -> None:
        v = p3g.Vec((0, 3, 4))

        assert abs(v) == 5

    def test_mul(self) -> None:
        v1 = p3g.Vec((1, 2, 3))
        v2 = p3g.Vec((2, 2, 2))

        assert (v1 * v2) == 12
        assert (v1 * 2) == p3g.Vec((2, 4, 6))
        assert (2 * v1) == p3g.Vec((2, 4, 6))

    def test_truediv(self) -> None:
        v1 = p3g.Vec((4, 2, 8))

        assert (v1 / 2) == p3g.Vec((2, 1, 4))

    def test_matmul(self) -> None:
        v1 = p3g.Vec((2, 3, 4))
        v2 = p3g.Vec((5, 6, 7))

        assert (v1 @ v2) == p3g.Vec((- 3, 6, -3))

    def test_normalize(self) -> None:
        v1 = p3g.Vec((100, 0, 0))

        assert v1.normalize() == p3g.Vec((1, 0, 0))

    # test boolean operators
    def test_eq(self) -> None:
        v1 = p3g.Vec((1, 2, 3))
        v2 = p3g.Vec((1, 2, 3))
        v3 = p3g.Vec((2, 2, 3))

        assert (v1 == v2) == True
        assert (v1 == v3) == False


class TestVec3:
    def test_init(self) -> None:

        assert p3g.Vec3(0, 1, 0) == p3g.Vec((0, 1, 0))

    def test_x_property(self) -> None:
        v = p3g.Vec3(0, 1, 2)

        assert v.x == 0
        v.x = 3
        assert v.x == 3

    def test_y_property(self) -> None:
        v = p3g.Vec3(0, 1, 2)

        assert v.y == 1
        v.y = 3
        assert v.y == 3

    def test_z_property(self) -> None:
        v = p3g.Vec3(0, 1, 2)

        assert v.z == 2
        v.z = 3
        assert v.z == 3


class TestQuat:
    def test_init(self) -> None:
        print(p3g.Quat(math.pi, p3g.Vec3(1, 2, 3)))

        assert p3g.Quat(math.pi, p3g.Vec3(1, 2, 3)) == p3g.Vec((0, 1, 2, 3)).normalize()
        assert p3g.Quat(2 * math.pi, p3g.Vec3(1, 2, 3)) == p3g.Vec((- 1, 0, 0, 0)).normalize()

    def test_w_property(self) -> None:
        q = p3g.Quat(0, p3g.Vec3(0, 0, 0))

        assert q.w == 1
        q.w = 3
        assert q.w == 3

    def test_x_property(self) -> None:
        q = p3g.Quat(math.pi, p3g.Vec3(1, 2, 3))

        assert q.x == 1 / 14 ** 0.5
        q.x = 4
        assert q.x == 4

    def test_y_property(self) -> None:
        q = p3g.Quat(math.pi, p3g.Vec3(1, 2, 3))

        assert q.y == 2 / 14 ** 0.5
        q.y = 4
        assert q.y == 4

    def test_z_property(self) -> None:
        q = p3g.Quat(math.pi, p3g.Vec3(1, 2, 3))

        assert q.z == 3 / 14 ** 0.5
        q.z = 4
        assert q.z == 4

    def test_mul(self) -> None:
        q1 = p3g.Quat.from_array((2, 1, 3, 4))
        q2 = p3g.Quat.from_array((2, 3, 1, 4))

        print(q1 * q2)
        assert (q1 * q2) == p3g.Quat.from_array((- 18, 16, 16, 8))

    def test_inverse(self) -> None:
        assert p3g.Quat.from_array((1, 1, 1, 1)).inverse() == p3g.Quat.from_array((0.25, - 0.25, - 0.25, - 0.25))
