import matplotlib.pyplot as plt
from sklearn.metrics._plot.confusion_matrix import ConfusionMatrixDisplay
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from .BaseModel import BaseModel


class ClassificationModel(BaseModel):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def test(self, X_test=None, Y_test=None, plot_show=False):
        if not self._trained:
            raise ValueError("Model Not tained Yet")

        if not X_test and not Y_test:
            X_test = self._xtest
            Y_test = self._ytest
        else:
            if self._poly is not None:
                X_test = self._poly.transform(X_test)

        if X_test is not None and Y_test is not None:
            yPred = self._model.predict(X_test)
            yPred_proba = self._model.predict_proba(X_test)

            self._perf_metrics["accuracy"] = accuracy_score(Y_test, yPred)
            self._perf_metrics["precision"] = precision_score(Y_test, yPred)
            self._perf_metrics["recall"] = recall_score(Y_test, yPred)
            self._perf_metrics["f1"] = f1_score(Y_test, yPred)
            self._perf_metrics["roc_auc"] = roc_auc_score(Y_test, yPred)
            self._perf_metrics["conf_matrix"] = confusion_matrix(Y_test, yPred)
            self._perf_metrics["cls_report"] = classification_report(Y_test, yPred)

            yPred_proba = yPred_proba[:, 1]
            fpr, tpr, thresholds = roc_curve(Y_test, yPred_proba)

            fig, axs = plt.subplots()
            axs.plot(
                fpr, tpr, label=f"ROC -CURVE (area ={self._perf_metrics["roc_auc"]})"
            )
            axs.set_xlabel("False Positive Rate")
            axs.set_ylabel("True Positive Rate")
            axs.grid(True)

            self._cache["roc_graph"] = fig

            if plot_show:
                fig.show()
                plt.show()

            self._cache["yPred"] = yPred
            self._cache["yPred_proba"] = yPred_proba

            return (
                yPred,
                self._perf_metrics["accuracy"],
                self._perf_metrics["precision"],
            )
        else:
            if not X_test and not Y_test:
                raise ValueError("No Test Data Available")
            elif not X_test:
                raise ValueError("No X_Test Data Available")
            raise ValueError("No Y_test Data Available")

    def perf_print(self):
        print(f"Accuracy: {self._perf_metrics.get("accuracy","NA")}")
        print(f"Precision: {self._perf_metrics.get("precision","NA")}")
        print(f"Recall Score: {self._perf_metrics.get("recall","NA")}\n\n")
        print(f"F1 Score: {self._perf_metrics.get("f1","NA")}")
        print(f"ROC-AUC Score: {self._perf_metrics.get("roc_auc","NA")}")
        print(f"Confusion Matrix: {self._perf_metrics.get("conf_matrix","NA")}")
        print(f"Classification Report: {self._perf_metrics.get("cls_report","NA")}")

    def roc_graph(self, **kwargs):
        plot = self._cache.get("roc_graph", None)
        if kwargs.get("force", False) or not plot:
            self.train()
            self.test()
            plot = self._cache.get("roc_graph", None)
            if not plot:
                raise ValueError("Something Wrong INternally")
        if "filename" in kwargs:
            filename = kwargs.get("filename", "roc_graph")
            filename = filename + ".png"
            plot.savefig(filename)

        if kwargs.get("show", True):
            plot.show()
            plt.show()

        return plot

    def precision_recall_plot(self, **kwargs):
        if kwargs.get("force", False):
            self.train()
            self.test()
        elif ("pre_recall_plot" in self._cache) and (
            self._cache["pre_recall_plot"] is not None
        ):
            plot = self._cache["pre_recall_plot"]
            plot.show()
            plt.show()

            return plot

        yPred_proba = self._cache["yPred_proba"]
        precision, recall, thresholds = precision_recall_curve(self._ytest, yPred_proba)

        fig, axs = plt.subplots()
        axs.plot(recall, precision, color="blue", lw=2)
        axs.set_xlabel("Recall")
        axs.set_ylabel("Precision")
        axs.grid(True)

        self._cache["pre_recall_plot"] = fig
        plt.show()
        return fig

    def confusion_display(self, **kwargs):
        if kwargs.get("force", False):
            self.train()
            self.test()

        if "conf_disp" in self._cache and self._cache["conf_disp"] is not None:
            disp = self._cache["conf_disp"]
            disp.plot(cmap=plt.cm.Blues)
            plt.show()
            return disp

        cm = None

        if "conf_matrix" in self._cache:
            cm = self._cache["conf_matrix"]
        elif "yPred" in self._cache:
            cm = confusion_matrix(self._ytest, self._cache["yPred"])
        else:
            yPred, _, _ = self.test()
            cm = confusion_matrix(self._ytest, yPred)

        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap=plt.cm.Blues)
        plt.show()

        self._cache["conf_disp"] = disp
        return disp

    @property
    def accuracy(self):
        return self._perf_metrics.get("accuracy", None)

    @property
    def precision(self):
        return self._perf_metrics.get("precision", None)

    @property
    def recall(self):
        return self._perf_metrics.get("recall", None)

    @property
    def f1(self):
        return self._perf_metrics.get("f1", None)

    @property
    def roc_auc(self):
        return self._perf_metrics.get("roc_auc", None)

    @property
    def conf_matrix(self):
        return self._perf_metrics.get("conf_matrix", None)

    @property
    def cls_report(self):
        return self._perf_metrics.get("cls_report", None)
