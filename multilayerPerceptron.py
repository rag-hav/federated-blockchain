import numpy as np
from sklearn.neural_network import MLPClassifier
from learning import Learner


class MultilayerPerceptronLearner(Learner):
    def __init__(self, datasetFile):
        super().__init__(datasetFile)

    def makeModel(self, weights=None):
        model = MLPClassifier(hidden_layer_sizes=(
            10, 5, 2), alpha=0.0001, random_state=1)
        if weights is not None:
            model.set_params(weights)
        model.classes_ = np.array([False, True])

        return model

    def getModel(self):
        assert(isinstance(self.model, MLPClassifier))
        return self.model.get_params(deep=True)

    def train(self):
        assert(isinstance(self.model, MLPClassifier))
        self.model.fit(self.X, self.Y)

    def score(self):
        assert(isinstance(self.model, MLPClassifier))
        return self.model.score(self.X, self.Y)

    def validateModel(self, weights):
        model = self.makeModel(weights)
        return model.score(self.X, self.Y)
