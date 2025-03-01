"""module dedicated to the integration of bodycomposition data"""

#! IMPORTS


from math import atan, exp, log, pi, prod
from typing import Literal


#! CLASS


class CheckupBIA:
    """
    an object allowing the calculation of body composition data from
    anthropometric and electric data.
    """

    _age: int
    _sex: Literal["M", "F"]
    _hcm: int
    _wgt: float
    _left_arm_r: int | float | None
    _left_arm_x: int | float | None
    _left_trunk_r: int | float | None
    _left_trunk_x: int | float | None
    _left_leg_r: int | float | None
    _left_leg_x: int | float | None
    _left_body_r: int | float | None
    _left_body_x: int | float | None
    _right_arm_r: int | float | None
    _right_arm_x: int | float | None
    _right_trunk_r: int | float | None
    _right_trunk_x: int | float | None
    _right_leg_r: int | float | None
    _right_leg_x: int | float | None
    _right_body_r: int | float | None
    _right_body_x: int | float | None
    _left_arm_r_betas = (-5.929064, 0.874883)
    _left_arm_x_betas = (3.304037, 0.686138)
    _left_body_r_betas = (29.735312, 0.893878)
    _left_body_x_betas = (-5.850700, 1.077053)
    _left_leg_r_betas = (22.703793, 0.988802)
    _left_leg_x_betas = (-0.196244, 0.988221)
    _left_trunk_r_betas = (2.874024, 0.868278)
    _left_trunk_x_betas = (7.535099, 0.028624)
    _right_arm_r_betas = (-17.392322, 0.904717)
    _right_arm_x_betas = (1.392877, 0.782267)
    _right_body_r_betas = (-13.248009, 0.971554)
    _right_body_x_betas = (4.612482, 0.886881)
    _right_leg_r_betas = (3.174666, 1.071437)
    _right_leg_x_betas = (-0.259402, 0.991873)
    _right_trunk_r_betas = (0.973686, 1.038562)
    _right_trunk_x_betas = (8.288528, -0.053032)

    def __init__(
        self,
        age: int | float,
        sex: Literal["M", "F"],
        height: int,
        weight: int | float,
        left_arm_r: int | float | None = None,
        left_arm_x: int | float | None = None,
        left_trunk_r: int | float | None = None,
        left_trunk_x: int | float | None = None,
        left_leg_r: int | float | None = None,
        left_leg_x: int | float | None = None,
        left_body_r: int | float | None = None,
        left_body_x: int | float | None = None,
        right_arm_r: int | float | None = None,
        right_arm_x: int | float | None = None,
        right_trunk_r: int | float | None = None,
        right_trunk_x: int | float | None = None,
        right_leg_r: int | float | None = None,
        right_leg_x: int | float | None = None,
        right_body_r: int | float | None = None,
        right_body_x: int | float | None = None,
        raw_electric_data: bool = False,
    ):
        self.set_age(age)
        self.set_sex(sex)
        self.set_height(height)
        self.set_weight(weight)

        self.set_left_arm_r(left_arm_r, raw_electric_data)
        self.set_left_arm_x(left_arm_x, raw_electric_data)
        self.set_left_leg_r(left_leg_r, raw_electric_data)
        self.set_left_leg_x(left_leg_x, raw_electric_data)
        self.set_left_trunk_r(left_trunk_r, raw_electric_data)
        self.set_left_trunk_x(left_trunk_x, raw_electric_data)
        self.set_left_body_r(left_body_r, raw_electric_data)
        self.set_left_body_x(left_body_x, raw_electric_data)

        self.set_right_arm_r(right_arm_r, raw_electric_data)
        self.set_right_arm_x(right_arm_x, raw_electric_data)
        self.set_right_leg_r(right_leg_r, raw_electric_data)
        self.set_right_leg_x(right_leg_x, raw_electric_data)
        self.set_right_trunk_r(right_trunk_r, raw_electric_data)
        self.set_right_trunk_x(right_trunk_x, raw_electric_data)
        self.set_right_body_r(right_body_r, raw_electric_data)
        self.set_right_body_x(right_body_x, raw_electric_data)

    def _nones(self, *args):
        """private method to check if any entry is None"""
        return [x is None for x in args]

    def _phase_angle_deg(
        self,
        res: float | int | None,
        rea: float | int | None,
    ):
        """return the phase angle in degrees"""
        if any(self._nones(res, rea)):
            return None
        return float(atan(rea / res)) * 180 / pi  # type: ignore

    def set_age(self, age: int | float):
        """set the user age in years"""
        self._age = int(age)

    def set_weight(self, wgt: int | float):
        """set the user weight in kg"""
        self._wgt = float(wgt)

    def set_height(self, hcm: int | float):
        """set the user height in cm"""
        self._hcm = int(hcm)

    def set_sex(self, sex: Literal["M", "F"]):
        """set the user sex"""
        self._sex = sex

    def set_left_arm_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the left arm resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._left_arm_r = r
        else:
            self._left_arm_r = sum(map(prod, zip((1, r), self._left_arm_r_betas)))

    def set_left_arm_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the left arm reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._left_arm_x = x
        else:
            self._left_arm_x = sum(map(prod, zip((1, x), self._left_arm_x_betas)))

    def set_left_leg_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the left leg resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._left_leg_r = r
        else:
            self._left_leg_r = sum(map(prod, zip((1, r), self._left_leg_r_betas)))

    def set_left_leg_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the left leg reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._left_leg_x = x
        else:
            self._left_leg_x = sum(map(prod, zip((1, x), self._left_leg_x_betas)))

    def set_left_trunk_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the left trunk resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._left_trunk_r = r
        else:
            self._left_trunk_r = sum(map(prod, zip((1, r), self._left_trunk_r_betas)))

    def set_left_trunk_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the left trunk reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._left_trunk_x = x
        else:
            self._left_trunk_x = sum(map(prod, zip((1, x), self._left_trunk_x_betas)))

    def set_left_body_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the left body resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._left_body_r = r
        else:
            self._left_body_r = sum(map(prod, zip((1, r), self._left_body_r_betas)))

    def set_left_body_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the left body reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._left_body_x = x
        else:
            self._left_body_x = sum(map(prod, zip((1, x), self._left_body_x_betas)))

    def set_right_arm_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the right arm resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._right_arm_r = r
        else:
            self._right_arm_r = sum(map(prod, zip((1, r), self._right_arm_r_betas)))

    def set_right_arm_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the right arm reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._right_arm_x = x
        else:
            self._right_arm_x = sum(map(prod, zip((1, x), self._right_arm_x_betas)))

    def set_right_leg_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the right arm resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._right_leg_r = r
        else:
            self._right_leg_r = sum(map(prod, zip((1, r), self._right_leg_r_betas)))

    def set_right_leg_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the right leg reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._right_leg_x = x
        else:
            self._right_leg_x = sum(map(prod, zip((1, x), self._right_leg_x_betas)))

    def set_right_trunk_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the right trunk resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._right_trunk_r = r
        else:
            self._right_trunk_r = sum(map(prod, zip((1, r), self._right_trunk_r_betas)))

    def set_right_trunk_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the right trunk reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._right_trunk_x = x
        else:
            self._right_trunk_x = sum(map(prod, zip((1, x), self._right_trunk_x_betas)))

    def set_right_body_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the right body resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._right_body_r = r
        else:
            self._right_body_r = sum(map(prod, zip((1, r), self._right_body_r_betas)))

    def set_right_body_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the right body reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._right_body_x = x
        else:
            self._right_body_x = sum(map(prod, zip((1, x), self._right_body_x_betas)))

    @property
    def age(self):
        """the user age in years"""
        return self._age

    @property
    def weight(self):
        """the user weight in kg"""
        return self._wgt

    @property
    def height(self):
        """the user height in cm"""
        return self._hcm

    @property
    def sex(self):
        """the user sex"""
        return self._sex

    @property
    def left_arm_r(self):
        """the left arm resistance in Ohm"""
        return self._left_arm_r

    @property
    def left_arm_x(self):
        """the left arm reactance in Ohm"""
        return self._left_arm_x

    @property
    def left_leg_r(self):
        """the left leg resistance in Ohm"""
        return self._left_leg_r

    @property
    def left_leg_x(self):
        """set the left leg reactance in Ohm"""
        return self._left_leg_x

    @property
    def left_trunk_r(self):
        """the left trunk resistance in Ohm"""
        return self._left_trunk_r

    @property
    def left_trunk_x(self):
        """the left trunk reactance in Ohm"""
        return self._left_trunk_x

    @property
    def left_body_r(self):
        """the left body resistance in Ohm"""
        return self._left_body_r

    @property
    def left_body_x(self):
        """the left body reactance in Ohm"""
        return self._left_body_x

    @property
    def right_arm_r(self):
        """the right arm resistance in Ohm"""
        return self._right_arm_r

    @property
    def right_arm_x(self):
        """the right arm reactance in Ohm"""
        return self._right_arm_x

    @property
    def right_leg_r(self):
        """the right leg resistance in Ohm"""
        return self._right_leg_r

    @property
    def right_leg_x(self):
        """the right leg reactance in Ohm"""
        return self._right_leg_x

    @property
    def right_trunk_r(self):
        """the right trunk resistance in Ohm"""
        return self._right_trunk_r

    @property
    def right_trunk_x(self):
        """the right trunk reactance in Ohm"""
        return self._right_trunk_x

    @property
    def right_body_r(self):
        """the right body resistance in Ohm"""
        return self._right_body_r

    @property
    def right_body_x(self):
        """the right body reactance in Ohm"""
        return self._right_body_x

    @property
    def left_arm_r_raw(self):
        """return the left arm resistance directly measured from sensors in Ohm"""
        if self.left_arm_r is None:
            return None
        return (self.left_arm_r - self._left_arm_r_betas[0]) / self._left_arm_r_betas[1]

    @property
    def left_arm_x_raw(self):
        """return the left arm reactance directly measured from sensors in Ohm"""
        if self.left_arm_x is None:
            return None
        return (self.left_arm_x - self._left_arm_x_betas[0]) / self._left_arm_x_betas[1]

    @property
    def left_leg_r_raw(self):
        """return the left leg resistance directly measured from sensors in Ohm"""
        if self.left_leg_r is None:
            return None
        return (self.left_leg_r - self._left_leg_r_betas[0]) / self._left_leg_r_betas[1]

    @property
    def left_leg_x_raw(self):
        """return the left leg reactance directly measured from sensors in Ohm"""
        if self.left_leg_x is None:
            return None
        return (self.left_leg_x - self._left_leg_x_betas[0]) / self._left_leg_x_betas[1]

    @property
    def left_trunk_r_raw(self):
        """return the left trunk resistance directly measured from sensors in Ohm"""
        if self.left_trunk_r is None:
            return None
        return (
            self.left_trunk_r - self._left_trunk_r_betas[0]
        ) / self._left_trunk_r_betas[1]

    @property
    def left_trunk_x_raw(self):
        """return the left trunk reactance directly measured from sensors in Ohm"""
        if self.left_trunk_x is None:
            return None
        return (
            self.left_trunk_x - self._left_trunk_x_betas[0]
        ) / self._left_trunk_x_betas[1]

    @property
    def left_body_r_raw(self):
        """return the left body resistance directly measured from sensors in Ohm"""
        if self.left_body_r is None:
            return None
        return (
            self.left_body_r - self._left_body_r_betas[0]
        ) / self._left_body_r_betas[1]

    @property
    def left_body_x_raw(self):
        """return the left body reactance directly measured from sensors in Ohm"""
        if self.left_body_x is None:
            return None
        return (
            self.left_body_x - self._left_body_x_betas[0]
        ) / self._left_body_x_betas[1]

    @property
    def right_arm_r_raw(self):
        """return the right arm resistance directly measured from sensors in Ohm"""
        if self.right_arm_r is None:
            return None
        return (
            self.right_arm_r - self._right_arm_r_betas[0]
        ) / self._right_arm_r_betas[1]

    @property
    def right_arm_x_raw(self):
        """return the right arm reactance directly measured from sensors in Ohm"""
        if self.right_arm_x is None:
            return None
        return (
            self.right_arm_x - self._right_arm_x_betas[0]
        ) / self._right_arm_x_betas[1]

    @property
    def right_leg_r_raw(self):
        """return the right leg resistance directly measured from sensors in Ohm"""
        if self.right_leg_r is None:
            return None
        return (
            self.right_leg_r - self._right_leg_r_betas[0]
        ) / self._right_leg_r_betas[1]

    @property
    def right_leg_x_raw(self):
        """return the right leg reactance directly measured from sensors in Ohm"""
        if self.right_leg_x is None:
            return None
        return (
            self.right_leg_x - self._right_leg_x_betas[0]
        ) / self._right_leg_x_betas[1]

    @property
    def right_trunk_r_raw(self):
        """return the right trunk resistance directly measured from sensors in Ohm"""
        if self.right_trunk_r is None:
            return None
        return (
            self.right_trunk_r - self._right_trunk_r_betas[0]
        ) / self._right_trunk_r_betas[1]

    @property
    def right_trunk_x_raw(self):
        """return the right trunk reactance directly measured from sensors in Ohm"""
        if self.right_trunk_x is None:
            return None
        return (
            self.right_trunk_x - self._right_trunk_x_betas[0]
        ) / self._right_trunk_x_betas[1]

    @property
    def right_body_r_raw(self):
        """return the right body resistance directly measured from sensors in Ohm"""
        if self.right_body_r is None:
            return None
        return (
            self.right_body_r - self._right_body_r_betas[0]
        ) / self._right_body_r_betas[1]

    @property
    def right_body_x_raw(self):
        """return the right body reactance directly measured from sensors in Ohm"""
        if self.right_body_x is None:
            return None
        return (
            self.right_body_x - self._right_body_x_betas[0]
        ) / self._right_body_x_betas[1]

    @property
    def left_arm_z(self):
        """return the left arm impedance in Ohm"""
        if self.left_arm_r is None or self.left_arm_x is None:
            return None
        return float((self.left_arm_r**2 + self.left_arm_x**2) ** 0.5)

    @property
    def left_arm_z_raw(self):
        """return the left arm impedance in Ohm from raw electric data"""
        if self.left_arm_r_raw is None or self.left_arm_x_raw is None:
            return None
        return (self.left_arm_r_raw**2 + self.left_arm_x_raw**2) ** 0.5

    @property
    def left_leg_z(self):
        """return the left leg impedance in Ohm"""
        if self.left_leg_r is None or self.left_leg_x is None:
            return None
        return float((self.left_leg_r**2 + self.left_leg_x**2) ** 0.5)

    @property
    def left_leg_z_raw(self):
        """return the left leg impedance in Ohm from raw electric data"""
        if self.left_leg_r_raw is None or self.left_leg_x_raw is None:
            return None
        return (self.left_leg_r_raw**2 + self.left_leg_x_raw**2) ** 0.5

    @property
    def left_trunk_z(self):
        """return the left trunk impedance in Ohm"""
        if self.left_trunk_r is None or self.left_trunk_x is None:
            return None
        return float((self.left_trunk_r**2 + self.left_trunk_x**2) ** 0.5)

    @property
    def left_trunk_z_raw(self):
        """return the left trunk impedance in Ohm from raw electric data"""
        if self.left_trunk_r_raw is None or self.left_trunk_x_raw is None:
            return None
        return (self.left_trunk_r_raw**2 + self.left_trunk_x_raw**2) ** 0.5

    @property
    def left_body_z(self):
        """return the left body impedance in Ohm"""
        if self.left_body_r is None or self.left_body_x is None:
            return None
        return float((self.left_body_r**2 + self.left_body_x**2) ** 0.5)

    @property
    def left_body_z_raw(self):
        """return the left body impedance in Ohm from raw electric data"""
        if self.left_body_r_raw is None or self.left_body_x_raw is None:
            return None
        return (self.left_body_r_raw**2 + self.left_body_x_raw**2) ** 0.5

    @property
    def right_arm_z(self):
        """return the right arm impedance in Ohm"""
        if self.right_arm_r is None or self.right_arm_x is None:
            return None
        return float((self.right_arm_r**2 + self.right_arm_x**2) ** 0.5)

    @property
    def right_arm_z_raw(self):
        """return the right arm impedance in Ohm from raw electric data"""
        if self.right_arm_r_raw is None or self.right_arm_x_raw is None:
            return None
        return (self.right_arm_r_raw**2 + self.right_arm_x_raw**2) ** 0.5

    @property
    def right_leg_z(self):
        """return the right leg impedance in Ohm"""
        if self.right_leg_r is None or self.right_leg_x is None:
            return None
        return float((self.right_leg_r**2 + self.right_leg_x**2) ** 0.5)

    @property
    def right_leg_z_raw(self):
        """return the right leg impedance in Ohm from raw electric data"""
        if self.right_leg_r_raw is None or self.right_leg_x_raw is None:
            return None
        return (self.right_leg_r_raw**2 + self.right_leg_x_raw**2) ** 0.5

    @property
    def right_trunk_z(self):
        """return the right trunk impedance in Ohm"""
        if self.right_trunk_r is None or self.right_trunk_x is None:
            return None
        return float((self.right_trunk_r**2 + self.right_trunk_x**2) ** 0.5)

    @property
    def right_trunk_z_raw(self):
        """return the right trunk impedance in Ohm from raw electric data"""
        if self.right_trunk_r_raw is None or self.right_trunk_x_raw is None:
            return None
        return (self.right_trunk_r_raw**2 + self.right_trunk_x_raw**2) ** 0.5

    @property
    def right_body_z(self):
        """return the right body impedance in Ohm"""
        if self.right_body_r is None or self.right_body_x is None:
            return None
        return float((self.right_body_r**2 + self.right_body_x**2) ** 0.5)

    @property
    def right_body_z_raw(self):
        """return the right body impedance in Ohm from raw electric data"""
        if self.right_body_r_raw is None or self.right_body_x_raw is None:
            return None
        return (self.right_body_r_raw**2 + self.right_body_x_raw**2) ** 0.5

    @property
    def left_arm_phase_angle(self):
        """return the left arm phase angle in degrees"""
        return self._phase_angle_deg(self.left_arm_r, self.left_arm_x)

    @property
    def left_arm_phase_angle_raw(self):
        """return the left arm phase angle from raw electric data in degrees"""
        return self._phase_angle_deg(self.left_arm_r_raw, self.left_arm_x_raw)

    @property
    def left_leg_phase_angle(self):
        """return the left leg phase angle in degrees"""
        return self._phase_angle_deg(self.left_leg_r, self.left_leg_x)

    @property
    def left_leg_phase_angle_raw(self):
        """return the left leg phase angle from raw electric data in degrees"""
        return self._phase_angle_deg(self.left_leg_r_raw, self.left_leg_x_raw)

    @property
    def left_trunk_phase_angle(self):
        """return the left trunk phase angle in degrees"""
        return self._phase_angle_deg(self.left_trunk_r, self.left_trunk_x)

    @property
    def left_trunk_phase_angle_raw(self):
        """return the left trunk phase angle from raw electric data in degrees"""
        return self._phase_angle_deg(self.left_trunk_r_raw, self.left_trunk_x_raw)

    @property
    def left_body_phase_angle(self):
        """return the left body phase angle in degrees"""
        return self._phase_angle_deg(self.left_body_r, self.left_body_x)

    @property
    def left_body_phase_angle_raw(self):
        """return the left body phase angle from raw electric datain degrees"""
        return self._phase_angle_deg(self.left_body_r_raw, self.left_body_x_raw)

    @property
    def right_arm_phase_angle(self):
        """return the right arm phase angle in degrees"""
        return self._phase_angle_deg(self.right_arm_r, self.right_arm_x)

    @property
    def right_arm_phase_angle_raw(self):
        """return the right arm phase angle from raw electric datain degrees"""
        return self._phase_angle_deg(self.right_arm_r_raw, self.right_arm_x_raw)

    @property
    def right_leg_phase_angle(self):
        """return the right leg phase angle in degrees"""
        return self._phase_angle_deg(self.right_leg_r, self.right_leg_x)

    @property
    def right_leg_phase_angle_raw(self):
        """return the right leg phase angle from raw electric datain degrees"""
        return self._phase_angle_deg(self.right_leg_r_raw, self.right_leg_x_raw)

    @property
    def right_trunk_phase_angle(self):
        """return the right trunk phase angle in degrees"""
        return self._phase_angle_deg(self.right_trunk_r, self.right_trunk_x)

    @property
    def right_trunk_phase_angle_raw(self):
        """return the right trunk phase angle from raw electric datain degrees"""
        return self._phase_angle_deg(self.right_trunk_r_raw, self.right_trunk_x_raw)

    @property
    def right_body_phase_angle(self):
        """return the right body phase angle in degrees"""
        return self._phase_angle_deg(self.right_body_r, self.right_body_x)

    @property
    def right_body_phase_angle_raw(self):
        """return the right body phase angle from raw electric datain degrees"""
        return self._phase_angle_deg(self.right_body_r_raw, self.right_body_x_raw)

    def is_male(self):
        """return True if the user is declared as male"""
        return self.sex == "M"

    @property
    def total_body_water(self):
        """return the total body water in liters and as percentage
        of the total body weight"""

        """old
        if any(self._nones(self.right_body_r)):
            return None, None
        lt = float(
            +0.286
            + 0.195 * self.height**2 / self.right_body_r  # type: ignore
            + 0.385 * self.weight
            + 5.086 * self.is_male()
        )
        """
        if any(
            self._nones(
                self.height,
                self.age,
                self.weight,
                self.left_body_r_raw,
                self.right_body_r_raw,
                self.left_body_x_raw,
                self.right_body_x_raw,
                self.left_body_phase_angle_raw,
                self.right_body_phase_angle_raw,
                self.left_body_z_raw,
                self.right_body_z_raw,
            )
        ):
            return None
        return float(
            -17.75953
            + 0.12309 * self.weight
            + 0.00734 * self.age
            + 0.55780 * (self.height**2) / ((self.left_body_r_raw + self.right_body_r_raw) / 2)  # type: ignore
            + 0.00208 * (((self.left_body_x_raw + self.right_body_x_raw) / 2) ** 2)  # type: ignore
            + 0.01627 * (self.height**2) / ((self.left_body_z_raw + self.right_body_z_raw) / 2)  # type: ignore
            + 0.16738 * (((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2) ** 2)  # type: ignore
            + 0.00152 * (self.height**2) / ((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2)  # type: ignore
        )

    @property
    def extra_cellular_water(self):
        """return the extracellular water in liters"""

        """old
        if any(self._nones(self.right_body_r, self.right_body_x)):
            return None
        lt = float(
            -3.32
            + 0.2 * self.height**2 / self.right_body_r  # type: ignore
            + 0.005 * self.height**2 / self.right_body_x  # type: ignore
            + 1.86 * ~self.is_male()
            + 0.08 * self.weight
        )
        if self.is_male():
            b0, b1 = [2.05848, 0.73795]
        else:
            b0, b1 = [0.46441, 1.21434]
        return b0 * lt**b1
        """
        if any(
            self._nones(
                self.height,
                self.age,
                self.weight,
                self.left_body_r_raw,
                self.right_body_r_raw,
                self.left_body_x_raw,
                self.right_body_x_raw,
                self.left_body_phase_angle_raw,
                self.right_body_phase_angle_raw,
                self.left_body_z_raw,
                self.right_body_z_raw,
            )
        ):
            return None
        return float(
            -5.27113
            + 0.04381 * self.weight
            + 0.00320 * self.age
            + 0.22309 * (self.height**2) / ((self.left_body_r_raw + self.right_body_r_raw) / 2)  # type: ignore
            + 0.00081 * (((self.left_body_x_raw + self.right_body_x_raw) / 2) ** 2)  # type: ignore
            + 0.01760 * (self.height**2) / ((self.left_body_z_raw + self.right_body_z_raw) / 2)  # type: ignore
            + 0.00592 * (((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2) ** 2)  # type: ignore
            + 0.00041 * (self.height**2) / ((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2)  # type: ignore
        )

    @property
    def intra_cellular_water(self):
        """return the intracellular water in liters"""
        tbw_lt = self.total_body_water  # type: ignore
        ecw_lt = self.extra_cellular_water  # type: ignore
        if any(self._nones(tbw_lt, ecw_lt)):
            return None
        return float(tbw_lt - ecw_lt)  # type: ignore

    @property
    def bmi(self):
        """return the user BMI"""
        return self.weight / (self.height / 100) ** 2

    @property
    def fat_free_mass(self):
        """return the free-fat mass in kg"""

        """old
        if any(self._nones(self.right_body_r, self.right_body_x)):
            return None
        ffm = float(  # kanellakis
            +12.299
            - 0.116 * self.right_body_r / ((self.height / 100) ** 2)  # type: ignore
            + 0.164 * self.weight
            + 0.365 * self.right_body_x / ((self.height / 100) ** 2)  # type: ignore
            + 7.827 * self.is_male()
            + 0.2157 * self.height
        )
        if self.bmi >= 30:
            ffm = ffm - 0.256 * (self.bmi - 30)
        if self.is_male():
            b0, b1 = [0.14931, 1.48464]
        else:
            b0, b1 = [0.85323, 1.08360]
        ffm = b0 * ffm**b1
        return ffm
        """
        if any(
            self._nones(
                self.height,
                self.age,
                self.weight,
                self.left_body_r_raw,
                self.right_body_r_raw,
                self.left_body_x_raw,
                self.right_body_x_raw,
                self.left_body_phase_angle_raw,
                self.right_body_phase_angle_raw,
                self.left_body_z_raw,
                self.right_body_z_raw,
            )
        ):
            return None
        return float(
            -25.08860
            + 0.17591 * self.weight
            + 0.01007 * self.age
            + 0.73751 * (self.height**2) / ((self.left_body_r_raw + self.right_body_r_raw) / 2)  # type: ignore
            + 0.00294 * (((self.left_body_x_raw + self.right_body_x_raw) / 2) ** 2)  # type: ignore
            + 0.02856 * (self.height**2) / ((self.left_body_z_raw + self.right_body_z_raw) / 2)  # type: ignore
            + 0.24395 * (((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2) ** 2)  # type: ignore
            + 0.00217 * (self.height**2) / ((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2)  # type: ignore
        )

    @property
    def fat_mass(self):
        """return the fat mass in kg"""
        if any(self._nones(self.fat_free_mass, self.weight)):
            return None
        return float(self.weight - self.fat_free_mass)  # type: ignore

    @property
    def bone_mineral_content(self):
        """return the bone mineral content in kg"""
        """old
        if any(self._nones(self.right_body_r)):
            return None
        kg = float(
            0.89328
            * exp(
                -0.47127 * self._ln(self.right_body_r)  # type: ignore
                + 2.65176 * self._ln(self.height)
                - 9.62779
            )
            - 0.12978 * ~self.is_male()
            + 0.35966
        )
        """
        if any(
            self._nones(
                self.weight,
                self.height,
                self.right_body_r_raw,
                self.left_body_r_raw,
                self.right_body_x_raw,
                self.left_body_x_raw,
            )
        ):
            return None
        return float(
            -1.72291
            + 0.01673 * self.weight
            + 0.02881 * (self.height**2) / ((self.right_body_r_raw + self.left_body_r_raw) / 2)  # type: ignore
            + 0.00038 * (((self.right_body_x_raw + self.left_body_x_raw) / 2) ** 2)  # type: ignore
            + 0.00212 * (self.height**2) / ((self.right_body_x_raw + self.left_body_x_raw) / 2)  # type: ignore
        )

    @property
    def lean_soft_mass(self):
        """return the lean soft mass in kg"""
        bmc_kg = self.bone_mineral_content
        ffm_kg = self.fat_free_mass
        if any(self._nones(ffm_kg, bmc_kg)):
            return None
        return float(ffm_kg - bmc_kg)  # type: ignore

    @property
    def skeletal_muscle_mass(self):
        """return the skeletal muscle mass in kg"""

        """old
        if any(self._nones(self.right_body_r)):
            return None
        smm = float(
            +5.102
            + 0.401 * self.height**2 / self.right_body_r  # type: ignore
            - 0.071 * self.age
            + 3.825 * self.is_male()
        )
        if self.is_male():
            b0, b1 = [1.43430, 0.94313]
        else:
            b0, b1 = [0.49926, 1.29378]
        return b0 * smm**b1
        """
        if any(
            self._nones(
                self.height,
                self.age,
                self.weight,
                self.left_body_r_raw,
                self.right_body_r_raw,
                self.left_body_x_raw,
                self.right_body_x_raw,
                self.left_body_phase_angle_raw,
                self.right_body_phase_angle_raw,
                self.left_body_z_raw,
                self.right_body_z_raw,
            )
        ):
            return None
        return float(
            -18.04706
            + 0.10446 * self.weight
            + 0.00543 * self.age
            + 0.42698 * (self.height**2) / ((self.left_body_r_raw + self.right_body_r_raw) / 2)  # type: ignore
            + 0.00170 * (((self.left_body_x_raw + self.right_body_x_raw) / 2) ** 2)  # type: ignore
            + 0.01179 * (self.height**2) / ((self.left_body_z_raw + self.right_body_z_raw) / 2)  # type: ignore
            + 0.20090 * (((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2) ** 2)  # type: ignore
            + 0.00139 * (self.height**2) / ((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2)  # type: ignore
        )

    @property
    def organs_mass(self):
        """return the mass of organs in kg"""
        smm_kg = self.skeletal_muscle_mass
        lst_kg = self.lean_soft_mass
        if any(self._nones(lst_kg, smm_kg)):
            return None
        return float(lst_kg - smm_kg)  # type: ignore

    @property
    def basal_metabolic_rate(self):
        """return the basal metabolic rate in kcal"""

        """old
        ffm_kg = self.fat_free_mass
        if any(self._nones(ffm_kg)):
            return None
        fm_kg = self.fat_mass
        return float(
            +238.85
            * (
                +0.05192 * ffm_kg  # type: ignore
                + 0.04036 * fm_kg  # type: ignore
                + 0.869 * self.is_male()
                - 0.01181 * self.age
                + 2.992
            )
        )
        """
        if any(
            self._nones(
                self.height,
                self.age,
                self.weight,
                self.sex,
                self.left_body_r_raw,
                self.right_body_r_raw,
                self.left_body_x_raw,
                self.right_body_x_raw,
                self.left_body_phase_angle_raw,
                self.right_body_phase_angle_raw,
                self.left_body_z_raw,
                self.right_body_z_raw,
            )
        ):
            return None
        return float(
            -340.40464
            + 3.99739 * self.weight
            + 0.16695 * self.age
            + 14.96410 * (self.height**2) / ((self.left_body_r_raw + self.right_body_r_raw) / 2)  # type: ignore
            + 0.35634 * (self.height**2) / ((self.left_body_z_raw + self.right_body_z_raw) / 2)  # type: ignore
            + 5.66971 * (((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2) ** 2)  # type: ignore
            + 0.05072 * (self.height**2) / ((self.left_body_phase_angle_raw + self.right_body_phase_angle_raw) / 2)  # type: ignore
            + 23.24532 * self.is_male()
            + 6.67914 * ((self.left_body_x_raw + self.right_body_x_raw) / 2)  # type: ignore
        )

    @property
    def _trunk_appendicular_index(self):
        """return the ratio between the trunk and appendicular resistance"""
        if any(
            self._nones(
                self.left_trunk_r,
                self.right_trunk_r,
                self.left_arm_r,
                self.left_leg_r,
                self.right_arm_r,
                self.right_leg_r,
            )
        ):
            return None
        return float(
            2
            * (self.left_trunk_r + self.right_trunk_r)  # type: ignore
            / (self.left_arm_r + self.left_leg_r + self.right_arm_r + self.right_leg_r)  # type: ignore
        )

    @property
    def _trunk_appendicular_index_raw(self):
        """return the ratio between the trunk and appendicular resistance"""
        if any(
            self._nones(
                self.left_trunk_r_raw,
                self.right_trunk_r_raw,
                self.left_arm_r_raw,
                self.left_leg_r_raw,
                self.right_arm_r_raw,
                self.right_leg_r_raw,
            )
        ):
            return None
        return float(
            2
            * (self.left_trunk_r_raw + self.right_trunk_r_raw)  # type: ignore
            / (self.left_arm_r_raw + self.left_leg_r_raw + self.right_arm_r_raw + self.right_leg_r_raw)  # type: ignore
        )

    @property
    def left_arm_fat_free_mass(self):
        """return the left arm fat free mass in kg"""
        if any(self._nones(self.left_arm_r_raw, self._trunk_appendicular_index_raw)):
            return None
        return float(
            +0.676
            + 0.026 * self.height**2 / self.left_arm_r_raw  # type: ignore
            - 11.398 * self._trunk_appendicular_index_raw  # type: ignore
            + 0.346 * self.is_male()
        )

    @property
    def left_arm_fat_mass(self):
        """return the left arm fat mass in kg"""
        if any(self._nones(self.left_arm_phase_angle_raw)):
            return None
        return float(
            -0.420
            + 0.107 * self.bmi
            - 0.216 * self.left_arm_phase_angle_raw  # type: ignore
            - 0.163 * self.is_male()
        )

    @property
    def right_arm_fat_free_mass(self):
        """return the right arm fat free mass in kg"""
        if any(self._nones(self.right_arm_r_raw, self._trunk_appendicular_index_raw)):
            return None
        return float(
            +0.676
            + 0.026 * self.height**2 / self.right_arm_r_raw  # type: ignore
            - 11.398 * self._trunk_appendicular_index_raw  # type: ignore
            + 0.346 * self.is_male()
        )

    @property
    def right_arm_fat_mass(self):
        """return the right arm fat mass in kg"""
        if any(self._nones(self.right_arm_phase_angle_raw, self.bmi)):
            return None
        return float(
            -0.447
            + 0.102 * self.bmi
            - 0.188 * self.right_arm_phase_angle_raw  # type: ignore
            - 0.155 * self.is_male()
        )

    @property
    def left_leg_fat_free_mass(self):
        """return the left leg fat free mass in kg"""
        if any(
            self._nones(
                self.left_leg_r_raw, self._trunk_appendicular_index_raw, self.height
            )
        ):
            return None
        return float(
            +4.756
            + 0.067 * self.height**2 / self.left_leg_r_raw  # type: ignore
            - 54.597 * self._trunk_appendicular_index_raw  # type: ignore
            + 0.901 * self.is_male()
        )

    @property
    def left_leg_fat_mass(self):
        """return the left leg fat mass in kg and as percentage of
        the as percentage of the total fat mass"""
        if any(self._nones(self.left_leg_phase_angle_raw)):
            return None
        return float(
            1.545
            + 0.250 * self.bmi
            - 1.343 * self.is_male()
            - 0.524 * self.left_leg_phase_angle_raw  # type: ignore
        )

    @property
    def right_leg_fat_free_mass(self):
        """return the right leg fat free mass in kg"""
        if any(
            self._nones(
                self.right_leg_r_raw, self._trunk_appendicular_index_raw, self.height
            )
        ):
            return None
        return float(
            +3.724
            + 0.071 * self.height**2 / self.right_leg_r_raw  # type: ignore
            - 46.197 * self._trunk_appendicular_index_raw  # type: ignore
            + 0.733 * self.is_male()
        )

    @property
    def right_leg_fat_mass(self):
        """return the right leg fat mass in kg"""
        if any(self._nones(self.right_leg_phase_angle_raw)):  # type: ignore
            return None
        return float(
            2.731
            + 0.256 * self.bmi
            - 1.286 * self.is_male()
            - 0.7 * self.right_leg_phase_angle_raw  # type: ignore
        )

    @property
    def trunk_fat_free_mass(self):
        """return the trunk fat free mass in kg"""
        if any(
            self._nones(
                self.left_trunk_r_raw,
                self.right_trunk_r_raw,
                self.left_trunk_x_raw,
                self.right_trunk_x_raw,
                self.left_trunk_phase_angle_raw,
                self.right_trunk_phase_angle_raw,
                self.left_trunk_z_raw,
                self.right_trunk_z_raw,
            )
        ):
            return None
        return float(
            -6.19740
            + 0.20178 * self.weight
            + 0.00287 * (self.height**2) / ((self.left_trunk_r_raw + self.right_trunk_r_raw) / 2)  # type: ignore
            + 0.01800 * ((self.left_trunk_x_raw + self.right_trunk_x_raw) / 2) ** 2  # type: ignore
            + 0.00003
            * (self.height**2)
            / ((self.left_trunk_phase_angle_raw + self.right_trunk_phase_angle_raw) / 2)  # type: ignore
            + 2.21723 * self.is_male()
            + 0.00157
            * (self.height**2)
            / ((self.left_trunk_x_raw + self.right_trunk_x_raw) / 2)  # type: ignore
            + 0.00208 * ((self.left_trunk_z_raw + self.right_trunk_z_raw) / 2) ** 2  # type: ignore
        )

    @property
    def trunk_fat_mass(self):
        """return the trunk fat mass in kg"""
        if any(self._nones(self.left_trunk_r, self.right_trunk_r)):
            return None

        return float(
            -26.788
            + 0.978 * self.bmi
            + 0.2225 * (self.left_trunk_r + self.right_trunk_r)  # type: ignore
            + 0.045 * self.age
        )

    @property
    def ideal_weight(self):
        """return the ideal weight of the user"""
        return self.bmi * (2.2 + 3.5 * (self.height / 100 - 1.5))

    def to_dict(self):
        """return all the measures as dictionary"""
        return {
            i: getattr(self, i)
            for i in dir(self)
            if i.split("_")[0] not in ["set", "to", "", "is"]
        }


__all__ = ["CheckupBIA"]
