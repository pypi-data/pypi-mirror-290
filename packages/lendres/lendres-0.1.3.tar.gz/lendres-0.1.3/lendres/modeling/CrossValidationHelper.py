"""
Created on March 31, 2022
@author: Lance A. Endres
"""
from   sklearn.model_selection                                       import KFold
from   sklearn.model_selection                                       import StratifiedKFold
from   sklearn.model_selection                                       import cross_val_score

from   lendres.io.ConsoleHelper                                      import ConsoleHelper

class CrossValidationHelper():

    def __init__(self, modelHelper):
        """
        Constructor.

        Parameters
        ----------
        modelHelper : ModelHelper
            ModelHelper used in the cross validation.

        Returns
        -------
        None.
        """
        self.modelHelper    = modelHelper
        self.kFold          = None
        self.results        = None


    def CreateModel(self, splits, score, stratified=False):
        # Defining kfold technique.

        if stratified:
            self.kFold = StratifiedKFold(n_splits=splits, random_state=1, shuffle=True)
        else:
            self.kFold = KFold(n_splits=splits, random_state=1, shuffle=True)

        self.results = cross_val_score(
			self.modelHelper.model,
			self.modelHelper.dataHelper.xTrainingData,
			self.modelHelper.dataHelper.yTrainingData,
			cv=self.kFold,
			scoring=score
		)


    def PrintResults(self):
        self.modelHelper.dataHelper.consoleHelper.Print("Accuracy: %.3f%%" % (self.results.mean()*100.0), ConsoleHelper.VERBOSETESTING)
        self.modelHelper.dataHelper.consoleHelper.Print("Standard deviation: %.3f%%" % (self.results.std()*100.0), ConsoleHelper.VERBOSETESTING)