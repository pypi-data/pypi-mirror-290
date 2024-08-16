from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict

from medmodels.medrecord.medrecord import MedRecord
from medmodels.medrecord.types import MedRecordAttribute

if TYPE_CHECKING:
    from medmodels.treatment_effect.treatment_effect import TreatmentEffect


class FullReport(TypedDict):
    relative_risk: float
    odds_ratio: float
    confounding_bias: float
    absolute_risk: float
    number_needed_to_treat: float
    hazard_ratio: float


class ContinuousReport(TypedDict):
    average_treatment_effect: float
    cohens_d: float


class Report:
    _treatment_effect: TreatmentEffect

    def __init__(self, treatment_effect: TreatmentEffect) -> None:
        self._treatment_effect = treatment_effect

    def full_report(self, medrecord: MedRecord) -> FullReport:
        """Generates a full report of the treatment effect estimation.

        Args:
            medrecord (MedRecord): An instance of the MedRecord class containing medical
                data.

        Returns:
            FullReport: A dictionary containing the results of all estimation
                methods: relative risk, odds ratio, confounding bias, absolute risk,
                number needed to treat, and hazard ratio.
        """
        return {
            "relative_risk": self._treatment_effect.estimate.relative_risk(medrecord),
            "odds_ratio": self._treatment_effect.estimate.odds_ratio(medrecord),
            "confounding_bias": self._treatment_effect.estimate.confounding_bias(
                medrecord
            ),
            "absolute_risk": self._treatment_effect.estimate.absolute_risk(medrecord),
            "number_needed_to_treat": self._treatment_effect.estimate.number_needed_to_treat(
                medrecord
            ),
            "hazard_ratio": self._treatment_effect.estimate.hazard_ratio(medrecord),
        }

    def continuous_estimators_report(
        self,
        medrecord: MedRecord,
        outcome_variable: MedRecordAttribute,
        reference: Literal["first", "last"] = "last",
        add_cohens_d_correction: bool = False,
    ) -> ContinuousReport:
        """Generates a report of continuous treatment effect estimators.

        Args:
            medrecord (MedRecord): An instance of the MedRecord class containing medical
                data.
            outcome_variable (MedRecordAttribute): The attribute in the edge that
                contains the outcome variable.
            reference (Literal["first", "last"], optional): The reference point for the
                exposure time. Options include "first" and "last". If "first", the
                function returns the earliest exposure edge. If "last", the function
                returns the latest exposure edge. Defaults to "last".
            add_cohens_d_correction (bool, optional): A boolean indicating whether to
                include a correction for Cohen's d. Defaults to False.

        Returns:
            ContinuousReport: A dictionary containing the results of continuous
                treatment effect estimators: average treatment effect and Cohen's d.
        """
        average_treatment_effect = (
            self._treatment_effect.estimate.average_treatment_effect(
                medrecord,
                outcome_variable,
                reference=reference,
            )
        )
        cohens_d_value = self._treatment_effect.estimate.cohens_d(
            medrecord,
            outcome_variable,
            reference=reference,
            add_correction=add_cohens_d_correction,
        )
        return {
            "average_treatment_effect": average_treatment_effect,
            "cohens_d": cohens_d_value,
        }
