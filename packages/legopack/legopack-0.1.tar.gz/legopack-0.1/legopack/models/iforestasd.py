import numpy as np
import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import time


class IforestASD():
    def __init__(self, n_estimators, contamination, drift_threshold, random_state=None):
        self.n_estimators = n_estimators
        self.contamination = contamination
        self.drift_threshold = drift_threshold
        self.random_state = random_state
        self.iforest = self._create()
        self.initialized = False
        self.last_anomaly_score = None
        self.drift_anomalies = {}

    def tmp_fit(self, sample, idx):
        if self.initialized:
            score = self._get_anomaly_scores(sample)
            print(np.abs(score - self.last_anomaly_score))
            if np.abs(score - self.last_anomaly_score) >= self.drift_threshold:
                self._report_anomaly(idx)
                self._create()
            else:
                self.last_anomaly_score = score
        self._fit(sample)

    def _create(self):
        return IsolationForest(
            n_estimators=self.n_estimators, contamination=self.contamination, random_state=self.random_state)

    def _fit(self, sample):
        # print("fitted")
        self.iforest.fit(sample)
        self.last_anomaly_score = self._get_anomaly_scores(sample)
        self.initialized = True

    def _report_anomaly(self, idx):
        timestamp = time.time_ns()
        message = f"Anomaly detected at index {idx}"
        print(message)
        self.drift_anomalies[idx] = timestamp

    def _get_anomaly_scores(self, sample):
        predictions = self.iforest.predict(sample)
        total_anomalies = (predictions < 0).sum()
        anomaly_rate = total_anomalies / len(sample)
        return anomaly_rate


def stream_simulation(model, data, ws, step):
    print("Start")
    current_index = 0
    while current_index < len(data):
        if current_index > ws:
            sample = data[:current_index][-ws:]
            model.tmp_fit(sample, current_index)
            # print(
            # f'{len(sample) = } - {current_index = } - {model.last_anomaly_score = }')
        else:
            print("initialization")
        current_index += step
        time.sleep(0.1)
    print(model.drift_anomalies)


if __name__ == '__main__':
    # Change this values
    FILE = "c08.csv"
    WS = 100
    FEATURES = ["v-rms", "a-rms", "a-peak", "distance"]
    STEP = 50
    N_TREES = 50
    CONTAMINATION = 0.5
    DRIFT_THR = 0.3
    RS = 42
    DATA_REPOSITORY = "data"
    # ==
    file_path = os.path.join(DATA_REPOSITORY, FILE)
    df = pd.read_csv(file_path)
    data = df[FEATURES].values
    model = IforestASD(n_estimators=N_TREES,
                       contamination=CONTAMINATION, drift_threshold=DRIFT_THR, random_state=RS)
    stream_simulation(model, data, ws=WS, step=STEP)
