import argparse
import time

from skrobot.model.primitives import Box
from skrobot.models.fetch import Fetch
from skrobot.viewers import PyrenderViewer

from plainmp.ik import solve_ik
from plainmp.robot_spec import FetchSpec
from plainmp.utils import set_robot_state, sksdf_to_cppsdf

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--visualize", action="store_true", help="visualize the result")
    args = parser.parse_args()

    # create table sdf
    table = Box([1.0, 2.0, 0.05], with_sdf=True)
    table.translate([1.0, 0.0, 0.8])
    sdf = sksdf_to_cppsdf(table.sdf, False)

    # create problem
    fs = FetchSpec()
    eq_cst = fs.create_gripper_pose_const([0.7, +0.2, 0.95, 0, 0, 0])
    ineq_cst = fs.create_collision_const()
    ineq_cst.set_sdf(sdf)
    lb, ub = fs.angle_bounds()

    # solve it
    ts = time.time()
    ret = solve_ik(eq_cst, ineq_cst, lb, ub, q_seed=None, max_trial=10)
    print(f"after {ret.n_trial} trials, elapsed time: {(time.time() - ts) * 1000:.2f} msec")
    assert ret.success

    if args.visualize:
        fetch = Fetch()
        set_robot_state(fetch, fs.control_joint_names, ret.q)
        v = PyrenderViewer()
        v.add(fetch)
        v.add(table)
        v.show()
        time.sleep(1000)
