from sklearn.linear_model import LogisticRegression as LR
from .ClassificationModel import ClassificationModel


class LogisticRegression(ClassificationModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._model = LR(max_iter=99999999)

    def _check_bin_cls(self, ds):
        if len(ds.unique()) == 2:
            return True

        return False

    def _feature_init(self, **kwargs):
        if isinstance(kwargs["target"], str):
            if not self._check_bin_cls(self._dataf[kwargs["target"]]):
                raise ValueError("Multi Class classification is not Supported Yet")

        return super()._feature_init(**kwargs)

    def _custom_train_test_init(self, **kwargs):
        if not self._check_bin_cls(kwargs["y_Train"]):
            raise ValueError("Multi Class Classification is not Supported Yet")

        return super()._custom_train_test_init(**kwargs)
