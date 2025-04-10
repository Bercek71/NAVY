import math


class LSystem:

    def __init__(self, axiom, rules, angle_deg):

        self.axiom = axiom
        self.rules = rules
        self.angle_deg = angle_deg
        self.angle_rad = math.radians(angle_deg)

    @classmethod
    def from_rule_string(cls, axiom, rule_str, angle_deg):

        rules = cls.parse_rules(rule_str)
        return cls(axiom, rules, angle_deg)

    @staticmethod
    def parse_rules(rule_str):
        rules = {}
        # oddělení pravidel čárkou
        rule_parts = [r.strip() for r in rule_str.split(',')]

        for part in rule_parts:
            if '->' in part:
                left, right = [s.strip() for s in part.split('->')]
                rules[left] = right

        return rules

    def generate(self, iterations):
        result = self.axiom
        # iterativní generování L-systému
        for _ in range(iterations):
            new_result = ""
            for char in result:
                if char in self.rules:
                    new_result += self.rules[char]
                else:
                    new_result += char
            result = new_result
        return result



# předdefinované L-systémy
PREDEFINED_SYSTEMS = [
    {
        "name": "System 1",
        "axiom": "F+F+F+F",
        "rule": "F -> F+F-F-FF+F+F-F",
        "angle": 90
    },
    {
        "name": "System 2",
        "axiom": "F++F++F",
        "rule": "F -> F+F--F+F",
        "angle": 60
    },
    {
        "name": "System 3",
        "axiom": "F",
        "rule": "F -> F[+F]F[-F]F",
        "angle": math.pi / 7 * 180 / math.pi  # Converting to degrees
    },
    {
        "name": "System 4",
        "axiom": "X",
        "rule": "X -> F[+X]F[-X]+X, F -> FF",
        "angle": 20
    }
]