"""
Tests for the module math3d
"""

import math
import py3dgame as p3g


class TestVec3:
    """
    Class containing tests for the methods of :class:`Vec3`.
    """

    def test_init(self) -> None:
        """
        Test __init__ method of :class:`Vec3`.
        """

        v = p3g.Vec3(0, 1, 2)

        assert v.x == 0
        assert v.y == 1
        assert v.z == 2

    def test_add(self):
        """
        Test __add__ method of :class:`Vec3`.
        """

        v1 = p3g.Vec3(1, 1, 1)
        v2 = p3g.Vec3(0, 1, 2)

        assert (v1 + v2) == p3g.Vec3(1, 2, 3)

    def test_sub(self) -> None:
        """
        Test __sub__ method of :class:`Vec3`.
        """

        v1 = p3g.Vec3(1, 1, 1)
        v2 = p3g.Vec3(1, 2, 3)

        assert (v1 - v2) == p3g.Vec3(0, - 1, - 2)
        assert (v2 - v2) == p3g.Vec3(0, 0, 0)
        assert (v1 - p3g.Vec3(-10, 0, 0)) == p3g.Vec3(11, 1, 1)

    def test_neg(self) -> None:
        """
        Test __neg__ method of :class:`Vec3`.
        """

        v1 = p3g.Vec3(1, 2, 3)

        assert - v1 == p3g.Vec3(- 1, - 2, - 3)

    def test_abs(self) -> None:
        """
        Test __abs__ method of :class:`Vec3`.
        """

        v = p3g.Vec3(0, 3, 4)

        assert abs(v) == 5

    def test_mul(self) -> None:
        """
        Test __mul__  and __rmul__ methods of :class:`Vec3`.
        """

        v1 = p3g.Vec3(1, 2, 3)
        v2 = p3g.Vec3(2, 2, 2)

        assert (v1 * v2) == 12
        assert (v1 * 2) == p3g.Vec3(2, 4, 6)
        assert (2 * v1) == p3g.Vec3(2, 4, 6)

    def test_truediv(self) -> None:
        """
        Test __truediv__ method of :class:`Vec3`.
        """

        v1 = p3g.Vec3(4, 2, 8)

        assert (v1 / 2) == p3g.Vec3(2, 1, 4)

    def test_matmul(self) -> None:
        """
        Test __matmul__ method of :class:`Vec3`.
        """

        v1 = p3g.Vec3(2, 3, 4)
        v2 = p3g.Vec3(5, 6, 7)

        assert (v1 @ v2) == p3g.Vec3(- 3, 6, -3)

    def test_normalize(self) -> None:
        """
        Test nomalize method of :class:`Vec3`.
        """

        v1 = p3g.Vec3(100, 0, 0)

        assert v1.normalize() == p3g.Vec3(1, 0, 0)

    def test_eq(self) -> None:
        """
        Test __eq__ method of :class:`Vec3`.
        """

        v1 = p3g.Vec3(1, 2, 3)
        v2 = p3g.Vec3(1, 2, 3)
        v3 = p3g.Vec3(2, 2, 3)

        assert (v1 == v2) is True
        assert (v1 == v3) is False


class TestQuat:
    """
    Class containing tests for the methods of :class:`Quat`.
    """

    def test_init(self) -> None:
        """
        Test __init__ method of :class:`Quat`.
        """

        q = p3g.Quat(2 * math.pi, p3g.Vec3(1, 2, 3))

        assert q.axis == p3g.Vec3(1, 2, 3).normalize()
        assert math.isclose(q.angle, 2 * math.pi, abs_tol=1e-12)
        assert math.isclose(q.w, - 1, abs_tol=1e-12)
        assert math.isclose(q.x, 0, abs_tol=1e-12)
        assert math.isclose(q.y, 0, abs_tol=1e-12)
        assert math.isclose(q.z, 0, abs_tol=1e-12)

    def test_from_coord(self) -> None:
        """
        Test from_coord class method of :class:`Quat`.
        """

        q = p3g.Quat.from_coord(1, 2, 3, 4)

        assert q.axis == p3g.Vec3(0, 0, 1)
        assert q.angle == 0
        assert q.w == 1
        assert q.x == 2
        assert q.y == 3
        assert q.z == 4

    def test_from_vec3(self) -> None:
        """
        Test from_vec3 class method of :class:`Quat`.
        """

        q = p3g.Quat.from_vec3(p3g.Vec3(1, 2, 3))

        assert q.axis == p3g.Vec3(0, 0, 1)
        assert q.angle == 0
        assert q.w == 0
        assert q.x == 1
        assert q.y == 2
        assert q.z == 3

    def test_to_vec3(self) -> None:
        """
        Test to_vec3 class method of :class:`Quat`.
        """

        q = p3g.Quat.from_coord(1, 2, 3, 4)

        assert q.to_vec3() == p3g.Vec3(2, 3, 4)

    def test_inverse(self) -> None:
        """
        Test inverse method of :class:`Quat`.
        """

        q1 = p3g.Quat.from_coord(1, 1, 1, 1).inverse()

        assert q1 == p3g.Quat.from_coord(0.25, - 0.25, - 0.25, - 0.25)

    def test_mul(self) -> None:
        """
        Test __mul__ method of :class:`Quat`.
        """

        q1 = p3g.Quat.from_coord(2, 1, 3, 4)
        q2 = p3g.Quat.from_coord(2, 3, 1, 4)

        print(q1 * q2)
        assert (q1 * q2) == p3g.Quat.from_coord(- 18, 16, 16, 8)

