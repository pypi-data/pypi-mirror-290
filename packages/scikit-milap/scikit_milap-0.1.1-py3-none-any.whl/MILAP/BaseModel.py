import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


class BaseModel:
    def __init__(self, **kwargs) -> None:
        self._model = None

        self._xtrain = None
        self._ytrain = None

        self._xtest = None
        self._ytest = None

        self._dataf = None
        self._X = None
        self._Y = None

        self._poly = None
        self._scaler = None

        self._trained = False
        self._fileload = False

        self._test_split_ratio = 0.2
        self._perf_metrics = {}
        self._cache = {}

        if "data" in kwargs:
            self._dataf = kwargs["data"]

            if "features" in kwargs and "target" in kwargs:
                self._feature_init(**kwargs)

        elif "X_Train" in kwargs and "y_Train" in kwargs:
            self._custom_train_test_init(**kwargs)

        elif "model_file" in kwargs:
            self._model = joblib.load(kwargs["model_file"])
            self._fileload = True

        else:
            raise ValueError("No Params Passed To Initialize")

    def train(self):
        self._model_check()

        if self._xtrain is not None and self._ytrain is not None:
            self._model.fit(self._xtrain, self._ytrain)
            self._trained = True

        elif not self._fileload:
            raise ValueError("Training Data Not Provided")

    def predict(self, X):
        self._model_check()

        if self._scaler:
            X = self._scaler.transform(X)

        if self._poly:
            X = self._poly.transform(X)

        return self._model.predict(X)

    def save_raw(self, filename=None):
        self._model_check()

        if not filename:
            filename = "regression_model"

        filename = filename + ".pkl"
        joblib.dump(self._model, filename)

    def save(self, filename=None):
        if not filename:
            filename = "model"

        filename = filename + ".pkl"

    @classmethod
    def load(cls, filename):
        loaded_instance = joblib.load(filename)
        return loaded_instance

    @property
    def features(self):
        return list(self._X)

    @property
    def target(self):
        return self._Y.name

    @property
    def intercept(self):
        return self._model.intercept_

    @property
    def coeffs(self):
        return self._model.coef_

    def _feature_init(self, **kwargs):
        if isinstance(kwargs["features"], list):
            self._X = self._dataf[kwargs["features"]]
        else:
            raise ValueError("Features Should be a List")
        if isinstance(kwargs["target"], str):
            self._Y = self._dataf[kwargs["target"]]
        else:
            raise ValueError("Target should be single and of type str")

        if kwargs.get("test", False):
            if "test_split_ratio" in kwargs:
                self._test_split_ratio = kwargs.get("test_split_ratio", 0.2)

            self._xtrain, self._xtest, self._ytrain, self._ytest = train_test_split(
                self._X,
                self._Y,
                test_size=self._test_split_ratio,
                random_state=42,
            )

        else:
            self._xtrain = self._X
            self._ytrain = self._Y

        if kwargs.get("scale", False):
            self._scaler_init()

        if kwargs.get("polynomial_regression", False):
            self._poly_init()

    def _custom_train_test_init(self, **kwargs):
        self._xtrain = kwargs["X_Train"]
        self._ytrain = kwargs["y_Train"]

        if kwargs.get("test", False) and "X_Test" in kwargs and "y_Test" in kwargs:
            self._xtest = kwargs["X_Test"]
            self._ytest = kwargs["y_Test"]

    def _poly_init(self):
        self._poly = PolynomialFeatures(degree=2)
        self._xtrain = self._poly.fit_transform(self._xtrain)
        if self._xtest is not None:
            self._xtest = self._poly.transform(self._xtest)

    def _scaler_init(self):
        self._scaler = StandardScaler()
        self._xtrain = self._scaler.fit_transform(self._xtrain)
        if self._xtest is not None:
            self._xtest = self._scaler.transform(self._xtest)

    def _model_check(self):
        if not self._model:
            raise ValueError("No Model Loaded/Initailized")
