"""Tests for the TreatmentEffect class in the treatment_effect module."""

import unittest
from typing import List

import pandas as pd

from medmodels import MedRecord
from medmodels.medrecord.types import NodeIndex
from medmodels.treatment_effect.continuous_estimators import (
    average_treatment_effect,
    cohens_d,
)


def create_patients(patient_list: List[NodeIndex]) -> pd.DataFrame:
    """Creates a patients dataframe.

    Returns:
        pd.DataFrame: A patients dataframe.
    """
    patients = pd.DataFrame(
        {
            "index": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"],
            "age": [20, 30, 40, 30, 40, 50, 60, 70, 80],
            "gender": [
                "male",
                "female",
                "male",
                "female",
                "male",
                "female",
                "male",
                "female",
                "male",
            ],
        }
    )

    patients = patients.loc[patients["index"].isin(patient_list)]
    return patients


def create_diagnoses() -> pd.DataFrame:
    """Creates a diagnoses dataframe.

    Returns:
        pd.DataFrame: A diagnoses dataframe.
    """
    diagnoses = pd.DataFrame(
        {
            "index": ["D1"],
            "name": ["Stroke"],
        }
    )
    return diagnoses


def create_prescriptions() -> pd.DataFrame:
    """Creates a prescriptions dataframe.

    Returns:
        pd.DataFrame: A prescriptions dataframe.
    """
    prescriptions = pd.DataFrame(
        {
            "index": ["M1", "M2"],
            "name": ["Rivaroxaban", "Warfarin"],
        }
    )
    return prescriptions


def create_edges1(patient_list: List[NodeIndex]) -> pd.DataFrame:
    """Creates an edges dataframe.

    Returns:
        pd.DataFrame: An edges dataframe.
    """
    edges = pd.DataFrame(
        {
            "source": [
                "M2",
                "M1",
                "M2",
                "M1",
                "M2",
                "M1",
                "M2",
            ],
            "target": [
                "P1",
                "P2",
                "P2",
                "P3",
                "P5",
                "P6",
                "P9",
            ],
            "time": [
                "1999-10-15",
                "2000-01-01",
                "1999-12-15",
                "2000-01-01",
                "2000-01-01",
                "2000-01-01",
                "2000-01-01",
            ],
        }
    )
    edges = edges.loc[edges["target"].isin(patient_list)]
    return edges


def create_edges2(patient_list: List[NodeIndex]) -> pd.DataFrame:
    """Creates an edges dataframe with attribute "intensity".

    Returns:
        pd.DataFrame: An edges dataframe.
    """
    edges = pd.DataFrame(
        {
            "source": [
                "D1",
                "D1",
                "D1",
                "D1",
                "D1",
                "D1",
            ],
            "target": [
                "P1",
                "P2",
                "P3",
                "P3",
                "P4",
                "P7",
            ],
            "time": [
                "2000-01-01",
                "2000-07-01",
                "1999-12-15",
                "2000-01-05",
                "2000-01-01",
                "2000-01-01",
            ],
            "intensity": [
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
            ],
            "type": [
                "A",
                "B",
                "A",
                "B",
                "A",
                "A",
            ],
        }
    )
    edges = edges.loc[edges["target"].isin(patient_list)]
    return edges


def create_medrecord(
    patient_list: List[NodeIndex] = [
        "P1",
        "P2",
        "P3",
        "P4",
        "P5",
        "P6",
        "P7",
        "P8",
        "P9",
    ],
) -> MedRecord:
    """Creates a MedRecord object.

    Returns:
        MedRecord: A MedRecord object.
    """
    patients = create_patients(patient_list=patient_list)
    diagnoses = create_diagnoses()
    prescriptions = create_prescriptions()
    edges1 = create_edges1(patient_list=patient_list)
    edges2 = create_edges2(patient_list=patient_list)
    medrecord = MedRecord.from_pandas(
        nodes=[(patients, "index"), (diagnoses, "index"), (prescriptions, "index")],
        edges=[(edges1, "source", "target")],
    )
    medrecord.add_group(group="patients", nodes=patients["index"].to_list())
    medrecord.add_group(
        "Stroke",
        ["D1"],
    )
    medrecord.add_group(
        "Rivaroxaban",
        ["M1"],
    )
    medrecord.add_group(
        "Warfarin",
        ["M2"],
    )
    medrecord.add_edges((edges2, "source", "target"))
    return medrecord


class TestContinuousEstimators(unittest.TestCase):
    """Class to test the continuous estimators."""

    def setUp(self):
        self.medrecord = create_medrecord()
        self.outcome_group = "Stroke"
        self.time_attribute = "time"

    def test_average_treatment_effect(self):
        ate_result = average_treatment_effect(
            self.medrecord,
            treatment_true_set=set({"P2", "P3"}),
            control_true_set=set({"P1", "P4", "P7"}),
            outcome_group=self.outcome_group,
            outcome_variable="intensity",
            reference="last",
            time_attribute=self.time_attribute,
        )
        self.assertAlmostEqual(-0.1, ate_result)

        ate_result = average_treatment_effect(
            self.medrecord,
            treatment_true_set=set({"P2", "P3"}),
            control_true_set=set({"P1", "P4", "P7"}),
            outcome_group=self.outcome_group,
            outcome_variable="intensity",
            reference="first",
            time_attribute=self.time_attribute,
        )
        self.assertAlmostEqual(-0.15, ate_result)

    def test_invalid_treatment_effect(self):
        with self.assertRaisesRegex(ValueError, "Outcome variable must be numeric"):
            average_treatment_effect(
                self.medrecord,
                treatment_true_set=set({"P2", "P3"}),
                control_true_set=set({"P1", "P4", "P7"}),
                outcome_group=self.outcome_group,
                outcome_variable="type",
                reference="last",
                time_attribute=self.time_attribute,
            )

    def test_cohens_d(self):
        cohens_d_result = cohens_d(
            self.medrecord,
            treatment_true_set=set({"P2", "P3"}),
            control_true_set=set({"P1", "P4", "P7"}),
            outcome_group=self.outcome_group,
            outcome_variable="intensity",
            reference="last",
            time_attribute=self.time_attribute,
        )
        self.assertAlmostEqual(-0.59, cohens_d_result, places=2)

        cohens_d_result = cohens_d(
            self.medrecord,
            treatment_true_set=set({"P2", "P3"}),
            control_true_set=set({"P1", "P4", "P7"}),
            outcome_group=self.outcome_group,
            outcome_variable="intensity",
            reference="first",
            time_attribute=self.time_attribute,
        )
        self.assertAlmostEqual(-0.96, cohens_d_result, places=2)

        cohens_d_corrected = cohens_d(
            self.medrecord,
            treatment_true_set=set({"P2", "P3"}),
            control_true_set=set({"P1", "P4", "P7"}),
            outcome_group=self.outcome_group,
            outcome_variable="intensity",
            reference="last",
            time_attribute=self.time_attribute,
            add_correction=True,
        )
        self.assertAlmostEqual(0, cohens_d_corrected)

    def test_invalid_cohens_D(self):
        with self.assertRaisesRegex(ValueError, "Outcome variable must be numeric"):
            cohens_d(
                self.medrecord,
                treatment_true_set=set({"P2", "P3"}),
                control_true_set=set({"P1", "P4", "P7"}),
                outcome_group=self.outcome_group,
                outcome_variable="type",
                reference="last",
                time_attribute=self.time_attribute,
            )


if __name__ == "__main__":
    run_test = unittest.TestLoader().loadTestsFromTestCase(TestContinuousEstimators)
    unittest.TextTestRunner(verbosity=2).run(run_test)
