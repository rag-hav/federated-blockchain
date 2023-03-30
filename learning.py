import pandas as pd
from pprint import pprint
import numpy as np
from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split

FEATURES = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'proto_icmp', 'proto_tcp', 'proto_udp', 'conn_state_OTH', 'conn_state_REJ',
            'conn_state_RSTO', 'conn_state_RSTOS0', 'conn_state_RSTR', 'conn_state_RSTRH', 'conn_state_S0', 'conn_state_S1', 'conn_state_S2', 'conn_state_S3', 'conn_state_SF', 'conn_state_SH', 'conn_state_SHR']

CLASS = 'label'


class Learner:
    def __init__(self, datasetFile):
        self.df = pd.read_csv(datasetFile, index_col=[0])

        self.X = self.df[FEATURES]
        self.Y = self.df[CLASS]

        # pprint(self.Y.value_counts())
        self.model = self.makeModel()

        # self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, random_state=10, test_size=0.2)

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

    def scoreModel(self, weights):
        model = self.makeModel(weights)
        return model.score(self.X, self.Y)
