import os
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import mujoco
import mujoco.viewer as viewer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENE_PATH = os.path.join(BASE_DIR, "friday_description", "scene.xml")

def main():
    if not os.path.exists(SCENE_PATH):
        raise FileNotFoundError(SCENE_PATH)

    model = mujoco.MjModel.from_xml_path(SCENE_PATH)
    data = mujoco.MjData(model)

    with viewer.launch_passive(model, data) as view:
        while True:
            mujoco.mj_step(model, data)
            view.sync()

if __name__ == '__main__':
    main()
