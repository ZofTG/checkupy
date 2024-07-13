"""module dedicated to the integration of bodycomposition data"""

#! IMPORTS


from math import atan, exp, log, pi, prod
from typing import Literal


#! CLASS


class CheckupBIA:
    """
    an object with attributes:
        'age': age in years
        'sex': "M" or "F"
        'hcm': height in cm
        'wtg': weight in kg
    in addition the dictionary shall contain additional keys with structure:
    "region"_"side"_"measure" where:
        "region": "arm", "leg", "trunk", "body"
        "side": "left", "right", "upper", "lower"
        "measure": "r", "x"
    all labels should be lower case and provide as value the corresponding
    measure in Ohm.
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
    _upper_body_r: int | float | None
    _upper_body_x: int | float | None
    _lower_body_r: int | float | None
    _lower_body_x: int | float | None
    _left_arm_r_betas = (-5.929064, 0.874883)
    _left_arm_x_betas = (3.304037, 0.686138)
    _left_body_r_betas = (29.735312, 0.893878)
    _left_body_x_betas = (-5.850700, 1.077053)
    _left_leg_r_betas = (22.703793, 0.988802)
    _left_leg_x_betas = (-0.196244, 0.988221)
    _left_trunk_r_betas = (2.874024, 0.868278)
    _left_trunk_x_betas = (7.535099, 0.028624)
    _lower_body_r_betas = (52.56977552, 0.948773993)
    _lower_body_x_betas = (-0.823281553, 1.00633072)
    _right_arm_r_betas = (-17.392322, 0.904717)
    _right_arm_x_betas = (1.392877, 0.782267)
    _right_body_r_betas = (-13.248009, 0.971554)
    _right_body_x_betas = (4.612482, 0.886881)
    _right_leg_r_betas = (3.174666, 1.071437)
    _right_leg_x_betas = (-0.259402, 0.991873)
    _right_trunk_r_betas = (0.973686, 1.038562)
    _right_trunk_x_betas = (8.288528, -0.053032)
    _upper_body_r_betas = (-63.78991222, 0.901742825)
    _upper_body_x_betas = (9.520406271, 0.612947206)

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
        upper_body_r: int | float | None = None,
        upper_body_x: int | float | None = None,
        lower_body_r: int | float | None = None,
        lower_body_x: int | float | None = None,
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

        self.set_upper_body_r(upper_body_r, raw_electric_data)
        self.set_upper_body_x(upper_body_x, raw_electric_data)
        self.set_lower_body_r(lower_body_r, raw_electric_data)
        self.set_lower_body_x(lower_body_x, raw_electric_data)

    def _ln(self, x: int | float):
        """return the natural logarithm of x"""
        return log(x, exp(1))

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
        return (
            2
            * (self.left_trunk_r + self.right_trunk_r)  # type: ignore
            / (self.left_arm_r + self.left_leg_r + self.right_arm_r + self.right_leg_r)  # type: ignore
        )

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

    def set_upper_body_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the upper body resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._upper_body_r = r
        else:
            self._upper_body_r = sum(map(prod, zip((1, r), self._upper_body_r_betas)))

    def set_upper_body_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the upper body reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._upper_body_x = x
        else:
            self._upper_body_x = sum(map(prod, zip((1, x), self._upper_body_x_betas)))

    def set_lower_body_r(
        self,
        r: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the lower body resistance in Ohm

        Parameters
        ----------
        r: int | float | None = None
            the input resistance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or r is None:
            self._lower_body_r = r
        else:
            self._lower_body_r = sum(map(prod, zip((1, r), self._lower_body_r_betas)))

    def set_lower_body_x(
        self,
        x: int | float | None = None,
        raw: bool = False,
    ):
        """
        set the lower body reactance in Ohm

        Parameters
        ----------
        x: int | float | None = None
            the input reactance

        raw: bool = False
            is the value raw or corrected?
        """
        if not raw or x is None:
            self._lower_body_x = x
        else:
            self._lower_body_x = sum(map(prod, zip((1, x), self._lower_body_x_betas)))

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
    def upper_body_r(self):
        """the upper body resistance in Ohm"""
        return self._upper_body_r

    @property
    def upper_body_x(self):
        """the upper body reactance in Ohm"""
        return self._upper_body_x

    @property
    def lower_body_r(self):
        """the lower body resistance in Ohm"""
        return self._lower_body_r

    @property
    def lower_body_x(self):
        """the lower body reactance in Ohm"""
        return self._upper_body_x

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
    def lower_body_r_raw(self):
        """return the lower body resistance directly measured from sensors in Ohm"""
        if self.lower_body_r is None:
            return None
        return (
            self.lower_body_r - self._lower_body_r_betas[0]
        ) / self._lower_body_r_betas[1]

    @property
    def lower_body_x_raw(self):
        """return the lower body reactance directly measured from sensors in Ohm"""
        if self.lower_body_x is None:
            return None
        return (
            self.lower_body_x - self._lower_body_x_betas[0]
        ) / self._lower_body_x_betas[1]

    @property
    def upper_body_r_raw(self):
        """return the upper body resistance directly measured from sensors in Ohm"""
        if self.upper_body_r is None:
            return None
        return (
            self.upper_body_r - self._upper_body_r_betas[0]
        ) / self._upper_body_r_betas[1]

    @property
    def upper_body_x_raw(self):
        """return the upper body reactance directly measured from sensors in Ohm"""
        if self.upper_body_x is None:
            return None
        return (
            self.upper_body_x - self._upper_body_x_betas[0]
        ) / self._upper_body_x_betas[1]

    @property
    def left_arm_phase_angle(self):
        """return the left arm phase angle in degrees"""
        return self._phase_angle_deg(self.left_arm_r, self.left_arm_x)

    @property
    def left_leg_phase_angle(self):
        """return the left leg phase angle in degrees"""
        return self._phase_angle_deg(self.left_leg_r, self.left_leg_x)

    @property
    def left_trunk_phase_angle(self):
        """return the left trunk phase angle in degrees"""
        return self._phase_angle_deg(self.left_trunk_r, self.left_trunk_x)

    @property
    def left_body_phase_angle(self):
        """return the left body phase angle in degrees"""
        return self._phase_angle_deg(self.left_body_r, self.left_body_x)

    @property
    def right_arm_phase_angle(self):
        """return the right arm phase angle in degrees"""
        return self._phase_angle_deg(self.right_arm_r, self.right_arm_x)

    @property
    def right_leg_phase_angle(self):
        """return the right leg phase angle in degrees"""
        return self._phase_angle_deg(self.right_leg_r, self.right_leg_x)

    @property
    def right_trunk_phase_angle(self):
        """return the right trunk phase angle in degrees"""
        return self._phase_angle_deg(self.right_trunk_r, self.right_trunk_x)

    @property
    def right_body_phase_angle(self):
        """return the right body phase angle in degrees"""
        return self._phase_angle_deg(self.right_body_r, self.right_body_x)

    @property
    def upper_body_phase_angle(self):
        """return the upper body phase angle in degrees"""
        return self._phase_angle_deg(self.upper_body_r, self.upper_body_x)

    @property
    def lower_body_phase_angle(self):
        """return the lower body phase angle in degrees"""
        return self._phase_angle_deg(self.lower_body_r, self.lower_body_x)

    def is_male(self):
        """return True if the user is declared as male"""
        return self.sex == "M"

    @property
    def total_body_water(self):
        """return the total body water in liters and as percentage
        of the total body weight"""
        if any(self._nones(self.right_body_r)):
            return None, None
        lt = float(
            +0.286
            + 0.195 * self.height**2 / self.right_body_r  # type: ignore
            + 0.385 * self.weight
            + 5.086 * self.is_male()
        )
        return lt, lt / self.weight

    @property
    def extra_cellular_water(self):
        """return the extracellular water in liters and as percentage
        of the total body water"""
        if any(self._nones(self.right_body_r, self.right_body_x)):
            return None, None
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
        ecw = b0 * lt**b1
        tbw = self.total_body_water[0]  # type: ignore
        rl = (ecw / tbw) if tbw is not None else None
        return ecw, rl

    @property
    def intra_cellular_water(self):
        """return the intracellular water in liters and as percentage
        of the total body water"""
        tbw_lt = self.total_body_water[0]  # type: ignore
        ecw_lt, ecw_rl = self.extra_cellular_water  # type: ignore
        if any(self._nones(tbw_lt, ecw_lt)):
            icw = None
        else:
            icw = float(tbw_lt - ecw_lt)  # type: ignore
        if any(self._nones(ecw_rl)):
            rl = None
        else:
            rl = float(1 - ecw_rl)  # type: ignore
        return icw, rl

    @property
    def bmi(self):
        """return the user BMI"""
        return self.weight / (self.height / 100) ** 2

    @property
    def fat_free_mass(self):
        """return the free-fat mass in kg and as percentage
        of the total body weight"""
        if any(self._nones(self.right_body_r, self.right_body_x)):
            return None, None
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
        return ffm, ffm / self.weight

    @property
    def fat_mass(self):
        """return the fat mass in kg and as percentage of the total body weight"""
        if any(self._nones(self.fat_free_mass)):
            return None, None
        ffm_kg, ffm_rl = self.fat_free_mass
        return float(self.weight - ffm_kg), float(1 - ffm_rl)  # type: ignore

    @property
    def bone_mineral_content(self):
        """return the bone mineral content in kg and as percentage of the
        user body weight"""
        if any(self._nones(self.right_body_r)):
            return None, None
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
        return kg, kg / self.weight

    @property
    def lean_soft_mass(self):
        """return the lean soft mass in kg and as percentage of the user
        body weight"""
        bmc_kg, bmc_rl = self.bone_mineral_content
        ffm_kg, ffm_rl = self.fat_free_mass
        if any(self._nones(ffm_kg, bmc_kg)):
            lst_kg = None
        else:
            lst_kg = float(ffm_kg - bmc_kg)  # type: ignore
        if any(self._nones(ffm_rl, bmc_rl)):
            lst_rl = None
        else:
            lst_rl = float(ffm_rl - bmc_rl)  # type: ignore
        return lst_kg, lst_rl

    @property
    def skeletal_muscle_mass(self):
        """return the skeletal muscle mass in kg and as percentage of the total body weight"""
        if any(self._nones(self.right_body_r)):
            return None, None
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
        smm = b0 * smm**b1
        return smm, smm / self.weight

    @property
    def organs_mass(self):
        """return the mass of organs in kg and as percentage of the total body weight"""
        smm_kg, smm_rl = self.skeletal_muscle_mass
        lst_kg, lst_rl = self.lean_soft_mass
        if any(self._nones(lst_kg, smm_kg)):
            orm_kg = None
        else:
            orm_kg = float(lst_kg - smm_kg)  # type: ignore
        if any(self._nones(smm_rl, lst_rl)):
            orm_rl = None
        else:
            orm_rl = float(lst_rl - smm_rl)  # type: ignore
        return orm_kg, orm_rl

    @property
    def left_arm_skeletal_muscle_mass(self):
        """return the left arm skeletal muscle mass in kg and as percentage of
        the total skeletal muscle mass"""
        if any(self._nones(self.left_arm_r, self._trunk_appendicular_index)):
            return None, None
        smm = float(
            +0.676
            + 0.026 * self.height**2 / self.left_arm_r  # type: ignore
            - 11.398 * self._trunk_appendicular_index  # type: ignore
            + 0.346 * self.is_male()
        )
        tot = self.skeletal_muscle_mass[0]
        if tot is None:
            prc = None
        else:
            prc = float(smm / tot)
        return smm, prc

    @property
    def right_arm_skeletal_muscle_mass(self):
        """return the right arm skeletal muscle mass in kg and as percentage of
        the total skeletal muscle mass"""
        if any(self._nones(self.right_arm_r, self._trunk_appendicular_index)):
            return None, None
        smm = float(
            +1.034
            + 0.024 * self.height**2 / self.right_arm_r  # type: ignore
            - 12.272 * self._trunk_appendicular_index  # type: ignore
            + 0.388 * self.is_male()
        )
        tot = self.skeletal_muscle_mass[0]
        if tot is None:
            prc = None
        else:
            prc = float(smm / tot)
        return smm, prc

    @property
    def left_leg_skeletal_muscle_mass(self):
        """return the left leg skeletal muscle mass in kg and as percentage of
        the total skeletal muscle mass"""
        if any(self._nones(self.left_leg_r, self._trunk_appendicular_index)):
            return None, None
        smm = float(
            +4.756
            + 0.067 * self.height**2 / self.left_leg_r  # type: ignore
            - 54.597 * self._trunk_appendicular_index  # type: ignore
            + 0.901 * self.is_male()
        )
        tot = self.skeletal_muscle_mass[0]
        if tot is None:
            prc = None
        else:
            prc = float(smm / tot)
        return smm, prc

    @property
    def right_leg_skeletal_muscle_mass(self):
        """return the right leg skeletal muscle mass in kg and as percentage of
        the total skeletal muscle mass"""
        if any(self._nones(self.right_leg_r, self._trunk_appendicular_index)):
            return None, None
        smm = float(
            +3.724
            + 0.071 * self.height**2 / self.right_leg_r  # type: ignore
            - 46.197 * self._trunk_appendicular_index  # type: ignore
            + 0.733 * self.is_male()
        )
        tot = self.skeletal_muscle_mass[0]
        if tot is None:
            prc = None
        else:
            prc = float(smm / tot)
        return smm, prc

    @property
    def trunk_skeletal_muscle_mass(self):
        """return the trunk skeletal muscle mass in kg and as percentage of
        the total skeletal muscle mass"""
        lamm = self.left_arm_skeletal_muscle_mass[0]
        llmm = self.left_leg_skeletal_muscle_mass[0]
        ramm = self.right_arm_skeletal_muscle_mass[0]
        rlmm = self.right_leg_skeletal_muscle_mass[0]
        smm_kg = self.skeletal_muscle_mass[0]
        if any(self._nones(lamm, llmm, ramm, rlmm, smm_kg)):
            return None, None
        tmm = float(smm_kg - lamm - ramm - llmm - rlmm)  # type: ignore
        return tmm, float(tmm / smm_kg)  # type: ignore

    @property
    def left_arm_fat_mass(self):
        """return the left arm fat mass in kg and as percentage of
        the as percentage of the total fat mass"""
        if any(self._nones(self.left_arm_phase_angle)):
            return None, None
        sfm = float(
            -0.420
            + 0.107 * self.bmi
            - 0.216 * self.left_arm_phase_angle  # type: ignore
            - 0.163 * self.is_male()
        )
        tot = self.fat_mass[0]
        if tot is None:
            prc = None
        else:
            prc = float(sfm / tot)
        return sfm, prc

    @property
    def left_leg_fat_mass(self):
        """return the left leg fat mass in kg and as percentage of
        the as percentage of the total fat mass"""
        if any(self._nones(self.left_leg_phase_angle)):
            return None, None
        sfm = float(
            1.545
            + 0.250 * self.bmi
            - 1.343 * self.is_male()
            - 0.524 * self.left_leg_phase_angle  # type: ignore
        )
        tot = self.fat_mass[0]
        if tot is None:
            prc = None
        else:
            prc = float(sfm / tot)
        return sfm, prc

    @property
    def right_arm_fat_mass(self):
        """return the right arm fat mass in kg and as percentage of
        the as percentage of the total fat mass"""
        if any(self._nones(self.right_arm_phase_angle)):
            return None, None
        sfm = float(
            -0.447
            + 0.102 * self.bmi
            - 0.188 * self.right_arm_phase_angle  # type: ignore
            - 0.155 * self.is_male()
        )
        tot = self.fat_mass[0]
        if tot is None:
            prc = None
        else:
            prc = float(sfm / tot)
        return sfm, prc

    @property
    def right_leg_fat_mass(self):
        """return the right leg fat mass in kg and as percentage of
        the as percentage of the total fat mass"""
        if any(self._nones(self.right_leg_phase_angle)):  # type: ignore
            return None, None
        sfm = float(
            2.731
            + 0.256 * self.bmi
            - 1.286 * self.is_male()
            - 0.7 * self.right_leg_phase_angle  # type: ignore
        )
        tot = self.fat_mass[0]
        if tot is None:
            prc = None
        else:
            prc = float(sfm / tot)
        return sfm, prc

    @property
    def trunk_fat_mass(self):
        """return the trunk fat mass in kg and as percentage of
        the total fat mass"""
        lafm = self.left_arm_fat_mass[0]
        llfm = self.left_leg_fat_mass[0]
        rafm = self.right_arm_fat_mass[0]
        rlfm = self.right_leg_fat_mass[0]
        fm_kg = self.fat_mass[0]
        if any(self._nones(lafm, llfm, rafm, rlfm, fm_kg)):
            return None, None
        tfm = float(fm_kg - lafm - rafm - llfm - rlfm)  # type: ignore
        """
        tfm = float(
            -26.788
            + 0.978 * self.bmi
            + 0.2225 * (self.left_trunk_r + self.right_trunk_r)  # type: ignore
            + 0.045 * self.age
        )
        """
        return tfm, float(tfm / fm_kg)  # type: ignore

    @property
    def basal_metabolic_rate(self):
        """return the basal metabolic rate in kcal"""
        ffm_kg = self.fat_free_mass[0]
        if any(self._nones(ffm_kg)):
            return None
        fm_kg = self.weight - ffm_kg  # type: ignore
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
