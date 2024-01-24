import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import patsy
import statsmodels.api as sm
from scipy.stats import linregress
from statsmodels.tsa.arima.model import ARIMA
from scipy.optimize import minimize_scalar


class Kannisto:
    """
    A class to perform Kannisto transformation and estimate mortality rates.

    Requirements:
    - import pandas as pd
    - import numpy as np
    - import statsmodels.api as sm

    Attributes:
    - fit_ages (numpy.ndarray or array-like): Ages used for fitting the model.
    - predict_ages (numpy.ndarray or array-like): Ages for which the transformation will be performed.
    - mx (pd.Series): Mortality rates.
    - all_ages (numpy.ndarray): All ages present in the mortality rates.
    - observed (numpy.ndarray): Observed mortality rates.
    - coef (list): Coefficients obtained from the fitting process.
    - fitted (pd.Series): Fitted mortality rates after transformation.
    - residuals (pd.Series): Residuals obtained from the fitting process.

    Methods:
    - fit(mx): Fits the Kannisto model to the given mortality rates.
    - transform(): Performs Kannisto transformation for the specified predict_ages and returns the transformed mortality rates.
    - fit_transform(mx): Fits the Kannisto model to the given mortality rates and then performs the transformation.
    - estimate(): Estimates the Kannisto coefficients and fitted mortality rates based on the given fit_ages and mortality rates.
    """

    def __init__(self, fit_ages=np.arange(60, 81, 5), predict_ages=np.arange(85, 101, 5)):
        self.mx = None
        self.all_ages = None
        self.observed = None
        self.fit_ages = fit_ages
        self.predict_ages = predict_ages
        self.coef = None
        self.fitted = None
        self.residuals = None

    def fit(self, mx):
        """
        Fits the Kannisto model to the given mortality rates.

        Args:
        - mx (pd.Series): Mortality rates.

        Returns:
        - Kannisto: The Kannisto object itself.
        """
        self.mx = mx
        self.all_ages = mx.index.values
        self.observed = mx.values
        self.estimate()
        return self

    def transform(self):
        """
        Performs Kannisto transformation for the specified predict_ages.

        Returns:
        - pd.Series: Transformed mortality rates.
        """
        mx = self.mx
        x = self.predict_ages
        c = self.coef[0]
        d = self.coef[1]
        fitted = pd.Series(c * np.exp(d * x) / (1 + c * np.exp(d * x)), x)
        orig_ages = list(set(self.all_ages) - set(self.predict_ages))
        self.fitted = pd.concat([mx[orig_ages], fitted]).sort_index()
        return self.fitted

    def fit_transform(self, mx):
        """
        Fits the Kannisto model to the given mortality rates and then performs the transformation.

        Args:
        - mx (pd.Series): Mortality rates.

        Returns:
        - pd.Series: Transformed mortality rates.
        """
        self.fit(mx)
        return self.transform()

    def estimate(self):
        """
        Estimates the Kannisto coefficients and fitted mortality rates based on the given fit_ages and mortality rates.
        """
        x = self.fit_ages
        values = self.mx[self.fit_ages]
        y = np.log(values) - np.log(1 - values)
        X = sm.add_constant(x)
        model = sm.OLS(y, X).fit()
        c = np.exp(model.params[0])
        d = model.params[1]
        self.coef = [c, d]
        self.fitted = pd.Series(c * np.exp(d * x) / (1 + c * np.exp(d * x)), x)
        self.residuals = values - self.fitted


