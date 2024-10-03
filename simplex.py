from json.encoder import INFINITY


class Simplex:
    def __init__(self, z, constraints, constraints_rhs, accuracy):
        self.z = z
        self.constraints = constraints
        self.constraints_rhs = constraints_rhs
        self.solution = 0
        self.constraints_number = len(constraints)
        self.variables_number = len(constraints[0])
        self.basis = list(range(self.variables_number, self.variables_number + self.constraints_number))
        self.accuracy = accuracy

        for i in range(self.constraints_number):
            constraints[i] += [0] * self.constraints_number
            constraints[i][self.variables_number + i] = 1

        for i in range(self.variables_number):
            self.z[i] *= -1

        self.z += [0] * self.constraints_number
        self.variables_number = len(self.constraints[0])

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

            ratio = self.constraints_rhs[i] / self.constraints[i][entering_index]

            if ratio < min_elem:
                min_elem = ratio
                basis_leaving_index = i

        leaving_index = self.basis[basis_leaving_index]

        return leaving_index

    # Changes the "table" for a new pivot
    def change_pivot(self, entering_index, leaving_index):
        basis_index = self.basis.index(leaving_index)
        self.basis[basis_index] = entering_index
        print(self.basis)

        for constr_id in range(self.constraints_number):

            # If it is a pivot row then we divide it such that the pivot variable = 1
            if constr_id == basis_index:
                divisor = self.constraints[constr_id][entering_index]

                for var_id in range(self.variables_number):
                    self.constraints[constr_id][var_id] = self.format(
                        self.constraints[constr_id][var_id] / divisor
                    )
                self.constraints_rhs[constr_id] = self.format(
                    self.constraints_rhs[constr_id] / divisor
                )

            # Else we sum current row with (factor * pivot row)
            else:
                factor = -(self.constraints[constr_id][entering_index] /
                           self.constraints[basis_index][entering_index])

                for var_id in range(self.variables_number):
                    self.constraints[constr_id][var_id] = self.format(
                        self.constraints[constr_id][var_id] +
                        factor * self.constraints[basis_index][var_id]
                    )

                self.constraints_rhs[constr_id] = self.format(
                    self.constraints_rhs[constr_id] +
                    factor * self.constraints_rhs[basis_index]
                )

        # Apply changes to z-row
        factor_z = -(self.z[entering_index] /
                     self.constraints[basis_index][entering_index])

        for var_id in range(self.variables_number):
            self.z[var_id] = self.format(
                self.z[var_id] +
                factor_z * self.constraints[basis_index][var_id]
            )
        self.solution = self.format(
            self.solution +
            factor_z * self.constraints_rhs[basis_index]
        )

        # print(self.z, self.solution)
        # for row in self.constraints:
        #     print(" ".join(f"{val:3}" for val in row))

    # Returns True if there is at least one negative element in z-row
    def can_continue(self):
        for elem in self.z:
            if elem < 0: return True

    # Returns True if for entering variable
    # there is at least one positive value in constraints
    def is_applicable(self, entering_index):
        for elem in self.constraints[entering_index]:
            if elem > 0: return True

    def format(self, num):
        return round(num, self.accuracy)


def main():
    z = [9, 10, 16]
    constraints = [
        [18, 15, 12],
        [6, 4, 8],
        [5, 3, 3],
    ]
    constraints_rhs = [360, 192, 180]
    accuracy = 4

    simplex_method = Simplex(z, constraints, constraints_rhs, accuracy)

    entering = simplex_method.define_entering()
    leaving = simplex_method.define_leaving(entering)

    print(entering, leaving)
    print(simplex_method.can_continue(), simplex_method.is_applicable(entering))

    simplex_method.change_pivot(entering, leaving)


if __name__ == '__main__':
    main()
