import math

class EasingFunction:
    def out(self, t, weight=1):
        raise NotImplementedError

    def in_(self, t, weight=1):
        raise NotImplementedError

    def in_out(self, t, weight=1):
        raise NotImplementedError

    def out_in(self, t, weight=1):
        raise NotImplementedError

class Exponential(EasingFunction):
    def in_(self, t, weight=1):
        return weight * (0 if t == 0 else 2 ** (10 * (t - 1)))

    def out(self, t, weight=1):
        return weight * (1 if t == 1 else 1 - 2 ** (-10 * t))

    def in_out(self, t, weight=1):
        if t == 0 or t == 1:
            return weight * t
        t *= 2
        if t < 1:
            return weight * 0.5 * 2 ** (10 * (t - 1))
        return weight * 0.5 * (2 - 2 ** (-10 * (t - 1)))

    def out_in(self, t, weight=1):
        if t < 0.5:
            return weight * 0.5 * self.out(t * 2)
        return weight * (0.5 * self.in_(t * 2 - 1) + 0.5)

class Quad(EasingFunction):
    def in_(self, t, weight=1):
        return weight * (t * t)

    def out(self, t, weight=1):
        return weight * (1 - (1 - t) * (1 - t))

    def in_out(self, t, weight=1):
        return weight * ((t / 0.5) ** 2 if t < 0.5 else 1 - ((1 - t) * (1 - t)) * 0.5)

    def out_in(self, t, weight=1):
        return weight * (0.5 * (t / 0.5) ** 2 if t < 0.5 else 0.5 * (1 - ((1 - t) * (1 - t)) * 0.5))

class Back(EasingFunction):
    def in_(self, t, weight=1):
        c1 = 1.70158
        c2 = c1 * 1.525
        return weight * (t ** 2 * ((c2 + 1) * t - c2))

    def out(self, t, weight=1):
        c1 = 1.70158
        c2 = c1 * 1.525
        t -= 1
        return weight * ((t ** 2) * ((c2 + 1) * t + c2) + 1)

    def in_out(self, t, weight=1):
        c1 = 1.70158
        c2 = c1 * 1.525
        t *= 2
        if t < 1:
            return weight * 0.5 * (t ** 2 * ((c2 + 1) * t - c2))
        t -= 2
        return weight * 0.5 * ((t ** 2 * ((c2 + 1) * t + c2)) + 2)

    def out_in(self, t, weight=1):
        if t < 0.5:
            return weight * 0.5 * self.out(t * 2)
        return weight * (0.5 * self.in_(t * 2 - 1) + 0.5)

class Bounce(EasingFunction):
    def out(self, t, weight=1):
        n1 = 7.5625
        d1 = 2.75
        if t < 1 / d1:
            return weight * n1 * t * t
        elif t < 2 / d1:
            t -= 1.5 / d1
            return weight * n1 * (t * t + 0.75)
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return weight * n1 * (t * t + 0.9375)
        else:
            t -= 2.625 / d1
            return weight * n1 * (t * t + 0.984375)

    def in_(self, t, weight=1):
        return weight * (1 - self.out(1 - t))

    def in_out(self, t, weight=1):
        return weight * (0.5 * self.in_(t * 2) if t < 0.5 else 0.5 * self.out(t * 2 - 1) + 0.5)

    def out_in(self, t, weight=1):
        return weight * (0.5 * self.out(t * 2) if t < 0.5 else 0.5 * self.in_(t * 2 - 1) + 0.5)

