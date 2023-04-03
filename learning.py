from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.neural_network import MLPClassifier 
import numpy as np

FEATURES = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'proto_icmp', 'proto_tcp', 'proto_udp', 'conn_state_OTH', 'conn_state_REJ',
            'conn_state_RSTO', 'conn_state_RSTOS0', 'conn_state_RSTR', 'conn_state_RSTRH', 'conn_state_S0', 'conn_state_S1', 'conn_state_S2', 'conn_state_S3', 'conn_state_SF', 'conn_state_SH', 'conn_state_SHR']

CLASS = 'label'
HIDDEN_LAYER_SIZES = (10, 5, 2)

class Learner:
    def __init__(self, datasetFile):
        self.df = pd.read_csv(datasetFile, index_col=[0])

        self.X = self.df[FEATURES]
        self.Y = self.df[CLASS]
        scaler = StandardScaler()
        self.X = scaler.fit_transform(self.X)
        self.model = self.makeModel()

    def makeModel(self, weights=None):
        model = MLPClassifier(hidden_layer_sizes= HIDDEN_LAYER_SIZES, alpha=0.0001, random_state=1, activation='relu')
        if weights is None:
            model.fit(np.array([[1 for i in FEATURES]]), np.array([[False]]))
        else:
            model.coefs_, model.intercepts_ = weights
        
        model.feature_names_in_ = FEATURES

        return model

    def getModel(self):
        assert(isinstance(self.model, MLPClassifier))
        return self.model.coefs_, self.model.intercepts_

    def train(self):
        assert(isinstance(self.model, MLPClassifier))
        self.model.fit(self.X, self.Y)

    def score(self):
        return self.model.score(self.X, self.Y)

    def validateModel(self, weights):
        model = self.makeModel(weights)
        return model.score(self.X, self.Y)


