from sklearn.linear_model import Ridge
from .RegressionModel import RegressionModel


class RidgeRegression(RegressionModel):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if not self._fileload:
            if "ridge" in kwargs:
                if isinstance(kwargs["ridge"], float):
                    self._model = Ridge(alpha=kwargs["ridge"])
                else:
                    raise ValueError("Alpha value of ridge should be a float")
            else:
                self._model = Ridge(alpha=0.0)
