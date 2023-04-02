from learning import *
import numpy as np
from sklearn.linear_model import LogisticRegression

class LogisticLearner(Learner):
    def __init__(self, datasetFile):
        super().__init__(datasetFile)

    def makeModel(self, weights=None):
        model = LogisticRegression()
        if weights is None:
            model.coef_, model.intercept_ = np.array(
                [[0 for _ in range(len(FEATURES))]]), np.array([0])
        else:
            model.coef_, model.intercept_ = weights
        model.classes_ = np.array([False, True])

        return model

    def getModel(self):
        assert(isinstance(self.model, LogisticRegression))
        return self.model.coef_, self.model.intercept_

    def train(self):
        assert(isinstance(self.model, LogisticRegression))
        self.model.fit(self.X, self.Y)

    def score(self):
        return self.model.score(self.X, self.Y)

    def validateModel(self, weights):
        model = self.makeModel(weights)
        return model.score(self.X, self.Y)

