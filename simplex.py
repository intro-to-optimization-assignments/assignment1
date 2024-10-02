from json.encoder import INFINITY


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

        for i in range(self.variables_number):
            self.z[i] *= -1

        self.z += [0] * self.constraints_number

        # print(self.z)
        # print(self.constraints)
        # print(self.basis)

        # [-5, -4, 0, 0, 0, 0]
        # [
        # [6, 4, 1, 0, 0, 0],
        # [1, 2, 0, 1, 0, 0],
        # [-1, 1, 0, 0, 1, 0],
        # [1, 0, 0, 0, 0, 1],
        # ]

        # [2, 3, 4, 5]


    # Gets the index of the entering variable from the z-row
    def define_entering(self):
        min_z = 0
        entering_index = -1

        for elem in self.z:
            if elem >= 0:
                continue

            if elem < min_z:
                min_z = elem
                entering_index = self.z.index(elem)

        return entering_index


    # Gets the index of the leaving variable from the z-row
    def define_leaving(self, entering_index):
        min_elem = INFINITY
        basis_leaving_index = -1

        for i in range(self.constraints_number):
            if self.constraints[i][entering_index] <= 0:
                continue

            # Index of solution is [i + 1] because it also contains z-row value
            ratio = solution[i + 1] / self.constraints[i][entering_index]

            if ratio < min_elem:
                min_elem = ratio
                basis_leaving_index = i

        leaving_index = self.basis[basis_leaving_index]

        return leaving_index




if __name__ == '__main__':
    z = [5, 4]
    constraints = [
        [6, 4],
        [1, 2],
        [-1, 1],
        [1, 0],
    ]
    solution = [0, 24, 6, 1, 2]

    simplex_method = Simplex(z, constraints, solution)

    entering = simplex_method.define_entering()
    leaving = simplex_method.define_leaving(entering)

    print(entering, leaving)
