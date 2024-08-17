from sklearn.linear_model import LinearRegression as LR
from .RegressionModel import RegressionModel


class LinearRegression(RegressionModel):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if not self._fileload:
            self._model = LR()