class TOPALS:
    def __init__(self):
        self.k = None
        self.p = None
        self.w = None
        self.a = None
        self.b = None

    def initialize_params(self, std, knot_positions, boundaries, penalty_precision=2):
        self.std = np.array(std)
        self.knot_positions = knot_positions
        self.boundaries = np.concatenate([np.array([0, 1]), np.arange(5, 86, 5)])
        self.penalty_precision = penalty_precision

        a = len(self.std)
        age = np.arange(0, 100)
        self.b = patsy.bs(
            degree=1,
            x=age,
            knots=self.knot_positions,
            include_intercept=False
        )
        self.k = self.b.shape[1]

        d1 = np.diff(np.eye(self.k), 1, axis=0)
        self.p = self.penalty_precision * d1.T @ d1

        g = len(self.boundaries) - 1
        nages = np.diff(self.boundaries)

        self.w = np.zeros((g, a))
        offset = 0
        for i in range(g):
            start = offset
            end = nages[i] + offset
            self.w[i, start:end] = 1 / nages[i]
            offset += nages[i]

        self.a = np.zeros((1, self.k))[0]

    def q(self, alpha):
        mu = np.exp(self.std + self.b @ alpha)
        m = self.w @ mu
        likelihood = np.sum(self.D * np.log(m) - self.N * m)
        penalty = 1 / 2 * alpha.T @ self.p @ alpha
        return likelihood - penalty

    def next_alpha(self, alpha):
        mu = np.exp(self.std + self.b @ alpha)
        m = self.w @ mu
        d_hat = self.N * m
        x = self.w @ np.diag(mu) @ self.b
        a = np.diag(self.N / m)
        y = (self.D - d_hat) / self.N + x @ alpha
        updated_alpha = np.linalg.solve(x.T @ a @ x + self.p, x.T @ a @ y)
        return updated_alpha

    def fit(self, N, D, std, knot_positions, boundaries, max_iter=50, alpha_tol=0.00005):
        """
        Train the model using the TOPALS method.

        Parameters:
        - N (array): Array of N values.
        - D (array): Array of D values.
        - std (array): Array of standard deviation values.
        - knot_positions (list): List of knot positions for basis functions.
        - boundaries (array): Array of boundaries for determining weight coefficients.
        - max_iter (int): Maximum number of iterations.
        - alpha_tol (float): Allowable difference between consecutive alpha values for convergence.

        Returns:
        self
        """
        self.N = np.array(N)
        self.D = np.array(D)
        self.initialize_params(std, knot_positions, boundaries)
        n_iter = 0
        while n_iter < max_iter:
            n_iter += 1
            last_param = self.a
            self.a = self.next_alpha(self.a)
            change = self.a - last_param
            converge = np.all(np.abs(change) < alpha_tol)
            if converge or n_iter == max_iter:
                break
        self.logmx = self.std + (self.b @ self.a)
        return self

    def transform(self):
        return self.logmx

    def fit_transform(self, N, D, std, knot_positions, boundaries, max_iter=50, alpha_tol=0.00005):
        """
        Train the model using the TOPALS method.

        Parameters:
        - N (array): Array of N values.
        - D (array): Array of D values.
        - std (array): Array of standard deviation values.
        - knot_positions (list): List of knot positions for basis functions.
        - boundaries (array): Array of boundaries for determining weight coefficients.
        - max_iter (int): Maximum number of iterations.
        - alpha_tol (float): Allowable difference between consecutive alpha values for convergence.

        Returns:
        logmx
        """
        self.fit(N, D, std, knot_positions, boundaries, max_iter=max_iter, alpha_tol=alpha_tol)
        return self.logmx


