from typing import Any

import numpy as np
from random import random


class solver:
    @staticmethod
    def solve_linear(k: float, b: float) -> list:  # solving linear equation kx+b=0
        if k == 0:
            raise ZeroDivisionError()
        return [-b / k]

    @staticmethod
    def solve_quadratic(b: float, c: float) -> dict[str, list[float | Any] | list] | dict[str, list]:  # solving quadratic equation x^2+bx+c=0
        D = b * b - 4 * c

        if D >= 0:
            return {
                "real" : [(-b - np.sqrt(D)) / 2, (-b + np.sqrt(D)) / 2],
                "complex" : []
            }
        else:
            return {
                "real": [],
                "complex": [complex(-0.5 * b, -0.5 * np.sqrt(-D)), complex(-0.5 * b, 0.5 * np.sqrt(-D))]
            }

    @staticmethod
    def solve_cubic(b: float, c: float, d: float, eps=0.001) -> list:  # solving cubic equation x^3+bx^2+cx+d=0
        def f(x):
            b1 = x[0]
            b2 = x[1]
            c2 = x[2]
            return np.array([
                b1 + b2 - b,
                b1 * b2 + c2 - c,
                b1 * c2 - d
            ])

        def j(x):
            b1 = x[0]
            b2 = x[1]
            c2 = x[2]
            return np.array([
                [1, 1, 0],
                [b2, b1, 1],
                [c2, 0, b1]
            ])

        def j1(x):
            return np.linalg.inv(j(x))

        x0 = np.array([random(), random(), random()])
        need_to_repeat = True
        k = 0
        while need_to_repeat and k <= 500:
            x0 = np.array([random(), random(), random()])
            adder = np.zeros(3)
            try:
                adder = - np.matmul(j1(x0), f(x0))
                need_to_repeat = False
            except Exception:
                need_to_repeat = True
                k += 1

        while np.linalg.norm(adder) >= eps:
            x0 += adder
            adder = - np.matmul(j1(x0), f(x0))

        ans = solver.solve_quadratic(x0[1], x0[2])
        ans["real"].append(solver.solve_linear(1, x0[0])[0])
        return ans

    @staticmethod
    def solve_forth(b:float, c:float, d:float, e:float, eps=0.001) -> dict[str, list[float | Any]]:
        def f(x):
            b1 = x[0]
            c1 = x[1]
            b2 = x[2]
            c2 = x[3]
            return np.array([
                b1+b2-b,
                c1+b1*b2+c2-d,
                b1*c2+b2*c1-d,
                c1*c2-e
            ])

        def j(x):
            b1 = x[0]
            c1 = x[1]
            b2 = x[2]
            c2 = x[3]
            return np.array([
                [1, 0, 1, 0],
                [b2, 1, b1, 1],
                [c2, b2, c1, b1],
                [0, c2, 0, c1]
            ])

        def j1(x):
            return np.linalg.inv(j(x))

        x0 = np.array([random(), random(), random(), random()])
        adder = np.zeros(4)
        need_to_repeat = True
        k = 0
        while need_to_repeat and k <= 500:
            x0 = np.array([random(), random(), random(), random()])
            try:
                adder = - np.matmul(j1(x0), f(x0))
                need_to_repeat = False
            except Exception:
                need_to_repeat = True
                k += 1
        while np.linalg.norm(adder) >= eps:
            x0 = x0 + adder
            adder = - np.matmul(j1(x0), f(x0))

        ans1 = solver.solve_quadratic(x0[0], x0[1])
        ans2 = solver.solve_quadratic(x0[2], x0[3])
        return {
            "real" : ans1["real"]+ans2["real"],
            "complex" : ans1["complex"]+ans2["complex"]
        }

