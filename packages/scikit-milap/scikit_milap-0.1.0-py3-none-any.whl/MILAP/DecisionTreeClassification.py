from .ClassificationModel import ClassificationModel
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import numpy as np


class DecisionTreeModel(ClassificationModel):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._citeration = kwargs.get("citeration", "gini")
        self._max_depth = kwargs.get("max_depth", None)
        self._max_features = kwargs.get("max_features", None)
        self._min_sample_split = kwargs.get("min_sample_split", 2)
        self._min_samples_leaf = kwargs.get("min_samples_leaf", 1)
        self._max_leaf_nodes = kwargs.get("max_leaf_nodes", None)

        self._model = DecisionTreeClassifier(
            criterion=self._citeration,
            max_depth=self._max_depth,
            max_features=self._max_features,
            min_samples_split=self._min_sample_split,
            min_samples_leaf=self._min_samples_leaf,
            max_leaf_nodes=self._max_leaf_nodes,
            random_state=42,
        )

    def test(self, X_test=None, Y_test=None, plot_show=False):
        ret = super().test(X_test, Y_test, plot_show=False)

        if plot_show:
            self.tree_plot()

        return ret

    def tree_plot(self):
        if self._max_depth and self._max_depth < 20:
            plot_tree(self._model)
            plt.show()
        else:
            print("Tree size too huge to show.\n Try Lowering the max_depth attribute")
