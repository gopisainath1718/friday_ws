import os
import sys
import mujoco

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URDF_PATH = os.path.join(BASE_DIR, "friday_robot", "friday_robot.urdf")
MJCF_PATH = os.path.join(BASE_DIR, "friday_robot", "friday.xml")

print(f"URDF_PATH : {URDF_PATH}")
def main():

    if not os.path.exists(URDF_PATH):
        print(f"[ERROR] URDF file not found")
        sys.exit(1)

    print(f"[INFO] Loading URDF file")
    model = mujoco.MjModel.from_xml_path(URDF_PATH)

    print(f"[INFO] Saving complied MJCF to {MJCF_PATH}")
    mujoco.mj_saveLastXML(MJCF_PATH, model)

    print(f"[INFO] Done.")

if __name__ == '__main__':
    main()
