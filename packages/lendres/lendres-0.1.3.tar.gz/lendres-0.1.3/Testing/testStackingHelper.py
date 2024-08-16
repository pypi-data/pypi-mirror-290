"""
Created on December 27, 2021
@author: Lance A. Endres
"""
from   sklearn.ensemble                                              import StackingClassifier

import DataSetLoading

from   lendres.io.ConsoleHelper                                      import ConsoleHelper
from   lendres.modeling.AdaBoostHelper                               import AdaBoostHelper
from   lendres.modeling.GradientBoostingHelper                       import GradientBoostingHelper
from   lendres.modeling.StackingHelper                               import StackingHelper

import unittest

class TestStackingHelper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        verboseLevel = ConsoleHelper.VERBOSEREQUESTED
        verboseLevel = ConsoleHelper.VERBOSETESTING
        cls.dataHelper, cls.dependentVariable = DataSetLoading.GetCreditData(verboseLevel=verboseLevel, dropFirst=False)


    def setUp(self):
        """
        Set up function that runs before each test.  Creates a new copy of the data and uses
        it to create a new regression helper.
        """
        self.dataHelper         = self.dataHelper.Copy()
        self.dataHelper.SplitData(self.dependentVariable, 0.3, stratify=False)


    def testResults(self):
        estimator1       = AdaBoostHelper(self.dataHelper)
        estimator1.dataHelper.SplitData(self.dependentVariable, 0.3, stratify=False)
        estimator1.Fit()

        estimator2       = GradientBoostingHelper(self.dataHelper)
        estimator2.dataHelper.SplitData(self.dependentVariable, 0.3, stratify=False)
        estimator2.Fit()

        finalEstimator   = GradientBoostingHelper(self.dataHelper)
        finalEstimator.dataHelper.SplitData(self.dependentVariable, 0.3, stratify=False)
        finalEstimator.Fit()

        estimators       = [("AdaBoost", estimator1.model), ("Gradient Boost", estimator2.model)]
        final_estimator  = finalEstimator.model

        self.regressionHelper   = StackingHelper(self.dataHelper, StackingClassifier(estimators=estimators, final_estimator=final_estimator))
        self.regressionHelper.FitPredict()

        self.regressionHelper.CreateConfusionMatrixPlot(dataSet="testing")
        result = self.regressionHelper.GetConfusionMatrix(dataSet="testing")
        self.assertAlmostEqual(result[1, 1], 28)

        self.regressionHelper.DisplayModelPerformanceScores(final=True)
        result = self.regressionHelper.GetModelPerformanceScores(final=True)
        self.assertAlmostEqual(result.loc["Testing", "Recall"], 0.3255, places=3)


if __name__ == "__main__":
    unittest.main()