class Gompertz:
    """
    Gompertz class for fitting and predicting using the Gompertz model.

    Requirements:
    - import pandas as pd
    - import numpy as np

    Attributes:
    - is_fitted (bool): Indicates whether the model has been fitted with data.
    - lx_init (numpy.ndarray or array-like): Initial lx values for fitting.
    - age_init (numpy.ndarray or array-like): Initial ages for fitting.
    - a (float): Gompertz parameter 'a'.
    - b (float): Gompertz parameter 'b'.
    - c (float): Gompertz parameter 'c'.
    - predictions (DataFrame): Predicted lx values and ages as a DataFrame.

    Methods:
    - fit(lx, age): Fits the Gompertz model to the given lx and age data.
    - predict(start_age, end_age): Predicts lx values for a range of ages.
    - fit_predict(lx_true, age_true, start_age, end_age): Fits the model with given data and predicts lx values for a range of ages.
    """

    def __init__(self):
        """
        Initializes a Gompertz model with default parameters.
        """
        self.is_fitted = False
        self.lx_init = None
        self.age_init = None
        self.a = None
        self.b = None
        self.c = None
        self.predictions = None

    def fit(self, lx, age):
        """
        Fits the Gompertz model to the given lx and age data.

        Args:
        - lx (numpy.ndarray or array-like): The lx values for fitting the Gompertz model.
        - age (numpy.ndarray or array-like): The corresponding ages for fitting the Gompertz model.

        Returns:
        - self: Returns the instance of the Gompertz class after fitting the model.

        Raises:
        - ValueError: If the lengths of lx and age vectors do not match or if they don't contain 3 data points.
        """
        if len(lx) != len(age):
            raise ValueError("lx and age vectors must have the same size")
        if len(lx) != 3 or len(age) != 3:
            raise ValueError(f"3 data poits expected, got {len(lx)}")
        self.lx_init = lx
        self.age_init = age
        self.n = (self.age_init[2] - self.age_init[0]) / 2
        if self.age_init[2] - self.age_init[1] != self.age_init[1] - self.age_init[0]:
            print(f"Attention! n = {self.n}")
        self.b = (np.log(self.lx_init[2] / self.lx_init[1]) /
                  np.log(self.lx_init[1] / self.lx_init[0])) ** (1 / self.n)
        self.a = np.exp(np.log(self.lx_init[1] / self.lx_init[0]) /
                        ((self.b ** self.age_init[0]) * ((self.b ** self.n) - 1)))
        self.c = self.lx_init[0] * np.exp(-((self.b ** self.age_init[0]) * np.log(self.a)))
        self.is_fitted = True
        return self

    def predict(self, start_age: int, end_age: int):
        """
        Predicts lx values for a range of ages using the fitted Gompertz model.

        Args:
        - start_age (int): The start age for prediction.
        - end_age (int): The end age for prediction.

        Returns:
        - predictions (DataFrame): A DataFrame containing the predicted lx values and corresponding ages.

        Raises:
        - ValueError: If start_age or end_age is less than 0 or if end_age is less than start_age.
        """
        if start_age < 0:
            raise ValueError("Invalid start_age")
        if end_age < 0:
            raise ValueError("Invalid end_age")
        if start_age > end_age:
            raise ValueError(f"end_age({end_age}) must be greater then start_age({start_age})")
        age_modeled = np.arange(start_age, end_age + 1)
        lx_modeled = self.c * (self.a ** self.b ** age_modeled)
        result = pd.DataFrame(
            {
                'lx': lx_modeled,
                'age': age_modeled
            }
        )
        result.set_index('age', inplace=True)
        self.predictions = result
        return self.predictions

    def fit_predict(self, lx_true, age_true, start_age, end_age):
        """
        Fits the model with given data and predicts lx values for a range of ages.

        Args:
        - lx_true (numpy.ndarray or array-like): The true lx values for fitting the Gompertz model.
        - age_true (numpy.ndarray or array-like): The corresponding true ages for fitting the Gompertz model.
        - start_age (int): The start age for prediction.
        - end_age (int): The end age for prediction.

        Returns:
        - predictions (DataFrame): A DataFrame containing the predicted lx values and corresponding ages.

        Raises:
        - ValueError: If the lengths of lx_true and age_true vectors do not match or if they don't contain 3 data points.
        - ValueError: If start_age or end_age is less than 0 or if end_age is less than start_age.
        """
        self.fit(lx_true, age_true).predict(start_age, end_age)
        return self.predictions


