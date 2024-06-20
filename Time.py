import streamlit as st
import numpy as np
from scipy.optimize import fsolve
from matplotlib import pyplot as plt

# Establecer semilla para reproducibilidad
np.random.seed(123)

# Definimos los parámetros del modelo con Streamlit
st.sidebar.header('Parámetros del modelo')
beta = st.sidebar.number_input('Factor de descuento (beta)', value=0.99)
delta = st.sidebar.number_input('Tasa de depreciación (delta)', value=0.025)
alpha = st.sidebar.number_input('Participación del capital en la función de producción (alpha)', value=0.36)
theta = st.sidebar.number_input('Parámetro de elasticidad de sustitución intertemporal (theta)', value=2.0)
rho = st.sidebar.number_input('Persistencia del shock tecnológico (rho)', value=0.45)
sigma = st.sidebar.number_input('Desviación estándar del shock tecnológico (sigma)', value=0.01)
v = st.sidebar.number_input('Parámetro de elasticidad de sustitución entre capital y trabajo (v)', value=0.5)
num_periods = st.sidebar.number_input('Número de periodos', value=100, step=1)
shock_size = st.sidebar.number_input('Tamaño del shock', value=0.1)
shock_period = st.sidebar.slider('Periodo en el que se produce el shock', 0, num_periods-1, 10)

# Función de producción
def production_function(X, k, n, y):
    return X * (n**(1 - alpha)) * ((1 - alpha) * k**(-v) + alpha * y**(-v))**(-1/v)

# Función de utilidad
def utility_function(c, l):
    return (c**(1 - theta) - 1) / (1 - theta) + l

# Ecuaciones del modelo
def model_equations(variables, params):
    c, k, n, y, X = variables
    beta, delta, alpha, theta, rho, sigma, k_prev, y_prev, X_prev, shock, shock_size = params

    eq1 = beta * ((c**(-theta)) * ((1 - delta) + alpha * production_function(X, k, n, y))) - c**(-theta)
    eq2 = k - ((1 - delta) * k_prev + y_prev)
    eq3 = y - (c + k - (1 - delta) * k_prev)
    eq4 = X - (rho * X_prev + (np.random.normal(0, sigma) + (shock_size if shock else 0)))
    eq5 = n - (1 - 0.3)  # asumiendo un valor constante para el trabajo

    return [eq1, eq2, eq3, eq4, eq5]

# Valores iniciales
initial_guess = [1, 1, 0.7, 0.1, 1]  # asumiendo n=0.7
params = [beta, delta, alpha, theta, rho, sigma, 1, 0.1, 1, False, 0]

# Simulación en el tiempo con shocks tecnológicos
c_series, k_series, n_series, y_series, X_series = [], [], [], [], []
for t in range(num_periods):
    if t == shock_period:
        params[-2] = True  # Activar shock
        params[-1] = shock_size  # Tamaño del shock
    else:
        params[-2] = False  # Desactivar shock
        params[-1] = 0  # Sin shock

    solution = fsolve(model_equations, initial_guess, args=(params,))
    c, k, n, y, X = solution
    c_series.append(c)
    k_series.append(k)
    n_series.append(n)
    y_series.append(y)
    X_series.append(X)
    initial_guess = solution
    params = [beta, delta, alpha, theta, rho, sigma, k, y, X, params[-2], params[-1]]

# Simulación en el tiempo sin shocks tecnológicos
initial_guess_no_shock = [1, 1, 0.7, 0.1, 1]  # asumiendo n=0.7
params_no_shock = [beta, delta, alpha, theta, rho, sigma, 1, 0.1, 1, False, 0]
c_series_no_shock, k_series_no_shock, n_series_no_shock, y_series_no_shock, X_series_no_shock = [], [], [], [], []
for t in range(num_periods):
    solution_no_shock = fsolve(model_equations, initial_guess_no_shock, args=(params_no_shock,))
    c_no_shock, k_no_shock, n_no_shock, y_no_shock, X_no_shock = solution_no_shock
    c_series_no_shock.append(c_no_shock)
    k_series_no_shock.append(k_no_shock)
    n_series_no_shock.append(n_no_shock)
    y_series_no_shock.append(y_no_shock)
    X_series_no_shock.append(X_no_shock)
    initial_guess_no_shock = solution_no_shock
    params_no_shock = [beta, delta, alpha, theta, rho, sigma, k_no_shock, y_no_shock, X_no_shock, False, 0]

# Graficar la producción
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(y_series, label='Producción (con shock)')
ax.plot(y_series_no_shock, label='Producción (sin shock)', linestyle='--')
ax.legend()
ax.set_xlabel('Periodos')
ax.set_ylabel('Producción')
ax.set_title('Producción: Tendencia y Respuesta al Impulso tras un Shock Tecnológico')

st.pyplot(fig)
