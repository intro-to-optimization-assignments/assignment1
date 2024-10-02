class Simplex:
    def __init__(self, z, constraints, solution):
        self.z = z
        self.constraints = constraints
        self.solution = solution
        self.constraints_number = len(constraints)
        self.variables_number = len(constraints[0])
        self.basis = list(range(self.variables_number, self.variables_number + self.constraints_number))

        for i in range(self.constraints_number):
            constraints[i] += [0] * self.constraints_number
            constraints[i][self.variables_number + i] = 1
        self.z += [0] * self.constraints_number

        # print(self.z)
        # print(self.constraints)
        # print(self.basis)


if __name__ == '__main__':
    z = [5, 4]
    constraints = [
        [6, 4],
        [1, 2],
        [-1, 1],
        [1, 0],
    ]
    solution = [24, 6, 1, 2]

    simplex_method = Simplex(z, constraints, solution)
