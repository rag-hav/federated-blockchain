from sklearn.preprocessing import StandardScaler
import pandas as pd
# from sklearn.model_selection import train_test_split

FEATURES = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'proto_icmp', 'proto_tcp', 'proto_udp', 'conn_state_OTH', 'conn_state_REJ',
            'conn_state_RSTO', 'conn_state_RSTOS0', 'conn_state_RSTR', 'conn_state_RSTRH', 'conn_state_S0', 'conn_state_S1', 'conn_state_S2', 'conn_state_S3', 'conn_state_SF', 'conn_state_SH', 'conn_state_SHR']

CLASS = 'label'


class Learner:
    def __init__(self, datasetFile):
        self.df = pd.read_csv(datasetFile, index_col=[0])

        self.X = self.df[FEATURES]
        self.Y = self.df[CLASS]
        scaler = StandardScaler()
        self.X = scaler.fit_transform(self.X)
        self.model = self.makeModel()

    def makeModel(self, weights=None):
        raise NotImplemented()

    def getModel(self):
        raise NotImplemented()

    def train(self):
        raise NotImplemented()

    def score(self):
        raise NotImplemented()

    def scoreModel(self, weights):
        raise NotImplemented()
