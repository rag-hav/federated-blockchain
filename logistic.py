from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

FEATURES = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'proto_icmp', 'proto_tcp', 'proto_udp', 'conn_state_OTH', 'conn_state_REJ',
            'conn_state_RSTO', 'conn_state_RSTOS0', 'conn_state_RSTR', 'conn_state_RSTRH', 'conn_state_S0', 'conn_state_S1', 'conn_state_S2', 'conn_state_S3', 'conn_state_SF', 'conn_state_SH', 'conn_state_SHR']

CLASS = 'label'


class LogisticLearner():
    def __init__(self, datasetFile):
        self.df = pd.read_csv(datasetFile, index_col=[0])

        self.X = self.df[FEATURES]
        self.Y = self.df[CLASS]
        self.datasetSize = self.X.shape[0]
        scaler = StandardScaler()
        self.X = scaler.fit_transform(self.X)
        self.model = self._makeModel()

    def _makeModel(self, weights=None):
        model = LogisticRegression()
        if weights is None:
            model.coef_, model.intercept_ = np.array(
                [[0 for _ in range(len(FEATURES))]]), np.array([0])
        else:
            model.coef_, model.intercept_ = weights
        model.classes_ = np.array([False, True])

        return model

    def getModelBytes(self):
        assert(isinstance(self.model, LogisticRegression))
        return pickle.dumps(( self.model.coef_, self.model.intercept_ ))

    def train(self):
        assert(isinstance(self.model, LogisticRegression))
        self.model.fit(self.X, self.Y)

    def score(self):
        return self.model.score(self.X, self.Y)

    def scoreModel(self, weightsBytes):
        model = self._makeModel(pickle.loads(weightsBytes))
        return model.score(self.X, self.Y)

    def updateModel(self, raw_models):
        # raw_models = [( bytes weights, uint256 score )]

        coefficients, intercepts, scores = [], [], []
        for _, weights, score, _ in raw_models:
            coef, intercept = pickle.loads(weights)
            coefficients.append(coef)
            intercepts.append(intercept)
            scores.append(score)

        print(scores)

        coefAvg = np.average(coefficients, weights=scores, axis=0)
        interceptAvg = np.average(intercepts, weights=scores, axis=0)

        # print(coefAvg, interceptAvg)
        return coefAvg, interceptAvg