class Elastic(EasingFunction):
    def in_(self, t, weight=1):
        if t == 0 or t == 1:
            return weight * t
        p = 0.3
        s = p / 4
        return weight * -(2 ** (10 * (t - 1))) * math.sin((t - s) * (2 * math.pi) / p)

    def out(self, t, weight=1):
        if t == 0 or t == 1:
            return weight * t
        p = 0.3
        s = p / 4
        return weight * ((2 ** (-10 * t)) * math.sin((t - s) * (2 * math.pi) / p) + 1)

    def in_out(self, t, weight=1):
        if t == 0 or t == 1:
            return weight * t
        t *= 2
        p = 0.45
        s = p / 4
        if t < 1:
            return weight * -0.5 * (2 ** (10 * (t - 1))) * math.sin((t - s) * (2 * math.pi) / p)
        return weight * ((2 ** (-10 * (t - 1))) * math.sin((t - s) * (2 * math.pi) / p) * 0.5 + 1)

    def out_in(self, t, weight=1):
        if t < 0.5:
            return weight * 0.5 * self.out(t * 2)
        return weight * (0.5 * self.in_(t * 2 - 1) + 0.5)

class Sine(EasingFunction):
    def in_(self, t, weight=1):
        return weight * (1 - math.cos((t * math.pi) / 2))

    def out(self, t, weight=1):
        return weight * math.sin((t * math.pi) / 2)

    def in_out(self, t, weight=1):
        return weight * 0.5 * (1 - math.cos(math.pi * t))

    def out_in(self, t, weight=1):
        if t < 0.5:
            return weight * 0.5 * self.out(t * 2)
        return weight * (0.5 * self.in_(t * 2 - 1) + 0.5)

class Circ(EasingFunction):
    def in_(self, t, weight=1):
        return weight * (1 - math.sqrt(1 - (t ** 2)))

    def out(self, t, weight=1):
        t -= 1
        return weight * math.sqrt(1 - (t ** 2))

    def in_out(self, t, weight=1):
        t *= 2
        if t < 1:
            return weight * 0.5 * (1 - math.sqrt(1 - (t ** 2)))
        t -= 2
        return weight * 0.5 * (math.sqrt(1 - (t ** 2)) + 1)

    def out_in(self, t, weight=1):
        if t < 0.5:
            return weight * 0.5 * self.out(t * 2)
        return weight * (0.5 * self.in_(t * 2 - 1) + 0.5)

class Cubic(EasingFunction):
    def in_(self, t, weight=1):
        return weight * (t ** 3)

    def out(self, t, weight=1):
        t -= 1
        return weight * ((t ** 3) + 1)

    def in_out(self, t, weight=1):
        t *= 2
        if t < 1:
            return weight * 0.5 * (t ** 3)
        t -= 2
        return weight * 0.5 * ((t ** 3) + 2)

    def out_in(self, t, weight=1):
        if t < 0.5:
            return weight * 0.5 * self.out(t * 2)
        return weight * (0.5 * self.in_(t * 2 - 1) + 0.5)

class Quart(EasingFunction):
    def in_(self, t, weight=1):
        return weight * (t ** 4)

    def out(self, t, weight=1):
        t -= 1
        return weight * ((t ** 4) + 1)

    def in_out(self, t, weight=1):
        t *= 2
        if t < 1:
            return weight * 0.5 * (t ** 4)
        t -= 2
        return weight * 0.5 * ((t ** 4) + 2)

    def out_in(self, t, weight=1):
        if t < 0.5:
            return weight * 0.5 * self.out(t * 2)
        return weight * (0.5 * self.in_(t * 2 - 1) + 0.5)

class Quint(EasingFunction):
    def in_(self, t, weight=1):
        return weight * (t ** 5)

    def out(self, t, weight=1):
        t -= 1
        return weight * ((t ** 5) + 1)

    def in_out(self, t, weight=1):
        t *= 2
        if t < 1:
            return weight * 0.5 * (t ** 5)
        t -= 2
        return weight * 0.5 * ((t ** 5) + 2)

    def out_in(self, t, weight=1):
        if t < 0.5:
            return weight * 0.5 * self.out(t * 2)
        return weight * (0.5 * self.in_(t * 2 - 1) + 0.5)


def mix_easing(t, *easing_funcs_and_weights):
    total_weight = sum(weight for weight, _ in easing_funcs_and_weights)
    result = 0
    for weight, easing_func in easing_funcs_and_weights:
        result += (weight / total_weight) * easing_func(t)
    return result