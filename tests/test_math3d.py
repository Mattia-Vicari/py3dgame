"""
Tests for the module math3d
"""

import math
import py3dgame as p3g


class TestVect:
    """
    Class containing tests for the methods of :class:`Vec`.
    """

    def test_init(self) -> None:
        """
        Test __init__ method of :class:`Vec`.
        """

        v = p3g.Vec((0, 1, 2))

        assert v.to_nparray()[0] == 0
        assert v.to_nparray()[1] == 1
        assert v.to_nparray()[2] == 2

    # test mathematical operators
    def test_add(self) -> None:
        """
        Test __add__ method of :class:`Vec`.
        """
        v1 = p3g.Vec((1, 1, 1))
        v2 = p3g.Vec((0, 1, 2))

        assert (v1 + v2) == p3g.Vec((1, 2, 3))

    def test_sub(self) -> None:
        """
        Test __sub__ method of :class:`Vec`.
        """

        v1 = p3g.Vec((1, 1, 1))
        v2 = p3g.Vec((1, 2, 3))

        assert (v1 - v2) == p3g.Vec((0, - 1, - 2))
        assert (v2 - v2) == p3g.Vec((0, 0, 0))
        assert (v1 - p3g.Vec((-10, 0, 0))) == p3g.Vec((11, 1, 1))

    def test_abs(self) -> None:
        """
        Test __abs__ method of :class:`Vec`.
        """

        v = p3g.Vec((0, 3, 4))

        assert abs(v) == 5

    def test_mul(self) -> None:
        """
        Test __mul__ method of :class:`Vec`.
        """

        v1 = p3g.Vec((1, 2, 3))
        v2 = p3g.Vec((2, 2, 2))

        assert (v1 * v2) == 12
        assert (v1 * 2) == p3g.Vec((2, 4, 6))
        assert (2 * v1) == p3g.Vec((2, 4, 6))

    def test_truediv(self) -> None:
        """
        Test __truediv__ method of :class:`Vec`.
        """

        v1 = p3g.Vec((4, 2, 8))

        assert (v1 / 2) == p3g.Vec((2, 1, 4))

    def test_matmul(self) -> None:
        """
        Test __matmul__ method of :class:`Vec`.
        """

        v1 = p3g.Vec((2, 3, 4))
        v2 = p3g.Vec((5, 6, 7))

        assert (v1 @ v2) == p3g.Vec((- 3, 6, -3))

    def test_normalize(self) -> None:
        """
        Test nomalize method of :class:`Vec`.
        """

        v1 = p3g.Vec((100, 0, 0))

        assert v1.normalize() == p3g.Vec((1, 0, 0))

    # test boolean operators
    def test_eq(self) -> None:
        """
        Test __eq__ method of :class:`Vec`.
        """

        v1 = p3g.Vec((1, 2, 3))
        v2 = p3g.Vec((1, 2, 3))
        v3 = p3g.Vec((2, 2, 3))

        assert (v1 == v2) is True
        assert (v1 == v3) is False


class TestVec3:
    """
    Class containing tests for the methods and properties of :class:`Vec3`.
    """

    def test_init(self) -> None:
        """
        Test __init__ method of :class:`Vec3`.
        """

        assert p3g.Vec3(0, 1, 0) == p3g.Vec((0, 1, 0))

    def test_x_property(self) -> None:
        """
        Test x property of :class:`Vec3`.
        """

        v = p3g.Vec3(0, 1, 2)

        assert v.x == 0
        v.x = 3
        assert v.x == 3

    def test_y_property(self) -> None:
        """
        Test y property of :class:`Vec3`.
        """

        v = p3g.Vec3(0, 1, 2)

        assert v.y == 1
        v.y = 3
        assert v.y == 3

    def test_z_property(self) -> None:
        """
        Test z property of :class:`Vec3`.
        """

        v = p3g.Vec3(0, 1, 2)

        assert v.z == 2
        v.z = 3
        assert v.z == 3


class TestQuat:
    """
    Class containing tests for the methods and rpoperties of :class:`Quat`.
    """

    def test_init(self) -> None:
        """
        Test __init__ method of :class:`Quat`.
        """

        assert p3g.Quat(math.pi, p3g.Vec3(1, 2, 3)) == p3g.Vec((0, 1, 2, 3)).normalize()
        assert p3g.Quat(2 * math.pi, p3g.Vec3(1, 2, 3)) == p3g.Vec((- 1, 0, 0, 0)).normalize()

    def test_w_property(self) -> None:
        """
        Test w property of :class:`Quat`.
        """

        q = p3g.Quat(0, p3g.Vec3(0, 0, 0))

        assert q.w == 1
        q.w = 3
        assert q.w == 3

    def test_x_property(self) -> None:
        """
        Test x property of :class:`Quat`.
        """

        q = p3g.Quat(math.pi, p3g.Vec3(1, 2, 3))

        assert q.x == 1 / 14 ** 0.5
        q.x = 4
        assert q.x == 4

    def test_y_property(self) -> None:
        """
        Test y property of :class:`Quat`.
        """

        q = p3g.Quat(math.pi, p3g.Vec3(1, 2, 3))

        assert q.y == 2 / 14 ** 0.5
        q.y = 4
        assert q.y == 4

    def test_z_property(self) -> None:
        """
        Test z property of :class:`Quat`.
        """

        q = p3g.Quat(math.pi, p3g.Vec3(1, 2, 3))

        assert q.z == 3 / 14 ** 0.5
        q.z = 4
        assert q.z == 4

    def test_mul(self) -> None:
        """
        Test __mul__ method of :class:`Quat`.
        """

        q1 = p3g.Quat.from_array((2, 1, 3, 4))
        q2 = p3g.Quat.from_array((2, 3, 1, 4))

        print(q1 * q2)
        assert (q1 * q2) == p3g.Quat.from_array((- 18, 16, 16, 8))

    def test_inverse(self) -> None:
        """
        Test inverse method of :class:`Quat`.
        """

        q1 = p3g.Quat.from_array((1, 1, 1, 1)).inverse()

        assert q1 == p3g.Quat.from_array((0.25, - 0.25, - 0.25, - 0.25))