class LeeCarter:
    def __init__(self):
        self.is_fitted = False

    def __str__(self):
        return f"LeeCarter forecasting model. Is fitted={self.is_fitted}"

    def fit(
            self,
            mxt_df: pd.DataFrame,
            sex: str,
            stopyear: object = None,
            adjust: object = None,
            smooth=None,
            regularize=False
    ) -> object:
        # Извлекаем матрицу смертности mxt_m, вектор возрастов ages_v и вектор лет years_v
        self.mxt_m, self.ages_v, self.years_v = self.unwrap_mxt_df(mxt_df)
        self.sex = sex
        self.regularize = regularize
        # Получаем матрицу логарифмов смертности
        self.log_mxt_m = np.log(mxt_df)
        # if smooth == 'spline':
            # self.log_mxt_m = preprocess.smooth_bivariate_spline(self.log_mxt_m, s=3)
        # Выполняем несколько этапов для подготовки модели
        self.ax_v, self.kt_v, self.bx_v = self.fit_kt_bx()
        self.kt_se_s = self.get_ktse()
        self.log_mxt_fit_m = self.fit_mx()
        self.mxt_fit_m = np.exp(self.log_mxt_fit_m)
        self.e0_fit_v = self.fit_e0()
        self.e0_actual_v = self.get_e0()
        self.kt_model = self.fit_kt_forecasting_model()
        if adjust == "e0":
            self.kt_model = None
            self.kt_v = self.adjust_by_e0()
            self.log_mxt_fit_adjusted_m = np.outer(self.kt_v, self.bx_v) + self.ax_v
            self.mxt_fit_adjusted_m = np.exp(self.log_mxt_fit_adjusted_m)
            self.e0_match = np.allclose(self.e0_actual_v, np.array([life_expectancy(
                mx, self.ages_v, sex=self.sex, restype='e0') for mx in self.mxt_fit_adjusted_m]))
            self.kt_model = self.fit_kt_forecasting_model()
        self.stopyear = stopyear
        self.is_fitted = True
        return self

    def forecast(self, n=1):
        # Генерируем будущие года
        # future_years = np.arange(np.min(self.years_v), np.max(self.years_v) + n + 1).reshape(-1, 1)
        # Добавляем столбец единиц для учета свободного коэффициента в регрессии
        # future_years_with_const = np.column_stack((future_years, np.ones_like(future_years)))
        # Прогнозируем значения с помощью модели линейной регрессии
        # kt_forecast = self.kt_model.predict(future_years_with_const)
        # mx_predicted = np.exp(self.ax_v + kt_forecast[-1] * self.bx_v)
        kt_forecast = self.kt_model.forecast(steps=n)
        mx_predicted = np.exp(self.ax_v + kt_forecast[-1] * self.bx_v)
        e0_predicted = life_expectancy(mx_predicted, self.ages_v, self.sex, restype='e0')
        return [kt_forecast, e0_predicted]

    def adjust_by_e0(self):
        def optimize(guess, e0_actual_s, ax_v, bx_v):
            mx_fitted_v = np.exp(ax_v + guess * bx_v)
            e0_fitted_s = life_expectancy(mx_fitted_v, self.ages_v, self.sex)
            return abs(e0_actual_s - e0_fitted_s)

        kt_adj_v = []
        for i in range(len(self.kt_v)):
            e0_actual_s = self.e0_actual_v[i]
            result = minimize_scalar(optimize, args=(e0_actual_s, self.ax_v, self.bx_v))
            kt_adj_s = result.x
            kt_adj_v.append(kt_adj_s)

        return np.array(kt_adj_v)

    def unwrap_mxt_df(self, mxt_df):
        # Извлекаем матрицу смертности mxt_m, вектор возрастов ages_v и вектор лет years_v
        mxt_m = mxt_df.values
        ages_v = np.array(mxt_df.columns.astype(int))
        years_v = np.array(mxt_df.index.astype(int))
        return mxt_m, ages_v, years_v

    def fit_kt_bx(self):
        # Вычисляем средние логарифмы смертности по годам
        ax_v = np.array(self.log_mxt_m.mean(axis=0))
        # Центрируем матрицу логарифмов смертности
        Axt_m = self.log_mxt_m.sub(ax_v, axis=1)
        # Сингулярное разложение для выделения главных компонент
        U_m, S_v, V_m = np.linalg.svd(Axt_m, full_matrices=True)
        sumv_s = np.sum(V_m[0, :])
        # Компоненты Картера
        s = S_v[0]
        kt_v = U_m[:, 0] * sumv_s * s
        bx_v = V_m[0, :] / sumv_s
        return ax_v, kt_v, bx_v

    def fit_mx(self, restype='log_mxt_m'):
        # Вычисляем приближенную матрицу логарифмов смертности
        centered_log_mxt_fit_m = np.outer(self.kt_v, self.bx_v)
        log_mxt_fit_m = centered_log_mxt_fit_m + self.ax_v
        return log_mxt_fit_m

    def fit_e0(self):
        # Вычисляем приближенные значения ожидаемой продолжительности жизни
        e0_fit_v = np.array([life_expectancy(
            mx, self.ages_v, sex=self.sex, restype='e0') for mx in self.mxt_fit_m])
        return e0_fit_v

    def get_e0(self):
        # Вычисляем фактические значения ожидаемой продолжительности жизни
        e0_actual_v = np.array([life_expectancy(
            mx, self.ages_v, sex=self.sex, restype='e0') for mx in self.mxt_m])
        return e0_actual_v

    def fit_kt_forecasting_model(self):
        # Создаем матрицу признаков для обучения модели линейной регрессии
        x = np.column_stack((self.years_v, np.ones_like(self.years_v)))
        # Обучаем модель линейной регрессии
        # model = LinearRegression(fit_intercept=True)
        # return model
        model = ARIMA(self.kt_v, order=(1, 1, 1))
        model_fit = model.fit()
        return model_fit


    def get_ktse(self):
        # Вычисляем стандартные ошибки для коэффициентов Картера
        x = np.arange(1, len(self.years_v) + 1)
        kt_se_s = linregress(x, self.kt_v).stderr
        return kt_se_s


