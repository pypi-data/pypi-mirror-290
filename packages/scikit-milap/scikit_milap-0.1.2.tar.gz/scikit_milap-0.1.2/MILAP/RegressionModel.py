import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    r2_score,
)

from .BaseModel import BaseModel


class RegressionModel(BaseModel):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def test(self, X_test=None, Y_test=None, plot_show=False):
        if not X_test and not Y_test:
            X_test = self._xtest
            Y_test = self._ytest
        else:
            if self._poly is not None:
                X_test = self._poly.transform(X_test)

        if X_test is not None and Y_test is not None:
            yPred = self._model.predict(X_test)

            merr = mean_squared_error(Y_test, yPred)
            rmerr = np.sqrt(merr)
            r2 = r2_score(Y_test, yPred)
            mae = mean_absolute_error(Y_test, yPred)
            mape = mean_absolute_percentage_error(Y_test, yPred)

            self._perf_metrics["MeanSqERR"] = merr
            self._perf_metrics["RootMeanSqERR"] = rmerr
            self._perf_metrics["MeanAbsERR"] = mae
            self._perf_metrics["MeanAbsPercERR"] = mape
            self._perf_metrics["r2"] = r2

            fig, axs = plt.subplots()
            axs.scatter(Y_test, yPred)
            axs.set_xlabel("True Values")
            axs.set_ylabel("Predictions")
            axs.set_title("True vs Predicted Prices")
            axs.grid(True)

            scatter_graph = fig

            if plot_show:
                plt.show()

            self._cache["scatter_plot"] = scatter_graph

            return yPred, merr, r2, scatter_graph
        else:
            if not X_test and not Y_test:
                raise ValueError("No Test Data Available")
            elif not X_test:
                raise ValueError("No X_Test Data Available")
            raise ValueError("No Y_test Data Available")

    def perf_print(self):
        print(f"R2 score: {self._perf_metrics.get("r2","NA")}")
        print(f"Mean Absolute Error: {self._perf_metrics.get("MeanAbsERR","NA")}")
        print(
            f"Mean Absolute Perc Error: {self._perf_metrics.get("MeanAbsPercERR","NA")}"
        )
        print(f"Mean Squared Error: {self._perf_metrics.get("MeanSqERR","NA")}")
        print(
            f"Root Mean Squared Error: {self._perf_metrics.get("RootMeanSqERR","NA")}\n\n"
        )

    def PredscatterPlot(self, **kwargs):
        plot = self._cache.get("scatter_plot", None)
        if kwargs.get("force", False) or not plot:
            self.train()
            plot = self._cache.get("scatter_plot", None)
            if not plot:
                raise ValueError("Something Wrong INternally")
        if "filename" in kwargs:
            filename = kwargs.get("filename", "scatter_plot")
            filename = filename + ".png"
            plot.savefig(filename)

        if kwargs.get("show", True):
            plt.show(plot)

        return plot

    @property
    def r2_score(self):
        return self._perf_metrics.get("r2", None)

    @property
    def mean_sq_err(self):
        return self._perf_metrics.get("MeanSqERR", None)

    @property
    def root_mean_sq_err(self):
        return self._perf_metrics.get("RootMeanSqERR", None)

    @property
    def mean_abs_err(self):
        return self._perf_metrics.get("MeanAbsERR", None)

    @property
    def mean_abs_perc_err(self):
        return self._perf_metrics.get("MeanAbsPercERR", None)
