""" LogEvent classes (Checks) """


from abc import ABC

from pyspark.sql import DataFrame as SparkDF

from pplog.config import Operator
from pplog.integrations import great_expectations as ge


#  pylint:disable=fixme,too-few-public-methods
class _ICheck(ABC):
    """Abtract log checking class"""


class CheckDataFrameCount(_ICheck):
    """Spark DataFrame Count Checker"""

    def __init__(self, sdf: SparkDF, params: dict) -> None:
        self._sdf = sdf
        self._params = params
        self._comparison_function_string = params["comparison_function"]
        self._comparison_function = getattr(Operator, self._comparison_function_string.upper())
        self._comparison_value = params["comparison_value"]
        self._sdf_count = sdf.count()

    def check(self):
        """Perform check and log result"""
        return self._comparison_function(self._sdf_count, self._comparison_value)


class GreatExpectationsSparkDFCheck(_ICheck):
    """Checks a SparkDataFrame with great expectations library."""

    def __init__(self, sdf: SparkDF, params: dict) -> None:
        self._sdf = sdf
        self._params = params

        expectation_config = ge.ExpectationConfiguration(
            expectation_type=params["expectation_type"],
            kwargs=params["kwargs"],
        )
        suite = ge.create_expectation_suite(expectation_config)
        self.checkpoint = ge.create_checkpoint(
            context=ge.get_in_memory_gx_context(), suite=suite, dataframe=sdf
        )

    def check(self):
        """Perform check and log result"""
        results = self.checkpoint.run()
        simple_results: ge.SimpleValidationResult = ge.get_validation_results(results)
        return simple_results.is_suite_success
