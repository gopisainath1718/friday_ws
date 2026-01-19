import os
import numpy as np
import mujoco
import mujoco.viewer as viewer
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel as C


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENE_PATH = os.path.join(BASE_DIR, "friday_description", "scene.xml")

#                   kp, damping, friction
param_min = np.array([0.1, 0.01, 0.01])
param_max = np.array([15.0, 0.3, 0.3])

def sample_random():
    params = param_min + np.random.rand(3)*(param_max - param_min) 
    print(params)
    return params

def evaluate(model, data, params):
    settling_time, energy = simulate(model, data, params)
    return settling_time + 0.8 * energy

def acquisition_ucb(gp, X):
    mu, sigma = gp.predict(X, return_std=True)
    beta= 2.0
    return mu - beta*sigma

def bayesian_optimization(model, data, iterations):
    X = []
    y = []

    for _ in range(5):
        params = sample_random()
        X.append(params)
        val = evaluate(model, data, params)
        y.append(val)

    X = np.array(X)
    y = np.array(y)

    kernel = C(1.0) * Matern(nu=2.5)
    gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True)

    for i in range(iterations):
        gp.fit(X, y)

        candidates = np.random.uniform(param_min, param_max, size=(1000, 3))

        acq = acquisition_ucb(gp, candidates)
        next_param = candidates[np.argmin(acq)]

        next_val = evaluate(model, data, next_param)

        X = np.vstack([X, next_param])
        y = np.append(y, next_val)

        print(f"[{i+1}/iterations] best so far = {y.min():.4f}")
    best_idx = y.argmin()
    return X[best_idx], y[best_idx]

def reset(model, data):
    mujoco.mj_resetData(model, data)

    data.qpos[:] = np.zeros(19, dtype=np.float32)
    data.qvel[:] = np.zeros(18, dtype=np.float32)

    mujoco.mj_forward(model, data)
    return data

def simulate(model, data, params):
    data = reset(model, data)

    kp, damping, friction = params
    model.actuator_gainprm[:,0] = kp
    model.dof_damping[6:] = damping
    model.dof_frictionloss[6:] = friction

    steps = 500
    energy_log = []
    q_traj = []
#    with viewer.launch_passive(model, data) as v:
    for _ in range(steps):
        q_traj.append(data.qpos[7:].copy())
        torque = data.actuator_force.copy()
        dq = data.qvel[6:].copy()
        energy_log.append(np.sum(np.abs(torque * dq * 0.005)))
        mujoco.mj_step(model, data)
#            v.sync()
    
    q_traj = np.array(q_traj)
    energy = float(np.sum(energy_log))

    error = np.abs(q_traj)
    threshold = np.deg2rad(1.0)

    settled_step = None
    for i in range(len(error)):
        if np.all(error < threshold):
            settled_step = i
            break
    settling_time = settled_step * 0.005 if settled_step is not None else 2.5

    return settling_time, energy


def main():
    if not os.path.exists(SCENE_PATH):
        raise FileNotFoundError(SCENE_PATH)

    model = mujoco.MjModel.from_xml_path(SCENE_PATH)
    data = mujoco.MjData(model)

    #print(bayesian_optimization(model, data, 100))

    with viewer.launch_passive(model, data) as view:
        while True:
            mujoco.mj_step(model,data)
            view.sync()

if __name__ == '__main__':
    main()
