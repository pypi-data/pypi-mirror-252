from streamad.model import SRDetector
import numpy as np
import time


class AbstractUnivariateAD():
    def __init__(self, model, thr: float, initialization: int) -> None:
        """Initialize a model for anomaly detection in data stream

        Args:
            model (_type_): a streamad model
            thr (float): threshold that will change the numbers of anomaly detected
            initialization (int): number of values to wait before the anomaly detection
        """
        self.model = model
        self.threshold = thr
        self.anomalies_scores = []
        self.initialization = initialization
        self.predictions = []

    def update() -> None:
        """fit the model and calcul an anomaly score for each new point based on drift concept"""
        pass

    def check_anomalies(self) -> bool:
        """check if anomalies are detected"""

        return np.array(self.predictions).any()

    def get_anomalies(self) -> list[int]:
        '''return a list of anomalies indices'''
        indices_true = [index for index,
                        value in enumerate(self.predictions) if value]
        return indices_true


class UnivariateAD(AbstractUnivariateAD):

    def __init__(self, model, thr: float = 0.9, initialization: int = 500) -> None:
        super().__init__(model, thr, initialization)
        self.n = 0

    def update(self, data: np.ndarray):
        self.n += len(data)
        print(self.n)
        current_data = data.reshape(-1, 1)
        # data_to_scores = current_data[len(
        #     self.anomalies_scores):]
        for x in current_data:
            score = self.model.fit_score(x)
            try:
                if (score > self.threshold) & (len(self.anomalies_scores) > self.initialization):
                    self.predictions.append(True)
                else:
                    self.predictions.append(False)
            except TypeError:
                self.predictions.append(False)
            self.anomalies_scores.append(score)


class MultivariateAD(AbstractUnivariateAD):
    def __init__(self, model, thr: int = 80000, initialization: int = 500) -> None:
        super().__init__(model, thr, initialization)

    def update(self, data: np.ndarray):
        data_to_scores = data
        for x in data_to_scores:
            score = self.model.fit_score(x)
            try:
                if (score > self.threshold) & (len(self.anomalies_scores) > self.initialization):
                    self.predictions.append(True)
                else:
                    self.predictions.append(False)
            except TypeError:
                self.predictions.append(False)
            self.anomalies_scores.append(score)


class CustomEnsembleAD():
    def __init__(self,
                 metrics=["v-rms", "distance", "carousel"],
                 initialization=1000,
                 carousel_window=50,
                 carousel_thr=0.9,
                 distance_window=100,
                 distance_thr=0.75,
                 vrms_window=100,
                 vrms_thr=0.9,
                 verbose=False
                 ) -> None:
        self.metrics = metrics
        self.alerts = {}
        self.subModels = {}
        self.initialization = initialization
        self.carousel_window = carousel_window
        self.carousel_thr = carousel_thr
        self.carousel_mag_num = 5
        self.distance_window = distance_window
        self.distance_thr = distance_thr
        self.vrms_window = vrms_window
        self.vrms_thr = vrms_thr
        self.last_inference_time = 0
        self.verbose = verbose
        self.set_detectors()

    def set_detectors(self):
        for metric in {"carousel", "distance", "v-rms"}:
            if metric == "carousel":
                model = SRDetector(
                    window_len=self.carousel_window, mag_num=self.carousel_mag_num)
                self.subModels[metric] = UnivariateAD(
                    model, self.carousel_thr, self.initialization)
                self.alerts[metric] = False
            if metric == "distance":
                model = SRDetector(window_len=self.distance_window)
                self.subModels[metric] = UnivariateAD(
                    model, self.distance_thr, self.initialization)
                self.alerts[metric] = False
            if metric == "v-rms":
                model = SRDetector(window_len=self.vrms_window)
                self.subModels[metric] = UnivariateAD(
                    model, self.vrms_thr, self.initialization)
                self.alerts[metric] = False
            if self.verbose:
                print(f"Anomaly detection launched for {metric.capitalize()}")

    def fit(self, data):
        # print(data)

        start = time.perf_counter_ns()
        for model_name, model in self.subModels.items():
            metric_data = data[model_name].values
            model.update(metric_data)
        end = time.perf_counter_ns()
        self.last_inference_time = (end - start) / 1e6

    def get_anomaly_status(self):
        return any(self.alerts.values())

    def get_anomaly_type(self) -> str:
        return [model_name for model_name, alert in self.alerts.items() if alert]

    def get_anomalies(self):
        anomalies = []
        for model in self.subModels.values():
            anomalies += model.get_anomalies()
        return anomalies


if __name__ == '__main__':
    import pandas as pd
    # En un seul passage condition benchmark
    file = "/mnt/c/Users/E078051/Desktop/work/dashboard/data/c15.csv"
    df = pd.read_csv(file)
    mod = CustomEnsembleAD(metrics=df.columns.to_list())
    data = df.values
    mod.fit(df)
    idx = mod.get_anomalies_indices()
    print(idx)
