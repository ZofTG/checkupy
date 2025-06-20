"""module dedicated to the integration of bodycomposition data"""

#! IMPORTS


from copy import deepcopy
from math import atan, exp, log, pi, prod
from typing import Literal
from .onnx_models import OnnxModel
import numpy as np
from os.path import join, dirname

__all__ = ["CheckupBIA"]


#! CLASS


class BIAInput:
    """
    an object allowing the calculation of body composition data from
    anthropometric and electric data.
    """

    # variables
    _age: int
    _sex: Literal["M", "F"]
    _hcm: int
    _wgt: float
    _left_arm_resistance: int | float
    _left_arm_reactance: int | float
    _left_trunk_resistance: int | float
    _left_trunk_reactance: int | float
    _left_leg_resistance: int | float
    _left_leg_reactance: int | float
    _left_body_resistance: int | float
    _left_body_reactance: int | float
    _right_arm_resistance: int | float
    _right_arm_reactance: int | float
    _right_trunk_resistance: int | float
    _right_trunk_reactance: int | float
    _right_leg_resistance: int | float
    _right_leg_reactance: int | float
    _right_body_resistance: int | float
    _right_body_reactance: int | float
    _corrected: bool

    # orthostatic correction coefficients
    _left_arm_resistance_betas = (-5.929064, 0.874883)
    _left_arm_reactance_betas = (3.304037, 0.686138)
    _left_body_resistance_betas = (29.735312, 0.893878)
    _left_body_reactance_betas = (-5.850700, 1.077053)
    _left_leg_resistance_betas = (22.703793, 0.988802)
    _left_leg_reactance_betas = (-0.196244, 0.988221)
    _left_trunk_resistance_betas = (2.874024, 0.868278)
    _left_trunk_reactance_betas = (7.535099, 0.028624)
    _right_arm_resistance_betas = (-17.392322, 0.904717)
    _right_arm_reactance_betas = (1.392877, 0.782267)
    _right_body_resistance_betas = (-13.248009, 0.971554)
    _right_body_reactance_betas = (4.612482, 0.886881)
    _right_leg_resistance_betas = (3.174666, 1.071437)
    _right_leg_reactance_betas = (-0.259402, 0.991873)
    _right_trunk_resistance_betas = (0.973686, 1.038562)
    _right_trunk_reactance_betas = (8.288528, -0.053032)

    def __init__(
        self,
        age: int | float,
        sex: Literal["M", "F"],
        height: int,
        weight: int | float,
        left_arm_resistance: int | float,
        left_arm_reactance: int | float,
        left_trunk_resistance: int | float,
        left_trunk_reactance: int | float,
        left_leg_resistance: int | float,
        left_leg_reactance: int | float,
        left_body_resistance: int | float,
        left_body_reactance: int | float,
        right_arm_resistance: int | float,
        right_arm_reactance: int | float,
        right_trunk_resistance: int | float,
        right_trunk_reactance: int | float,
        right_leg_resistance: int | float,
        right_leg_reactance: int | float,
        right_body_resistance: int | float,
        right_body_reactance: int | float,
        corrected_electrical_values: bool = False,
    ):
        self.set_age(age)
        self.set_sex(sex)
        self.set_height(height)
        self.set_weight(weight)

        self.set_left_arm_resistance(left_arm_resistance)
        self.set_left_arm_reactance(left_arm_reactance)
        self.set_left_leg_resistance(left_leg_resistance)
        self.set_left_leg_reactance(left_leg_reactance)
        self.set_left_trunk_resistance(left_trunk_resistance)
        self.set_left_trunk_reactance(left_trunk_reactance)
        self.set_left_body_resistance(left_body_resistance)
        self.set_left_body_reactance(left_body_reactance)

        self.set_right_arm_resistance(right_arm_resistance)
        self.set_right_arm_reactance(right_arm_reactance)
        self.set_right_leg_resistance(right_leg_resistance)
        self.set_right_leg_reactance(right_leg_reactance)
        self.set_right_trunk_resistance(right_trunk_resistance)
        self.set_right_trunk_reactance(right_trunk_reactance)
        self.set_right_body_resistance(right_body_resistance)
        self.set_right_body_reactance(right_body_reactance)

        # check if the electrical data are corrected for orthostatism
        self._corrected = corrected_electrical_values
        if self.is_corrected():
            self.remove_orthostatic_correction()

    def _phaseangle_deg(
        self,
        res: float | int,
        rea: float | int,
    ):
        """return the phase angle in degrees"""
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

    def set_left_arm_resistance(self, r: int | float):
        """
        set the left arm resistance in Ohm

        Parameters
        ----------
        r: int | float
            the input resistance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._left_arm_resistance = r

    def set_left_arm_reactance(self, r: int | float):
        """
        set the left arm reactance in Ohm

        Parameters
        ----------
        r: int | float
            the input reactance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._left_arm_reactance = r

    def set_left_leg_resistance(self, r: int | float):
        """
        set the left leg resistance in Ohm

        Parameters
        ----------
        r: int | float
            the input resistance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._left_leg_resistance = r

    def set_left_leg_reactance(self, r: int | float):
        """
        set the left leg reactance in Ohm

        Parameters
        ----------
        r: int | float
            the input reactance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._left_leg_reactance = r

    def set_left_trunk_resistance(self, r: int | float):
        """
        set the left trunk resistance in Ohm

        Parameters
        ----------
        r: int | float
            the input resistance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._left_trunk_resistance = r

    def set_left_trunk_reactance(self, r: int | float):
        """
        set the left trunk reactance in Ohm

        Parameters
        ----------
        r: int | float
            the input reactance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._left_trunk_reactance = r

    def set_left_body_resistance(self, r: int | float):
        """
        set the left body resistance in Ohm

        Parameters
        ----------
        r: int | float
            the input resistance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._left_body_resistance = r

    def set_left_body_reactance(self, r: int | float):
        """
        set the left body reactance in Ohm

        Parameters
        ----------
        r: int | float
            the input reactance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._left_body_reactance = r

    def set_right_arm_resistance(self, r: int | float):
        """
        set the right arm resistance in Ohm

        Parameters
        ----------
        r: int | float
            the input resistance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._right_arm_resistance = r

    def set_right_arm_reactance(self, r: int | float):
        """
        set the right arm reactance in Ohm

        Parameters
        ----------
        r: int | float
            the input reactance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._right_arm_reactance = r

    def set_right_leg_resistance(self, r: int | float):
        """
        set the right leg resistance in Ohm

        Parameters
        ----------
        r: int | float
            the input resistance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._right_leg_resistance = r

    def set_right_leg_reactance(self, r: int | float):
        """
        set the right leg reactance in Ohm

        Parameters
        ----------
        r: int | float
            the input reactance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._right_leg_reactance = r

    def set_right_trunk_resistance(self, r: int | float):
        """
        set the right trunk resistance in Ohm

        Parameters
        ----------
        r: int | float
            the input resistance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._right_trunk_resistance = r

    def set_right_trunk_reactance(self, r: int | float):
        """
        set the right trunk reactance in Ohm

        Parameters
        ----------
        r: int | float
            the input reactance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._right_trunk_reactance = r

    def set_right_body_resistance(self, r: int | float):
        """
        set the right body resistance in Ohm

        Parameters
        ----------
        r: int | float
            the input resistance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._right_body_resistance = r

    def set_right_body_reactance(self, r: int | float):
        """
        set the right body reactance in Ohm

        Parameters
        ----------
        r: int | float
            the input reactance

        corrected_electrical_value: bool = False
            is the value raw or corrected?
        """
        self._right_body_reactance = r

    def to_dict(self):
        """return all the measures as dictionary"""
        return {
            i: getattr(self, i)
            for i in dir(self)
            if i.split("_")[0]
            not in ["set", "to", "", "is", "fitness", "standard", "copy", "apply"]
        }

    def is_male(self):
        """return True if the user is declared as male"""
        return self.sex == "M"

    def is_corrected(self):
        """return true if the electrical data are corrected for orthostaticity"""
        return self._corrected

    def apply_orthostatic_correction(self):
        """If not applied, apply orthostatic correction to the stored electrical data"""
        if not self.is_corrected():

            def lsq(x, y):
                return sum(list(map(lambda x: prod(x), list(zip([1, x], y)))))

            self.set_left_arm_resistance(
                lsq(self.left_arm_resistance, self._left_arm_resistance_betas)
            )
            self.set_left_arm_reactance(
                lsq(self.left_arm_reactance, self._left_arm_reactance_betas)
            )
            self.set_left_leg_resistance(
                lsq(self.left_leg_resistance, self._left_leg_resistance_betas)
            )
            self.set_left_leg_reactance(
                lsq(self.left_leg_reactance, self._left_leg_reactance_betas)
            )
            self.set_left_trunk_resistance(
                lsq(self.left_trunk_resistance, self._left_trunk_resistance_betas)
            )
            self.set_left_trunk_reactance(
                lsq(self.left_trunk_reactance, self._left_trunk_reactance_betas)
            )
            self.set_left_body_resistance(
                lsq(self.left_body_resistance, self._left_body_resistance_betas)
            )
            self.set_left_body_reactance(
                lsq(self.left_body_reactance, self._left_body_reactance_betas)
            )
            self.set_right_arm_resistance(
                lsq(self.right_arm_resistance, self._right_arm_resistance_betas)
            )
            self.set_right_arm_reactance(
                lsq(self.right_arm_reactance, self._right_arm_reactance_betas)
            )
            self.set_right_leg_resistance(
                lsq(self.right_leg_resistance, self._right_leg_resistance_betas)
            )
            self.set_right_leg_reactance(
                lsq(self.right_leg_reactance, self._right_leg_reactance_betas)
            )
            self.set_right_trunk_resistance(
                lsq(self.right_trunk_resistance, self._right_trunk_resistance_betas)
            )
            self.set_right_trunk_reactance(
                lsq(self.right_trunk_reactance, self._right_trunk_reactance_betas)
            )
            self.set_right_body_resistance(
                lsq(self.right_body_resistance, self._right_body_resistance_betas)
            )
            self.set_right_body_reactance(
                lsq(self.right_body_reactance, self._right_body_reactance_betas)
            )

    def remove_orthostatic_correction(self):
        """If already applied, remove orthostatic correction from electrical data"""
        if self.is_corrected():

            def ilsq(x, y):
                return (x - y[0]) / y[1]

            self.set_left_arm_resistance(
                ilsq(self.left_arm_resistance, self._left_arm_resistance_betas)
            )
            self.set_left_arm_reactance(
                ilsq(self.left_arm_reactance, self._left_arm_reactance_betas)
            )
            self.set_left_leg_resistance(
                ilsq(self.left_leg_resistance, self._left_leg_resistance_betas)
            )
            self.set_left_leg_reactance(
                ilsq(self.left_leg_reactance, self._left_leg_reactance_betas)
            )
            self.set_left_trunk_resistance(
                ilsq(self.left_trunk_resistance, self._left_trunk_resistance_betas)
            )
            self.set_left_trunk_reactance(
                ilsq(self.left_trunk_reactance, self._left_trunk_reactance_betas)
            )
            self.set_left_body_resistance(
                ilsq(self.left_body_resistance, self._left_body_resistance_betas)
            )
            self.set_left_body_reactance(
                ilsq(self.left_body_reactance, self._left_body_reactance_betas)
            )
            self.set_right_arm_resistance(
                ilsq(self.right_arm_resistance, self._right_arm_resistance_betas)
            )
            self.set_right_arm_reactance(
                ilsq(self.right_arm_reactance, self._right_arm_reactance_betas)
            )
            self.set_right_leg_resistance(
                ilsq(self.right_leg_resistance, self._right_leg_resistance_betas)
            )
            self.set_right_leg_reactance(
                ilsq(self.right_leg_reactance, self._right_leg_reactance_betas)
            )
            self.set_right_trunk_resistance(
                ilsq(self.right_trunk_resistance, self._right_trunk_resistance_betas)
            )
            self.set_right_trunk_reactance(
                ilsq(self.right_trunk_reactance, self._right_trunk_reactance_betas)
            )
            self.set_right_body_resistance(
                ilsq(self.right_body_resistance, self._right_body_resistance_betas)
            )
            self.set_right_body_reactance(
                ilsq(self.right_body_reactance, self._right_body_reactance_betas)
            )

    def copy(self):
        """create a copy of the object"""
        return deepcopy(self)

    def is_valid(self):
        """returns True if the measure is valid from an electrical standpoint"""
        hgt = self.height / 100
        pha = {}
        valid = 1
        for side in ["left", "right"]:
            res = getattr(self, f"{side}_body_resistance")
            rea = getattr(self, f"{side}_body_reactance")
            pha[side] = getattr(self, f"{side}_body_phaseangle")
            valid *= res / hgt >= 200
            valid *= res / hgt <= 600
            valid *= rea / hgt >= 10
            valid *= rea / hgt <= 60
            valid *= pha[side] >= 3
            valid *= pha[side] <= 12
        valid *= abs(pha["left"] - pha["right"]) <= 1
        return bool(valid)

    @property
    def _trunk_appendicular_index(self):
        """return the ratio between the trunk and appendicular resistance"""
        return float(
            2
            * (self.left_trunk_resistance + self.right_trunk_resistance)  # type: ignore
            / (self.left_arm_resistance + self.left_leg_resistance + self.right_arm_resistance + self.right_leg_resistance)  # type: ignore
        )

    @property
    def bmi(self):
        """return the user BMI"""
        return self.weight / (self.height / 100) ** 2

    @property
    def target_weight(self):
        """return the ideal weight of the user"""
        return self.bmi * (2.2 + 3.5 * (self.height / 100 - 1.5))

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
    def left_arm_resistance(self):
        """the left arm resistance in Ohm"""
        return self._left_arm_resistance

    @property
    def left_arm_reactance(self):
        """the left arm reactance in Ohm"""
        return self._left_arm_reactance

    @property
    def left_arm_impedance(self):
        """the left arm impedance in Ohm"""
        return (self.left_arm_resistance**2 + self.left_arm_reactance**2) ** 0.5

    @property
    def left_arm_phaseangle(self):
        """the left arm phase angle in degrees"""
        return self._phaseangle_deg(self.left_arm_resistance, self.left_arm_reactance)

    @property
    def left_leg_resistance(self):
        """the left leg resistance in Ohm"""
        return self._left_leg_resistance

    @property
    def left_leg_reactance(self):
        """set the left leg reactance in Ohm"""
        return self._left_leg_reactance

    @property
    def left_leg_impedance(self):
        """the left leg impedance in Ohm"""
        return (self.left_leg_resistance**2 + self.left_leg_reactance**2) ** 0.5

    @property
    def left_leg_phaseangle(self):
        """the left leg phase angle in degrees"""
        return self._phaseangle_deg(self.left_leg_resistance, self.left_leg_reactance)

    @property
    def left_trunk_resistance(self):
        """the left trunk resistance in Ohm"""
        return self._left_trunk_resistance

    @property
    def left_trunk_reactance(self):
        """the left trunk reactance in Ohm"""
        return self._left_trunk_reactance

    @property
    def left_trunk_impedance(self):
        """the left trunk impedance in Ohm"""
        return (self.left_trunk_resistance**2 + self.left_trunk_reactance**2) ** 0.5

    @property
    def left_trunk_phaseangle(self):
        """the left trunk phase angle in degrees"""
        return self._phaseangle_deg(
            self.left_trunk_resistance, self.left_trunk_reactance
        )

    @property
    def left_body_resistance(self):
        """the left body resistance in Ohm"""
        return self._left_body_resistance

    @property
    def left_body_reactance(self):
        """the left body reactance in Ohm"""
        return self._left_body_reactance

    @property
    def left_body_impedance(self):
        """the left body impedance in Ohm"""
        return (self.left_body_resistance**2 + self.left_body_reactance**2) ** 0.5

    @property
    def left_body_phaseangle(self):
        """the left body phase angle in degrees"""
        return self._phaseangle_deg(self.left_body_resistance, self.left_body_reactance)

    @property
    def right_arm_resistance(self):
        """the right arm resistance in Ohm"""
        return self._right_arm_resistance

    @property
    def right_arm_reactance(self):
        """the right arm reactance in Ohm"""
        return self._right_arm_reactance

    @property
    def right_arm_impedance(self):
        """the right arm impedance in Ohm"""
        return (self.right_arm_resistance**2 + self.right_arm_reactance**2) ** 0.5

    @property
    def right_arm_phaseangle(self):
        """the right arm phase angle in degrees"""
        return self._phaseangle_deg(self.right_arm_resistance, self.right_arm_reactance)

    @property
    def right_leg_resistance(self):
        """the right leg resistance in Ohm"""
        return self._right_leg_resistance

    @property
    def right_leg_reactance(self):
        """the right leg reactance in Ohm"""
        return self._right_leg_reactance

    @property
    def right_leg_impedance(self):
        """the right leg impedance in Ohm"""
        return (self.right_leg_resistance**2 + self.right_leg_reactance**2) ** 0.5

    @property
    def right_leg_phaseangle(self):
        """the right leg phase angle in degrees"""
        return self._phaseangle_deg(self.right_leg_resistance, self.right_leg_reactance)

    @property
    def right_trunk_resistance(self):
        """the right trunk resistance in Ohm"""
        return self._right_trunk_resistance

    @property
    def right_trunk_reactance(self):
        """the right trunk reactance in Ohm"""
        return self._right_trunk_reactance

    @property
    def right_trunk_impedance(self):
        """the right trunk impedance in Ohm"""
        return (self.right_trunk_resistance**2 + self.right_trunk_reactance**2) ** 0.5

    @property
    def right_trunk_phaseangle(self):
        """the right trunk phase angle in degrees"""
        return self._phaseangle_deg(
            self.right_trunk_resistance, self.right_trunk_reactance
        )

    @property
    def right_body_resistance(self):
        """the right body resistance in Ohm"""
        return self._right_body_resistance

    @property
    def right_body_reactance(self):
        """the right body reactance in Ohm"""
        return self._right_body_reactance

    @property
    def right_body_impedance(self):
        """the right body impedance in Ohm"""
        return (self.right_body_resistance**2 + self.right_body_reactance**2) ** 0.5

    @property
    def right_body_phaseangle(self):
        """the right body phase angle in degrees"""
        return self._phaseangle_deg(
            self.right_body_resistance, self.right_body_reactance
        )

    @property
    def total_arm_resistance(self):
        """return the average arm resistance in ohm"""
        return (self.left_arm_resistance + self.right_arm_resistance) / 2

    @property
    def total_arm_reactance(self):
        """return the average arm reactance in ohm"""
        return (self.left_arm_reactance + self.right_arm_reactance) / 2

    @property
    def total_arm_impedance(self):
        """the average arm impedance in Ohm"""
        return (self.right_arm_impedance + self.left_arm_impedance) / 2

    @property
    def total_arm_phaseangle(self):
        """the average arm phase angle in degrees"""
        return (self.right_arm_phaseangle + self.left_arm_phaseangle) / 2

    @property
    def total_leg_resistance(self):
        """return the average leg resistance in ohm"""
        return (self.left_leg_resistance + self.right_leg_resistance) / 2

    @property
    def total_leg_reactance(self):
        """return the average leg reactance in ohm"""
        return (self.left_leg_reactance + self.right_leg_reactance) / 2

    @property
    def total_leg_impedance(self):
        """the average leg impedance in Ohm"""
        return (self.right_leg_impedance + self.left_leg_impedance) / 2

    @property
    def total_leg_phaseangle(self):
        """the average leg phase angle in degrees"""
        return (self.right_leg_phaseangle + self.left_leg_phaseangle) / 2

    @property
    def total_trunk_resistance(self):
        """return the average trunk resistance in ohm"""
        return (self.left_trunk_resistance + self.right_trunk_resistance) / 2

    @property
    def total_trunk_reactance(self):
        """return the average trunk reactance in ohm"""
        return (self.left_trunk_reactance + self.right_trunk_reactance) / 2

    @property
    def total_trunk_impedance(self):
        """the average trunk impedance in Ohm"""
        return (self.right_trunk_impedance + self.left_trunk_impedance) / 2

    @property
    def total_trunk_phaseangle(self):
        """the average trunk phase angle in degrees"""
        return (self.right_trunk_phaseangle + self.left_trunk_phaseangle) / 2

    @property
    def total_body_resistance(self):
        """return the average body resistance in ohm"""
        return (self.left_body_resistance + self.right_body_resistance) / 2

    @property
    def total_body_reactance(self):
        """return the average body reactance in ohm"""
        return (self.left_body_reactance + self.right_body_reactance) / 2

    @property
    def total_body_impedance(self):
        """the average body impedance in Ohm"""
        return (self.right_body_impedance + self.left_body_impedance) / 2

    @property
    def total_body_phaseangle(self):
        """the average body phase angle in degrees"""
        return (self.right_body_phaseangle + self.left_body_phaseangle) / 2


class Fitness(BIAInput):
    """
    an object allowing the calculation of body composition data from
    anthropometric and electric data.
    """

    def __init__(
        self,
        age: int | float,
        sex: Literal["M", "F"],
        height: int,
        weight: int | float,
        left_arm_resistance: int | float,
        left_arm_reactance: int | float,
        left_trunk_resistance: int | float,
        left_trunk_reactance: int | float,
        left_leg_resistance: int | float,
        left_leg_reactance: int | float,
        left_body_resistance: int | float,
        left_body_reactance: int | float,
        right_arm_resistance: int | float,
        right_arm_reactance: int | float,
        right_trunk_resistance: int | float,
        right_trunk_reactance: int | float,
        right_leg_resistance: int | float,
        right_leg_reactance: int | float,
        right_body_resistance: int | float,
        right_body_reactance: int | float,
        corrected_electrical_values=False,
    ):
        super().__init__(
            age=age,
            sex=sex,
            height=height,
            weight=weight,
            left_arm_resistance=left_arm_resistance,
            left_arm_reactance=left_arm_reactance,
            left_leg_resistance=left_leg_resistance,
            left_leg_reactance=left_leg_reactance,
            left_trunk_resistance=left_trunk_resistance,
            left_trunk_reactance=left_trunk_reactance,
            left_body_resistance=left_body_resistance,
            left_body_reactance=left_body_reactance,
            right_arm_resistance=right_arm_resistance,
            right_arm_reactance=right_arm_reactance,
            right_leg_resistance=right_leg_resistance,
            right_leg_reactance=right_leg_reactance,
            right_trunk_resistance=right_trunk_resistance,
            right_trunk_reactance=right_trunk_reactance,
            right_body_resistance=right_body_resistance,
            right_body_reactance=right_body_reactance,
            corrected_electrical_values=corrected_electrical_values,
        )
        self.remove_orthostatic_correction()

    @property
    def total_body_water(self):
        """return the total body water in liters and as percentage
        of the total body weight"""
        return float(
            -17.75953
            + 0.12309 * self.weight
            + 0.00734 * self.age
            + 0.55780 * (self.height**2) / self.total_body_resistance
            + 0.00208 * (self.total_body_reactance**2)
            + 0.01627 * (self.height**2) / self.total_body_impedance
            + 0.16738 * (self.total_body_phaseangle**2)
            + 0.00152 * (self.height**2) / self.total_body_phaseangle
        )

    @property
    def total_body_waterperc(self):
        """return the total body water as percentage of the body weight"""
        return self.total_body_water / self.weight * 100

    @property
    def total_body_extracellularwater(self):
        """return the extracellular water in liters"""
        return float(
            -5.27113
            + 0.04381 * self.weight
            + 0.00320 * self.age
            + 0.22309 * (self.height**2) / self.total_body_resistance
            + 0.00081 * (self.total_body_reactance**2)
            + 0.01760 * (self.height**2) / self.total_body_impedance
            + 0.00592 * (self.total_body_phaseangle**2)
            + 0.00041 * (self.height**2) / self.total_body_phaseangle
        )

    @property
    def total_body_extracellularwaterperc(self):
        """
        return the total body extracellular water as percentage of the total
        body water
        """
        return self.total_body_extracellularwater / self.total_body_water * 100

    @property
    def total_body_intracellularwater(self):
        """return the intracellular water in liters"""
        return self.total_body_water - self.total_body_extracellularwater

    @property
    def total_body_intracellularwaterperc(self):
        """
        return the total body intracellular water as percentage of the total
        body water
        """
        return 100 - self.total_body_extracellularwaterperc

    @property
    def total_body_fatfreemass(self):
        """return the free-fat mass in kg"""
        return float(
            -25.08860
            + 0.17591 * self.weight
            + 0.01007 * self.age
            + 0.73751 * (self.height**2) / self.total_body_resistance
            + 0.00294 * (self.total_body_reactance**2)
            + 0.02856 * (self.height**2) / self.total_body_impedance
            + 0.24395 * (self.total_body_phaseangle**2)
            + 0.00217 * (self.height**2) / self.total_body_phaseangle
        )

    @property
    def total_body_fatfreemassindex(self):
        """return the total body fat free mass index"""
        return self.total_body_fatfreemass / ((self.height / 100) ** 2)

    @property
    def total_body_fatfreemassperc(self):
        """
        return the total body fat free mass as percentage of the total body
        weight
        """
        return self.total_body_fatfreemass / self.weight * 100

    @property
    def total_body_fatmass(self):
        """return the fat mass in kg"""
        return self.weight - self.total_body_fatfreemass

    @property
    def total_body_fatmassindex(self):
        """return the total body fat mass index"""
        return self.total_body_fatmass / ((self.height / 100) ** 2)

    @property
    def total_body_fatmassperc(self):
        """
        return the total body fat mass as percentage of the total body
        weight
        """
        return 100 - self.total_body_fatfreemassperc

    @property
    def total_body_bonemineralcontent(self):
        """return the bone mineral content in kg"""
        return float(
            -1.72291
            + 0.01673 * self.weight
            + 0.02881 * (self.height**2) / self.total_body_resistance
            + 0.00038 * (self.total_body_reactance**2)
            + 0.00212 * (self.height**2) / self.total_body_reactance
        )

    @property
    def total_body_bonemineralcontentperc(self):
        """
        return the total body bone mineral content as percentage of the total body
        weight
        """
        return self.total_body_bonemineralcontent / self.weight * 100

    @property
    def total_body_softleanmass(self):
        """return the lean soft mass in kg"""
        return self.total_body_fatfreemass - self.total_body_bonemineralcontent

    @property
    def total_body_softleanmassperc(self):
        """
        return the total body soft lean mass as percentage of the total body
        weight
        """
        return self.total_body_softleanmass / self.weight * 100

    @property
    def total_body_skeletalmusclemass(self):
        """return the skeletal muscle mass in kg"""
        return float(
            -18.04706
            + 0.10446 * self.weight
            + 0.00543 * self.age
            + 0.42698 * (self.height**2) / self.total_body_resistance
            + 0.00170 * (self.total_body_reactance**2)
            + 0.01179 * (self.height**2) / self.total_body_impedance
            + 0.20090 * (self.total_body_phaseangle**2)
            + 0.00139 * (self.height**2) / self.total_body_phaseangle
        )

    @property
    def total_body_skeletalmusclemassindex(self):
        """return the total body fat skeletal muscle mass index"""
        return self.total_body_skeletalmusclemass / ((self.height / 100) ** 2)

    @property
    def total_body_skeletalmusclemassperc(self):
        """
        return the total body skeletal muscle massas percentage of the total body
        weight
        """
        return self.total_body_skeletalmusclemass / self.weight * 100

    @property
    def total_body_othertissuesmass(self):
        """return the mass of organs in kg"""
        return self.total_body_softleanmass - self.total_body_skeletalmusclemass

    @property
    def total_body_othertissuesmassperc(self):
        """
        return the mass of organs and other tissues as percentage of the total
        body weight
        """
        return self.total_body_othertissuesmass / self.weight * 100

    @property
    def total_body_basalmetabolicrate(self):
        """return the basal metabolic rate in kcal"""
        return float(
            -340.40464
            + 3.99739 * self.weight
            + 0.16695 * self.age
            + 14.96410 * (self.height**2) / self.total_body_resistance
            + 0.35634 * (self.height**2) / self.total_body_impedance
            + 5.66971 * (self.total_body_phaseangle**2)
            + 0.05072 * (self.height**2) / self.total_body_phaseangle
            + 23.24532 * self.is_male()
            + 6.67914 * self.total_body_reactance
        )

    @property
    def left_arm_fatfreemass(self):
        """return the left arm fat free mass in kg"""
        return float(
            +0.676
            + 0.026 * self.height**2 / self.left_arm_resistance
            - 11.398 * self._trunk_appendicular_index
            + 0.346 * self.is_male()
        )

    @property
    def left_arm_fatfreemassperc(self):
        """
        return the left arm fat free mass as percentage of the total body weight
        """
        return self.left_arm_fatfreemass / self.weight * 100

    @property
    def left_arm_fatmass(self):
        """return the left arm fat mass in kg"""
        return float(
            -0.420
            + 0.107 * self.bmi
            - 0.216 * self.left_arm_phaseangle
            - 0.163 * self.is_male()
        )

    @property
    def left_arm_fatmassperc(self):
        """
        return the left arm fat mass as percentage of the total body weight
        """
        return self.left_arm_fatmass / self.weight * 100

    @property
    def right_arm_fatfreemass(self):
        """return the right arm fat free mass in kg"""
        return float(
            +0.676
            + 0.026 * self.height**2 / self.right_arm_resistance
            - 11.398 * self._trunk_appendicular_index
            + 0.346 * self.is_male()
        )

    @property
    def right_arm_fatfreemassperc(self):
        """
        return the right arm fat free mass as percentage of the total body weight
        """
        return self.right_arm_fatfreemass / self.weight * 100

    @property
    def right_arm_fatmass(self):
        """return the right arm fat mass in kg"""
        return float(
            -0.447
            + 0.102 * self.bmi
            - 0.188 * self.right_arm_phaseangle
            - 0.155 * self.is_male()
        )

    @property
    def right_arm_fatmassperc(self):
        """
        return the right arm fat mass as percentage of the total body weight
        """
        return self.right_arm_fatmass / self.weight * 100

    @property
    def left_leg_fatfreemass(self):
        """return the left leg fat free mass in kg"""
        return float(
            +4.756
            + 0.067 * self.height**2 / self.left_leg_resistance
            - 54.597 * self._trunk_appendicular_index
            + 0.901 * self.is_male()
        )

    @property
    def left_leg_fatfreemassperc(self):
        """
        return the left leg fat free mass as percentage of the total body weight
        """
        return self.left_leg_fatfreemass / self.weight * 100

    @property
    def left_leg_fatmass(self):
        """return the left leg fat mass in kg and as percentage of
        the as percentage of the total fat mass"""
        return float(
            1.545
            + 0.250 * self.bmi
            - 1.343 * self.is_male()
            - 0.524 * self.left_leg_phaseangle
        )

    @property
    def left_leg_fatmassperc(self):
        """
        return the left leg fat mass as percentage of the total body weight
        """
        return self.left_leg_fatmass / self.weight * 100

    @property
    def right_leg_fatfreemass(self):
        """return the right leg fat free mass in kg"""
        return float(
            +3.724
            + 0.071 * self.height**2 / self.right_leg_resistance
            - 46.197 * self._trunk_appendicular_index
            + 0.733 * self.is_male()
        )

    @property
    def right_leg_fatfreemassperc(self):
        """
        return the right leg fat free mass as percentage of the total body weight
        """
        return self.right_leg_fatfreemass / self.weight * 100

    @property
    def right_leg_fatmass(self):
        """return the right leg fat mass in kg"""
        return float(
            2.731
            + 0.256 * self.bmi
            - 1.286 * self.is_male()
            - 0.7 * self.right_leg_phaseangle
        )

    @property
    def right_leg_fatmassperc(self):
        """
        return the right leg fat mass as percentage of the total body weight
        """
        return self.right_leg_fatmass / self.weight * 100

    @property
    def total_trunk_fatfreemass(self):
        """return the trunk fat free mass in kg"""
        return float(
            -6.19740
            + 0.20178 * self.weight
            + 0.00287 * (self.height**2) / self.total_trunk_resistance
            + 0.01800 * (self.total_trunk_reactance**2)
            + 0.00003 * (self.height**2) / self.total_trunk_phaseangle
            + 2.21723 * self.is_male()
            + 0.00157 * (self.height**2) / self.total_trunk_reactance
            + 0.00208 * (self.total_trunk_impedance**2)
        )

    @property
    def total_trunk_fatfreemassperc(self):
        """
        return the trunk fat free mass as percentage of the total body weight
        """
        return self.total_trunk_fatfreemass / self.weight * 100

    @property
    def total_trunk_fatmass(self):
        """return the trunk fat mass in kg"""
        return float(
            -26.788
            + 0.978 * self.bmi
            + 0.445 * self.total_trunk_resistance
            + 0.045 * self.age
        )

    @property
    def total_trunk_fatmassperc(self):
        """
        return the trunk fat mass as percentage of the total body weight
        """
        return self.total_trunk_fatmass / self.weight * 100


class Standard(Fitness):
    """
    an object allowing the calculation of body composition data from
    anthropometric and electric data using standard equations from the literature
    """

    def __init__(
        self,
        age: int | float,
        sex: Literal["M", "F"],
        height: int,
        weight: int | float,
        left_arm_resistance: int | float,
        left_arm_reactance: int | float,
        left_trunk_resistance: int | float,
        left_trunk_reactance: int | float,
        left_leg_resistance: int | float,
        left_leg_reactance: int | float,
        left_body_resistance: int | float,
        left_body_reactance: int | float,
        right_arm_resistance: int | float,
        right_arm_reactance: int | float,
        right_trunk_resistance: int | float,
        right_trunk_reactance: int | float,
        right_leg_resistance: int | float,
        right_leg_reactance: int | float,
        right_body_resistance: int | float,
        right_body_reactance: int | float,
        corrected_electrical_values=False,
    ):
        super().__init__(
            age=age,
            sex=sex,
            height=height,
            weight=weight,
            left_arm_resistance=left_arm_resistance,
            left_arm_reactance=left_arm_reactance,
            left_leg_resistance=left_leg_resistance,
            left_leg_reactance=left_leg_reactance,
            left_trunk_resistance=left_trunk_resistance,
            left_trunk_reactance=left_trunk_reactance,
            left_body_resistance=left_body_resistance,
            left_body_reactance=left_body_reactance,
            right_arm_resistance=right_arm_resistance,
            right_arm_reactance=right_arm_reactance,
            right_leg_resistance=right_leg_resistance,
            right_leg_reactance=right_leg_reactance,
            right_trunk_resistance=right_trunk_resistance,
            right_trunk_reactance=right_trunk_reactance,
            right_body_resistance=right_body_resistance,
            right_body_reactance=right_body_reactance,
            corrected_electrical_values=corrected_electrical_values,
        )
        self.apply_orthostatic_correction()

    @property
    def total_body_water(self):
        """
        return the total body water in liters and as percentage
        of the total body weight

        Reference
        ---------
        Matias CN, Santos DA, Júdice PB, Magalhães JP, Minderico CS, Fields DA,
            et al. Estimation of total body water and extracellular water with
            bioimpedance in athletes: a need for athlete-specific prediction
            models. Clin Nutr. 2016;35:468–74. doi:10.1016/j.clnu.2015.03.013
            https://www.doi.org/10.1016/j.clnu.2015.03.013
        """
        return float(
            0.286
            + 0.195 * (self.height**2) / self.right_body_resistance
            + 0.385 * self.weight
            + 5.086 * self.is_male()
        )

    @property
    def total_body_extracellularwater(self):
        """
        return the extracellular water in liters

        Reference
        ---------
        Sergi G, Bussolotto M, Perini P, Calliari I, Giantin V, Ceccon A,
            Scanferla F, Bressan M, Moschini G, Enzi G. Accuracy of
            Bioelectrical Impedance Analysis in Estimation of Extracellular
            Space in Healthy Subjects and in Fluid Retention States.
            Ann Nutr Metab 1 March 1994; 38 (3): 158–165. doi:10.1159/000177806
            https://doi.org/10.1159/000177806
        """
        return float(
            -3.32
            + 0.2 * (self.height**2) / self.right_body_resistance
            + 0.005 * (self.height**2) / self.right_body_reactance
            + 1.86 * (not self.is_male())
            + 0.08 * self.weight
        )

    @property
    def total_body_fatfreemass(self):
        """
        return the free-fat mass in kg

        References
        ----------
        Matias CN, Campa F, Santos DA, Lukaski H, Sardinha LB, Silva AM.
        Fat-free mass bioelectrical impedance analysis predictive equation for
        athletes using a 4-compartment model. Int J Sports Med. 2021;42:27–32.
        doi:10.1055/a-1179-6236. https://www.doi.org/10.1055/a-1179-6236
        """
        return float(
            -2.261
            + 0.327 * (self.height**2) / self.right_body_resistance
            + 0.525 * self.weight
            + 5.462 * self.is_male()
        )

    @property
    def total_body_bonemineralcontent(self):
        """
        return the bone mineral content in kg

        References
        ----------
        Stone TM, Wingo JE, Nickerson BS, Esco MR. Comparison of
            Bioelectrical Impedance Analysis and Dual-Energy X-Ray
            Absorptiometry for Estimating Bone Mineral Content.
            International Journal of Sport Nutrition and Exercise Metabolism
            28 (5): 542:546. doi:10.1123/ijsnem.2017-0185.
            https://www.doi.org/10.1123/ijsnem.2017-0185
        """
        return (
            +0.35966
            + 0.89328
            * exp(
                -0.47127 * log(self.right_body_resistance)
                + 2.65176 * log(self.height)
                - 9.62779
            )
            - 0.12978 * (not self.is_male())
        )

    @property
    def total_body_skeletalmusclemass(self):
        """
        return the skeletal muscle mass in kg

        References
        ----------
        Janssen I, Heymsfield SB, Baumgartner RN, Ross R. Estimation of skeletal
            muscle mass by bioelectrical impedance analysis. Journal of Applied
            Physiology 2000 89:2, 465-471. doi: 10.1152/jappl.2000.89.2.465
            https://doi.org/10.1152/jappl.2000.89.2.465
        """
        return float(
            +5.102
            + 0.401 * (self.height**2) / self.right_body_resistance
            + 3.825 * self.is_male()
            - 0.071 * self.age
        )

    @property
    def total_body_basalmetabolicrate(self):
        """
        return the basal metabolic rate in kcal

        References
        ----------
        Müller MJ, Bosy-Westphal A, Klaus S, Kreymann G, Lührmann PM,
            Neuhäuser-Berthold M, Noack R, Pirke KM, Platte P, Selberg O,
            Steiniger J. World Health Organization equations have shortcomings
            for predicting resting energy expenditure in persons from a modern,
            affluent population: generation of a new reference standard from a
            retrospective analysis of a German database of resting energy
            expenditure. Am J Clin Nutr. 2004 Nov;80(5):1379-90.
            doi: 10.1093/ajcn/80.5.1379.
            https://www.doi.org/10.1093/ajcn/80.5.1379
        """
        return float(
            238.85
            * (
                +0.05192 * self.total_body_fatfreemass
                + 0.04036 * self.total_body_fatmass
                + 0.869 * self.is_male()
                - 0.01181 * self.age
                + 2.992
            )
        )

    @property
    def left_arm_fatfreemass(self):
        """
        return the left arm fat free mass in kg

        References
        ----------
        Sardinha, L.B., Rosa, G.B., Hetherington-Rauth, M. et al. Development
            and validation of bioelectrical impedance prediction equations
            estimating regional lean soft tissue mass in middle-aged adults.
            Eur J Clin Nutr 77, 202–211 (2023). doi: 10.1038/s41430-022-01224-0
            https://doi.org/10.1038/s41430-022-01224-0
        """
        return float(
            +0.676
            + 0.026 * self.height**2 / self.left_arm_resistance
            - 11.398 * self._trunk_appendicular_index
            + 0.346 * self.is_male()
        )

    @property
    def left_arm_fatmass(self):
        """
        return the left arm fat mass in kg

        References
        ----------
        Silva 2024 unpublished
        """
        return float(
            -0.420
            + 0.107 * self.bmi
            - 0.216 * self.left_arm_phaseangle
            - 0.163 * self.is_male()
        )

    @property
    def right_arm_fatfreemass(self):
        """
        return the right arm fat free mass in kg

        References
        ----------
        Sardinha, L.B., Rosa, G.B., Hetherington-Rauth, M. et al. Development
            and validation of bioelectrical impedance prediction equations
            estimating regional lean soft tissue mass in middle-aged adults.
            Eur J Clin Nutr 77, 202–211 (2023). doi: 10.1038/s41430-022-01224-0
            https://doi.org/10.1038/s41430-022-01224-0
        """
        return float(
            +0.676
            + 0.026 * self.height**2 / self.right_arm_resistance
            - 11.398 * self._trunk_appendicular_index
            + 0.346 * self.is_male()
        )

    @property
    def right_arm_fatmass(self):
        """
        return the right arm fat mass in kg

        References
        ----------
        Silva 2024 unpublished
        """
        return float(
            -0.447
            + 0.102 * self.bmi
            - 0.188 * self.right_arm_phaseangle
            - 0.155 * self.is_male()
        )

    @property
    def left_leg_fatfreemass(self):
        """
        return the left leg fat free mass in kg

        References
        ----------
        Sardinha, L.B., Rosa, G.B., Hetherington-Rauth, M. et al. Development
            and validation of bioelectrical impedance prediction equations
            estimating regional lean soft tissue mass in middle-aged adults.
            Eur J Clin Nutr 77, 202–211 (2023). doi: 10.1038/s41430-022-01224-0
            https://doi.org/10.1038/s41430-022-01224-0
        """
        return float(
            +4.756
            + 0.067 * self.height**2 / self.left_leg_resistance
            - 54.597 * self._trunk_appendicular_index
            + 0.901 * self.is_male()
        )

    @property
    def left_leg_fatmass(self):
        """
        return the left leg fat mass in kg

        References
        ----------
        Silva 2024 unpublished
        """
        return float(
            1.545
            + 0.250 * self.bmi
            - 1.343 * self.is_male()
            - 0.524 * self.left_leg_phaseangle
        )

    @property
    def right_leg_fatfreemass(self):
        """
        return the right leg fat free mass in kg

        References
        ----------
        Sardinha, L.B., Rosa, G.B., Hetherington-Rauth, M. et al. Development
            and validation of bioelectrical impedance prediction equations
            estimating regional lean soft tissue mass in middle-aged adults.
            Eur J Clin Nutr 77, 202–211 (2023). doi: 10.1038/s41430-022-01224-0
            https://doi.org/10.1038/s41430-022-01224-0
        """
        return float(
            +3.724
            + 0.071 * self.height**2 / self.right_leg_resistance
            - 46.197 * self._trunk_appendicular_index
            + 0.733 * self.is_male()
        )

    @property
    def right_leg_fatmass(self):
        """
        return the right leg fat mass in kg

        References
        ----------
        Silva 2024 unpublished
        """
        return float(
            2.731
            + 0.256 * self.bmi
            - 1.286 * self.is_male()
            - 0.7 * self.right_leg_phaseangle
        )

    @property
    def total_trunk_fatfreemass(self):
        """
        return the trunk fat free mass in kg

        References
        ----------
        Sardinha, L.B., Rosa, G.B., Hetherington-Rauth, M. et al. Development
            and validation of bioelectrical impedance prediction equations
            estimating regional lean soft tissue mass in middle-aged adults.
            Eur J Clin Nutr 77, 202–211 (2023). doi: 10.1038/s41430-022-01224-0
            https://doi.org/10.1038/s41430-022-01224-0
        """
        return float(
            -10.039
            + 0.015 * (self.height**2) / self.total_trunk_resistance
            + 160.945 * self._trunk_appendicular_index
        )

    @property
    def total_trunk_fatmass(self):
        """
        return the trunk fat mass in kg

        References
        ----------
        Silva 2024 unpublished
        """
        return float(
            -26.788
            + 0.978 * self.bmi
            + 0.445 * self.total_trunk_resistance
            + 0.045 * self.age
        )


class Inbody(Fitness):

    _onnx_model: OnnxModel
    _model_path = join(dirname(__file__), "assets", "model2_200x4_vs_inbody.onnx")
    _preds: dict[str, float]

    def __init__(
        self,
        age: int | float,
        height: int,
        weight: int | float,
        left_arm_resistance: int | float,
        left_arm_reactance: int | float,
        left_leg_resistance: int | float,
        left_leg_reactance: int | float,
        left_body_resistance: int | float,
        left_body_reactance: int | float,
        right_arm_resistance: int | float,
        right_arm_reactance: int | float,
        right_leg_resistance: int | float,
        right_leg_reactance: int | float,
        right_body_resistance: int | float,
        right_body_reactance: int | float,
    ):
        super().__init__(
            age=age,
            sex="M",
            height=height,
            weight=weight,
            left_arm_resistance=left_arm_resistance,
            left_arm_reactance=left_arm_reactance,
            left_leg_resistance=left_leg_resistance,
            left_leg_reactance=left_leg_reactance,
            left_trunk_resistance=np.nan,
            left_trunk_reactance=np.nan,
            left_body_resistance=left_body_resistance,
            left_body_reactance=left_body_reactance,
            right_arm_resistance=right_arm_resistance,
            right_arm_reactance=right_arm_reactance,
            right_leg_resistance=right_leg_resistance,
            right_leg_reactance=right_leg_reactance,
            right_trunk_resistance=np.nan,
            right_trunk_reactance=np.nan,
            right_body_resistance=right_body_resistance,
            right_body_reactance=right_body_reactance,
            corrected_electrical_values=False,
        )

        self._onnx_model = OnnxModel(
            model_path=self._model_path,
            input_labels=[  # order is important and defined at model creation
                "height",
                "weight",
                "age",
                "left_arm_resistance",
                "left_arm_reactance",
                "left_leg_resistance",
                "left_leg_reactance",
                "left_body_resistance",
                "left_body_reactance",
                "right_arm_resistance",
                "right_arm_reactance",
                "right_leg_resistance",
                "right_leg_reactance",
                "right_body_resistance",
                "right_body_reactance",
            ],
            output_labels=[  # order is important and defined at model creation
                "total_body_basalmetabolicrate",
                "total_body_proteins",
                "total_body_minerals",
                "target_weight",
                "total_body_phaseangle",
                "total_body_phaseanglecorrected",
                "total_body_fatmass",
                "total_body_fatmassperc",
                "total_body_fatmassindex",
                "total_body_fatfreemass",
                "total_body_fatfreemassperc",
                "total_body_fatfreemassindex",
                "total_body_bonemineralcontentperc",
                "total_body_bonemineralcontent",
                "total_body_softleanmass",
                "total_body_softleanmassperc",
                "total_body_skeletalmusclemass",
                "total_body_skeletalmusclemassperc",
                "total_body_skeletalmusclemassindex",
                "left_arm_fatmass",
                "left_arm_fatfreemassperc",
                "left_leg_fatmass",
                "left_leg_fatmassperc",
                "left_leg_fatfreemass",
                "left_leg_fatfreemassperc",
                "right_arm_fatmass",
                "right_arm_fatmassperc",
                "right_arm_fatfreemass",
                "right_arm_fatfreemassperc",
                "right_leg_fatmass",
                "right_leg_fatmassperc",
                "right_leg_fatfreemass",
                "right_leg_fatfreemassperc",
                "total_trunk_fatmass",
                "total_trunk_fatmassperc",
                "total_trunk_fatfreemass",
                "total_trunk_fatfreemassperc",
                "total_body_water",
                "total_body_waterperc",
                "total_body_extracellularwater",
                "total_body_extracellularwaterperc",
                "total_body_intracellularwater",
                "total_body_intracellularwaterperc",
                "ecw_on_icw",
            ],
        )

        # get the predictions
        inputs = {i: getattr(self, i) for i in self._onnx_model.input_labels}
        self._preds = self._onnx_model(inputs)

    @property
    def total_body_water(self):
        """return the total body water in liters and as percentage
        of the total body weight"""
        return float(self._preds["total_body_water"])

    @property
    def total_body_extracellularwater(self):
        """return the extracellular water in liters"""
        return float(self._preds["total_body_extracellularwater"])

    @property
    def total_body_fatfreemass(self):
        """return the free-fat mass in kg"""
        return float(self._preds["total_body_fatfreemass"])

    @property
    def total_body_bonemineralcontent(self):
        """return the bone mineral content in kg"""
        return float(self._preds["total_body_bonemineralcontent"])

    @property
    def total_body_skeletalmusclemass(self):
        """return the skeletal muscle mass in kg"""
        return float(self._preds["total_body_skeletalmusclemass"])

    @property
    def total_body_basalmetabolicrate(self):
        """return the basal metabolic rate in kcal"""
        return float(self._preds["total_body_basalmetabolicrate"])

    @property
    def total_body_minerals(self):
        """return the total body mineral content"""
        return float(self._preds["total_body_minerals"])

    @property
    def total_body_proteins(self):
        """return the total body proteins mass"""
        return float(self._preds["total_body_proteins"])

    @property
    def left_arm_fatfreemass(self):
        """return the left arm fat free mass in kg"""
        return float(self._preds["left_arm_fatfreemass"])

    @property
    def left_arm_fatmass(self):
        """return the left arm fat mass in kg"""
        return float(self._preds["left_arm_fatmass"])

    @property
    def right_arm_fatfreemass(self):
        """return the right arm fat free mass in kg"""
        return float(self._preds["right_arm_fatfreemass"])

    @property
    def right_arm_fatmass(self):
        """return the right arm fat mass in kg"""
        return float(self._preds["right_arm_fatmass"])

    @property
    def left_leg_fatfreemass(self):
        """return the left leg fat free mass in kg"""
        return float(self._preds["left_leg_fatfreemass"])

    @property
    def left_leg_fatmass(self):
        """return the left leg fat mass in kg and as percentage of
        the as percentage of the total fat mass"""
        return float(self._preds["left_leg_fatmass"])

    @property
    def right_leg_fatfreemass(self):
        """return the right leg fat free mass in kg"""
        return float(self._preds["right_leg_fatfreemass"])

    @property
    def right_leg_fatmass(self):
        """return the right leg fat mass in kg"""
        return float(self._preds["right_leg_fatmass"])

    @property
    def total_trunk_fatfreemass(self):
        """return the trunk fat free mass in kg"""
        return float(self._preds["total_trunk_fatfreemass"])

    @property
    def total_trunk_fatmass(self):
        """return the trunk fat mass in kg"""
        return float(self._preds["total_trunk_fatmass"])

    @property
    def total_body_phaseanglecorrected(self):
        return self._preds["total_body_phaseanglecorrected"]


class CheckupBIA:
    """BIA analysis"""

    _fitness: Fitness
    _inbody: Inbody
    _standard: Standard

    def __init__(
        self,
        age: int | float,
        sex: Literal["M", "F"],
        height: int,
        weight: int | float,
        left_arm_resistance: int | float,
        left_arm_reactance: int | float,
        left_trunk_resistance: int | float,
        left_trunk_reactance: int | float,
        left_leg_resistance: int | float,
        left_leg_reactance: int | float,
        left_body_resistance: int | float,
        left_body_reactance: int | float,
        right_arm_resistance: int | float,
        right_arm_reactance: int | float,
        right_trunk_resistance: int | float,
        right_trunk_reactance: int | float,
        right_leg_resistance: int | float,
        right_leg_reactance: int | float,
        right_body_resistance: int | float,
        right_body_reactance: int | float,
        corrected_electrical_values=False,
    ):
        self._fitness = Fitness(
            age=age,
            sex=sex,
            height=height,
            weight=weight,
            left_arm_resistance=left_arm_resistance,
            left_arm_reactance=left_arm_reactance,
            left_leg_resistance=left_leg_resistance,
            left_leg_reactance=left_leg_reactance,
            left_trunk_resistance=left_trunk_resistance,
            left_trunk_reactance=left_trunk_reactance,
            left_body_resistance=left_body_resistance,
            left_body_reactance=left_body_reactance,
            right_arm_resistance=right_arm_resistance,
            right_arm_reactance=right_arm_reactance,
            right_leg_resistance=right_leg_resistance,
            right_leg_reactance=right_leg_reactance,
            right_trunk_resistance=right_trunk_resistance,
            right_trunk_reactance=right_trunk_reactance,
            right_body_resistance=right_body_resistance,
            right_body_reactance=right_body_reactance,
            corrected_electrical_values=corrected_electrical_values,
        )
        self._standard = Standard(
            age=age,
            sex=sex,
            height=height,
            weight=weight,
            left_arm_resistance=left_arm_resistance,
            left_arm_reactance=left_arm_reactance,
            left_leg_resistance=left_leg_resistance,
            left_leg_reactance=left_leg_reactance,
            left_trunk_resistance=left_trunk_resistance,
            left_trunk_reactance=left_trunk_reactance,
            left_body_resistance=left_body_resistance,
            left_body_reactance=left_body_reactance,
            right_arm_resistance=right_arm_resistance,
            right_arm_reactance=right_arm_reactance,
            right_leg_resistance=right_leg_resistance,
            right_leg_reactance=right_leg_reactance,
            right_trunk_resistance=right_trunk_resistance,
            right_trunk_reactance=right_trunk_reactance,
            right_body_resistance=right_body_resistance,
            right_body_reactance=right_body_reactance,
            corrected_electrical_values=corrected_electrical_values,
        )
        self._inbody = Inbody(
            age=age,
            height=height,
            weight=weight,
            left_arm_resistance=left_arm_resistance,
            left_arm_reactance=left_arm_reactance,
            left_leg_resistance=left_leg_resistance,
            left_leg_reactance=left_leg_reactance,
            left_body_resistance=left_body_resistance,
            left_body_reactance=left_body_reactance,
            right_arm_resistance=right_arm_resistance,
            right_arm_reactance=right_arm_reactance,
            right_leg_resistance=right_leg_resistance,
            right_leg_reactance=right_leg_reactance,
            right_body_resistance=right_body_resistance,
            right_body_reactance=right_body_reactance,
        )

    def to_dict(self):
        """return all the measures as dictionary"""
        return dict(
            fitness=self.fitness.to_dict(),
            standard=self.standard.to_dict(),
            inbody=self.inbody.to_dict(),
        )

    @property
    def fitness(self):
        """return the set of fitness-equations based measures"""
        return self._fitness

    @property
    def standard(self):
        """return the set of standard-equations based measures"""
        return self._standard

    @property
    def inbody(self):
        """return the set of standard-equations based measures"""
        return self._inbody