def life_expectancy(mx, age, sex='M', l0=1, restype='e0'):
    """
    Calculates life expectancy based on mortality rates.

    Requirements:
    - import pandas as pd
    - import numpy as np

    Args:
    - mx (numpy.ndarray or array-like): Mortality rates.
    - age (numpy.ndarray or array-like): Age values.
    - sex (str, optional): Gender specification (either 'M' or 'F'), default is 'M'.
    - l0 (int, optional): Initial population size, default is 100000.
    - restype (str, optional): Type of result to return:
      - 'e0' for life expectancy,
      - 'ex' for life expectancy at each age,
      - 'lifetable' for complete life table.

    Returns:
    - float or array-like or DataFrame: Depending on the restype, it returns life expectancy, life expectancy at each age,
      or complete life table as DataFrame.

    Raises:
    - ValueError: If restype is not recognized.
    """
    if type(mx) != np.ndarray and type(mx) != np.array:
        mx = np.array(mx)
    if type(age) != np.ndarray and type(age) != np.array:
        age = np.array(age)
    mx = np.where(mx < 0, 0, mx)
    last = len(mx)
    ax = np.zeros(last) + 0.5
    nx = np.append(np.diff(age), 1)
    if sex == '':
        print('warning: sex==m')
        sex = 'M'
    if mx[0] >= 0.107:
        if sex == 'M':
            ax[0] = 0.33
            if nx[1] > 1:
                ax[1] = 1.352 / 4
        else:
            ax[0] = 0.35
            if nx[1] > 1:
                ax[1] = 1.361 / 4
    else:
        if sex == 'F':
            ax[0] = 0.045 + 2.684 * mx[0]
            if nx[1] > 1:
                ax[1] = (1.653 - 3.013 * mx[0]) / 4
        else:
            ax[0] = 0.053 + 2.8 * mx[0]
            if nx[1] > 1:
                ax[1] = (1.524 - 1.627 * mx[0]) / 4

    ax[last - 1] = 1 / mx[last - 1]
    qx = nx * mx / (1 + nx * (1 - ax) * mx)
    qx = np.where(qx > 1, 1, qx)
    n = np.argmax(qx > 1)
    if n > 1:
        qx = np.append(qx[:n - 1], 1)
        ax = np.append(ax[:n - 1], 0.5)
        nx = nx[:n]
    last = len(qx)
    qx[last - 1] = 1
    ax[last - 1] = 1 / mx[last - 1]
    px = 1 - qx
    lx = np.cumprod(px)
    lx = np.insert(lx, 0, 1)[:-1] * l0
    dx = lx * qx
    dx[-1] = lx[-1]
    Lx = nx * lx - nx * (1 - ax) * dx
    Lx[-1] = lx[-1] * ax[-1]
    Tx = [None] * len(age)
    for i in range(last):
        Tx[i] = sum(Lx[i:])
    ex = [None] * len(age)
    for i in range(last - 1):
        ex[i] = Tx[i] / lx[i]
    ex[-1] = ax[-1]
    e0 = sum(Lx)
    if restype == 'e0':
        return e0
    elif restype == 'ex':
        return ex
    elif restype == 'lifetable':
        Tx = np.array(Tx)
        lifetable = pd.DataFrame({
            'age': age,
            'mx': mx,
            'qx': qx,
            'px': px,
            'ax': ax,
            'lx': lx,
            'Lx': Lx,
            'Tx': Tx,
            'ex': ex
        }).set_index('age')
        return lifetable
    else:
        raise ValueError('Unknown restype')
