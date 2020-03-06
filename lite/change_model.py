#!/usr/bin/python3

import sys
import os
import time
import shutil
import paddle.fluid as fluid

DEBUG = False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ./{} <model_dir>".format(
            os.path.basename(__file__)))
        exit(0)

    # input parameters
    model_dir = sys.argv[1]  #whole dir
    timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    save_model_dir = "".join([model_dir, "/", "saved-", timestamp])
    os.mkdir(save_model_dir)
    if os.path.exists(model_dir + "/model"):
        model_filename = "model"
    elif os.path.exists(model_dir + "/__model__"):
        model_filename = "__model__"
    else:
        print("[ERROR] No model file `model` or `__model__` found")
        exit(0)

    exe = fluid.Executor(fluid.CPUPlace())
    [inference_program, feed_target_names,
     fetch_targets] = fluid.io.load_inference_model(dirname=model_dir,
                                                    executor=exe)
    ops = inference_program.global_block().ops
    i = 0
    for op in ops:
        print("第{}个op: {}".format(i, op.type))
        if i == 85:
            print(op)
        i = i + 1
    inference_program.global_block()._remove_op(85)
    i = 0
    for op in ops:
        print("第{}个op: {}".format(i, op.type))
        i = i + 1
    print(feed_target_names)
    fluid.io.save_inference_model(dirname=save_model_dir,
                                  feeded_var_names=feed_target_names,
                                  target_vars=fetch_targets,
                                  executor=exe,
                                  main_program=inference_program,
                                  params_filename="__params__")
