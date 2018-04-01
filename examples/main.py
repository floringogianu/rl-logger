import sys
from random import randint, random

sys.path.append('')
from rl_logger import Logger


if __name__ == "__main__":

    log = Logger(label="experiment1", path="./examples/results")
    train_log = log.add_group(
        tag="training",
        metrics=(log.MaxMetric("max_q")),
        console_options=("white", "on_blue", ["bold"])
    )

    eval_log = log.add_group(
        tag="evaluation",
        metrics=(log.AvgMetric("rw_per_ep"),
                 log.AvgMetric("rw_per_step"),
                 log.MaxMetric("max_q")),
        console_options=("white", "on_magenta", ["bold"])
    )

    training_steps = 5000001
    done = False

    for step in range(training_steps):
        done = step % 500 == 0 and step != 0

        r, q = randint(0, 1000), random() * randint(0, step)
        # train

        train_log.update(max_q=q)

        if step % 50000 == 0 and step != 0:
            log.log(train_log, step)
            train_log.reset()

        if done:
            done = False

        # Start evaluation
        # ----------------
        eval_step = step
        if step % 250000 == 0 and step != 0:
            done = False
            for i in range(150000):
                done = i % 1500 == 0 and i != 0

                r, q = randint(0, 50), random() * randint(0, 10)
                # evaluate

                eval_log.update(rw_per_ep=(r, (1 if done else 0)),
                                rw_per_step=r,
                                max_q=q)

                if i % 50000 == 0 and i != 0:
                    log.log(eval_log, eval_step)

                if done:
                    # new episode
                    done = False

            log.log(eval_log, eval_step)
            eval_log.reset()

    log.log(train_log, step)
    train_log.reset()
