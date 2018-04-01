import unittest
import random
from metrics import MaxMetric, SumMetric, AvgMetric


class TestMaxMetric(unittest.TestCase):

    def test_construction(self):
        self.assertRaises(AssertionError, MaxMetric, None)
        self.assertRaises(AssertionError, MaxMetric, "")

    def test_add_scalar(self):
        """ max_metric._get() returns 23 """

        m = MaxMetric(name="maxQ")
        val = 23
        m._update(val)
        self.assertEqual(m._get(), val)

    def test_add_many_scalars(self):
        """ max_metric._get() returns 1 """

        m = MaxMetric(name="maxQ")
        vals = [-23, 0.97, 1]
        for idx, val in enumerate(vals):
            m._update(val)

        self.assertEqual(m._get(), max(vals))

    def test_add_and_reset(self):
        m = MaxMetric(name="loss")
        control_loss = []

        for i in range(10):
            loss = -random.random() - random.randint(0, 5)
            m._update(loss)
            control_loss.append(loss)

            if i % 5 == 0 and i != 0:
                self.assertEqual(m._get(), max(control_loss))
                m._reset()
                control_loss = []


class TestSumMetric(unittest.TestCase):

    def test_construction(self):
        self.assertRaises(AssertionError, SumMetric, None)
        self.assertRaises(AssertionError, SumMetric, "")

    def test_add_scalar(self):
        """ sum_metric._get() returns 23 """

        m = SumMetric(name="reward_per_episode")
        val = 23
        m._update(val)
        self.assertEqual(m._get(), val)

    def test_add_many_scalars(self):
        """ sum_metric._get() returns -21.03 """

        m = SumMetric(name="reward_per_episode")
        vals = [-23, 0.97, 1]
        for idx, val in enumerate(vals):
            m._update(val)

        self.assertEqual(m._get(), sum(vals))

    def test_add_and_reset(self):
        m = SumMetric(name="loss")
        control_loss = []

        for i in range(10):
            loss = - random.random() - random.randint(0, 5)
            m._update(loss)
            control_loss.append(loss)

            if i % 5 == 0 and i != 0:
                self.assertEqual(m._get(), sum(control_loss))
                m._reset()
                control_loss = []

    def test_with_reporting_frequency(self):
        m = SumMetric(name="loss")
        control_loss = []
        step_num = 500
        # eval_freq = 100
        ep_len = 10

        for i in range(step_num):
            loss = i
            done = i % ep_len == 0 and i != 0

            m._update(loss)
            control_loss.append(loss)

            if done:
                self.assertEqual(m._get(), sum(control_loss))
                m._reset()
                control_loss = []


class TestAvgMetric(unittest.TestCase):

    def test_construction(self):
        self.assertRaises(AssertionError, AvgMetric, None)
        self.assertRaises(AssertionError, AvgMetric, "")

    def test_add_scalar(self):
        """ sum_metric._get() returns 23 """

        m = AvgMetric(name="reward_per_episode")
        val = 23
        m._update(val)
        self.assertEqual(m._get(), val)

    def test_add_many_scalars(self):
        """ sum_metric._get() returns -21.03 """

        m = AvgMetric(name="reward_per_episode")
        vals = [-23, 0.97, 1]
        for idx, val in enumerate(vals):
            m._update(val)

        self.assertEqual(m._get(), sum(vals) / len(vals))

    def test_add_and_reset(self):
        m = AvgMetric(name="loss")
        control_loss = []

        for i in range(10):
            loss = - random.random() - random.randint(0, 5)

            m._update(loss)
            control_loss.append(loss)

            if i % 5 == 0 and i != 0:
                self.assertEqual(m._get(),
                                 sum(control_loss) / len(control_loss))
                m._reset()
                control_loss = []

    def test_with_different_n(self):
        m = AvgMetric(name="loss")
        control_loss = []
        control_ep = 0

        step_num = 500
        ep_len = 10

        for i in range(step_num):
            loss = i
            done = i % ep_len == 0 and i != 0

            m._update(loss, n=(1 if done else 0))
            control_loss.append(loss)

            if done:
                control_ep += 1
                self.assertEqual(m._get(), sum(control_loss) / control_ep)
                m._reset()
                control_ep = 0
                control_loss = []
