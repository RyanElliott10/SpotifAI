import random

class Reverse:
    def __init__(self):
        self.train_data = []
        self.target_data = []

    def generate_all(self):
        self.generate_train()
        self.generate_target()

    def generate_train(self):
        for _ in range(10000):
            self.train_data.append([random.randint(0, 1), random.randint(0, 1),
                                    random.randint(0, 1), random.randint(0, 1)])

    def generate_target(self):
        for v in self.train_data:
            self.target_data.append(v[::-1])


class XOR:
    def __init__(self):
        self.train_data = []
        self.target_data = []

    def generate_all(self):
        self.generate_train()
        self.generate_target()

    def generate_train(self):
        for _ in range(10000):
            self.train_data.append([random.randint(0, 1), random.randint(0, 1)])

    def generate_target(self):
        for v in self.train_data:
            self.target_data.append(int(v[0] != v[1]))
