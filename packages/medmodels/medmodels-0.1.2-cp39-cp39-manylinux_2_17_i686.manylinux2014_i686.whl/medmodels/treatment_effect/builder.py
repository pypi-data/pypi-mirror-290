from __future__ import annotations

from typing import Any, Dict, Literal, Optional

import medmodels.treatment_effect.treatment_effect as tee
from medmodels.medrecord.querying import NodeOperation
from medmodels.medrecord.types import (
    Group,
    MedRecordAttribute,
    MedRecordAttributeInputList,
)
from medmodels.treatment_effect.matching.algorithms.propensity_score import Model
from medmodels.treatment_effect.matching.matching import MatchingMethod


class TreatmentEffectBuilder:
    treatment: Group
    outcome: Group

    patients_group: Optional[Group]
    time_attribute: Optional[MedRecordAttribute]

    washout_period_days: Optional[Dict[str, int]]
    washout_period_reference: Optional[Literal["first", "last"]]

    grace_period_days: Optional[int]
    grace_period_reference: Optional[Literal["first", "last"]]

    follow_up_period_days: Optional[int]
    follow_up_period_reference: Optional[Literal["first", "last"]]

    outcome_before_treatment_days: Optional[int]

    filter_controls_operation: Optional[NodeOperation]

    matching_method: Optional[MatchingMethod]
    matching_essential_covariates: Optional[MedRecordAttributeInputList]
    matching_one_hot_covariates: Optional[MedRecordAttributeInputList]
    matching_model: Optional[Model]
    matching_number_of_neighbors: Optional[int]
    matching_hyperparam: Optional[Dict[str, Any]]

    def with_treatment(self, treatment: Group) -> TreatmentEffectBuilder:
        """Sets the treatment group for the treatment effect estimation.

        Args:
            treatment (Group): The treatment group.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder.
        """
        self.treatment = treatment

        return self

    def with_outcome(self, outcome: Group) -> TreatmentEffectBuilder:
        """Sets the outcome group for the treatment effect estimation.

        Args:
            outcome (Group): The group to be used as the outcome.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated outcome group.
        """
        self.outcome = outcome

        return self

    def with_patients_group(self, group: Group) -> TreatmentEffectBuilder:
        """Sets the group of patients to be used in the treatment effect estimation.

        Args:
            group (Group): The group of patients.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated patients group.
        """
        self.patients_group = group

        return self

    def with_time_attribute(
        self, attribute: MedRecordAttribute
    ) -> TreatmentEffectBuilder:
        """Sets the time attribute to be used in the treatment effect estimation.

        Args:
            attribute (MedRecordAttribute): The time attribute.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated time attribute.
        """
        self.time_attribute = attribute

        return self

    def with_washout_period(
        self,
        days: Optional[Dict[str, int]] = None,
        reference: Optional[Literal["first", "last"]] = None,
    ) -> TreatmentEffectBuilder:
        """Sets the washout period for the treatment effect estimation.

        The washout period is the period of time before the treatment that is not considered in the
        estimation.

        Args:
            days (Optional[Dict[str, int]], optional): The duration of the washout
                period in days. If None, the duration is left as it was. Defaults to
                None.
            reference (Optional[Literal['first', 'last']], optional): The reference
                point for the washout period. Must be either 'first' or 'last'.
                Defaults to None.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated time attribute.
        """
        if days is not None:
            self.washout_period_days = days
        if reference is not None:
            self.washout_period_reference = reference

        return self

    def with_grace_period(
        self,
        days: Optional[int] = None,
        reference: Optional[Literal["first", "last"]] = None,
    ) -> TreatmentEffectBuilder:
        """Sets the grace period for the treatment effect estimation.

        The grace period is the period of time after the treatment that is not considered in the
        estimation.

        Args:
            days (Optional[int], optional): The duration of the grace period in days.
                If None, the duration is left as it was. Defaults to 0.
            reference (Optional[Literal['first', 'last']], optional): The reference
                point for the grace period. Must be either 'first' or 'last'.
                Defaults to None.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated time attribute.
        """
        if days is not None:
            self.grace_period_days = days

        if reference is not None:
            self.grace_period_reference = reference

        return self

    def with_follow_up_period(
        self,
        days: Optional[int] = None,
        reference: Optional[Literal["first", "last"]] = None,
    ) -> TreatmentEffectBuilder:
        """Sets the follow-up period for the treatment effect estimation.

        Args:
            days (Optional[int], optional): The duration of the follow-up period
                in days. If None, the duration is left as it was. Defaults to 365.
            reference (Optional[Literal['first', 'last']], optional): The reference
                point for the follow-up period. Must be either 'first' or 'last'.
                Defaults to None.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated time attribute.
        """
        if days is not None:
            self.follow_up_period_days = days

        if reference is not None:
            self.follow_up_period_reference = reference

        return self

    def with_outcome_before_treatment_exclusion(
        self, days: int
    ) -> TreatmentEffectBuilder:
        """Define whether we allow the outcome to exist before the treatment or not.

        The outcome_before_treatment_days parameter is used to set the number of days
        before the treatment that the outcome should not exist. If not set, the outcome
        is allowed to exist before the treatment.

        Args:
            days (int): The number of days before the treatment that the outcome should
                not exist.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated time attribute.
        """
        self.outcome_before_treatment_days = days

        return self

    def filter_controls(self, operation: NodeOperation) -> TreatmentEffectBuilder:
        """Filter the control group based on the provided operation.

        Args:
            operation (NodeOperation): The operation to be applied to the control group.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated time attribute.
        """
        self.filter_controls_operation = operation

        return self

    def with_propensity_matching(
        self,
        essential_covariates: MedRecordAttributeInputList = ["gender", "age"],
        one_hot_covariates: MedRecordAttributeInputList = ["gender"],
        model: Model = "logit",
        number_of_neighbors: int = 1,
        hyperparam: Optional[Dict[str, Any]] = None,
    ) -> TreatmentEffectBuilder:
        """Adjust the treatment effect estimate using propensity score matching.

        Args:
            essential_covariates (MedRecordAttributeInputList, optional):
                Covariates that are essential for matching. Defaults to
                ["gender", "age"].
            one_hot_covariates (MedRecordAttributeInputList, optional):
                Covariates that are one-hot encoded for matching. Defaults to
                ["gender"].
            model (Model, optional): Model to choose for the matching. Defaults to
                "logit".
            number_of_neighbors (int, optional): Number of neighbors to consider
                for the matching. Defaults to 1.
            hyperparam (Optional[Dict[str, Any]], optional): Hyperparameters for the
                matching model. Defaults to None.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated matching configurations.
        """
        self.matching_method = "propensity"
        self.matching_essential_covariates = essential_covariates
        self.matching_one_hot_covariates = one_hot_covariates
        self.matching_model = model
        self.matching_number_of_neighbors = number_of_neighbors
        self.matching_hyperparam = hyperparam

        return self

    def with_nearest_neighbors_matching(
        self,
        essential_covariates: MedRecordAttributeInputList = ["gender", "age"],
        one_hot_covariates: MedRecordAttributeInputList = ["gender"],
        number_of_neighbors: int = 1,
    ) -> TreatmentEffectBuilder:
        """Adjust the treatment effect estimate using nearest neighbors matching.

        Args:
            essential_covariates (MedRecordAttributeInputList, optional):
                Covariates that are essential for matching. Defaults to
                ["gender", "age"].
            one_hot_covariates (MedRecordAttributeInputList, optional):
                Covariates that are one-hot encoded for matching. Defaults to
                ["gender"].
            number_of_neighbors (int, optional): Number of neighbors to consider for the
                matching. Defaults to 1.

        Returns:
            TreatmentEffectBuilder: The current instance of the TreatmentEffectBuilder
                with updated matching configurations.
        """
        self.matching_method = "nearest_neighbors"
        self.matching_essential_covariates = essential_covariates
        self.matching_one_hot_covariates = one_hot_covariates
        self.matching_number_of_neighbors = number_of_neighbors

        return self

    def build(self) -> tee.TreatmentEffect:
        """Builds the treatment effect with all the provided configurations.

        Returns:
            tee.TreatmentEffect: treatment effect object
        """
        treatment_effect = tee.TreatmentEffect.__new__(tee.TreatmentEffect)
        tee.TreatmentEffect._set_configuration(treatment_effect, **vars(self))

        return treatment_effect
