from json.encoder import INFINITY


# Prints the basic variables as "x1 = basic_variables_values[0], x2 = basic_variables_values[1],... "
def format_output(basic_variables_values):
    formatted_output = ", ".join(f"x{i + 1} = {value}" for i, value in enumerate(basic_variables_values))
    print(formatted_output)


class Simplex:
    def __init__(self, z, constraints, constraints_rhs, accuracy):
        self._z = z
        self._constraints = constraints
        self._constraints_rhs = constraints_rhs
        self._solution = 0
        self._constraints_number = len(constraints)
        self._basic_variables_number = len(constraints[0])
        self._variables_number = self._basic_variables_number + self._constraints_number
        self._basic_variables = list(range(self._basic_variables_number))
        self._basis = list(
            range(self._basic_variables_number,
                  self._basic_variables_number + self._constraints_number)
        )
        self._accuracy = accuracy

        for i in range(self._constraints_number):
            constraints[i] += [0] * self._constraints_number
            constraints[i][self._basic_variables_number + i] = 1

        for i in range(self._basic_variables_number):
            self._z[i] *= -1

        self._z += [0] * self._constraints_number

    # Computes the maximum value for z
    def compute_maximum(self):
        while True:
            if not self._can_continue():
                basic_variables_values = self._get_basic_variables_values()

                format_output(basic_variables_values)
                return self._solution

            entering = self._define_entering()

            if not self._is_applicable(entering):
                print("The method is not applicable!")
                return None

            leaving = self._define_leaving(entering)
            self._change_pivot(entering, leaving)

    # Computes the minimum value for z
    def compute_minimum(self):
        self._z = [-elem for elem in self._z]
        return -self.compute_maximum()

    # Gets the index of the entering variable from the z-row
    def _define_entering(self):
        min_z = 0
        entering_index = -1

        for elem in self._z:
            if elem >= 0:
                continue

            if elem < min_z:
                min_z = elem
                entering_index = self._z.index(elem)

        return entering_index

    # Gets the index of the leaving variable from the z-row
    def _define_leaving(self, entering_index):
        min_elem = INFINITY
        basis_leaving_index = -1

        for i in range(self._constraints_number):
            if self._constraints[i][entering_index] <= 0:
                continue

            ratio = self._constraints_rhs[i] / self._constraints[i][entering_index]

            if ratio < min_elem:
                min_elem = ratio
                basis_leaving_index = i

        leaving_index = self._basis[basis_leaving_index]

        return leaving_index

    # Changes the "table" for a new pivot
    def _change_pivot(self, entering_index, leaving_index):
        basis_index = self._basis.index(leaving_index)
        self._basis[basis_index] = entering_index

        self._update_constraints(basis_index, entering_index)
        self._update_z_row(basis_index, entering_index)

    # Updates the whole "table"
    def _update_constraints(self, basis_index, entering_index):
        for constr_id in range(self._constraints_number):
            if constr_id == basis_index:
                self._normalize_pivot_row(constr_id, entering_index)
            else:
                self._update_non_pivot_row(constr_id, basis_index, entering_index)

    # Normalizes the pivot row by dividing all elements by the pivot value
    def _normalize_pivot_row(self, constr_id, entering_index):
        divisor = self._constraints[constr_id][entering_index]
        for var_id in range(self._variables_number):
            self._constraints[constr_id][var_id] = self._format(
                self._constraints[constr_id][var_id] / divisor
            )
        self._constraints_rhs[constr_id] = self._format(
            self._constraints_rhs[constr_id] / divisor
        )

    # Updates values in the non-pivot row
    def _update_non_pivot_row(self, constr_id, basis_index, entering_index):
        factor = -(self._constraints[constr_id][entering_index] /
                   self._constraints[basis_index][entering_index])
        for var_id in range(self._variables_number):
            self._constraints[constr_id][var_id] = self._format(
                self._constraints[constr_id][var_id] +
                factor * self._constraints[basis_index][var_id]
            )
        self._constraints_rhs[constr_id] = self._format(
            self._constraints_rhs[constr_id] +
            factor * self._constraints_rhs[basis_index]
        )

    # Updates values in the z-row
    def _update_z_row(self, basis_index, entering_index):
        factor_z = -(self._z[entering_index] /
                     self._constraints[basis_index][entering_index])
        for var_id in range(self._variables_number):
            self._z[var_id] = self._format(
                self._z[var_id] +
                factor_z * self._constraints[basis_index][var_id]
            )
        self._solution = self._format(
            self._solution +
            factor_z * self._constraints_rhs[basis_index]
        )

    # Gets the basic variables values from the constraints_rhs "column"
    def _get_basic_variables_values(self):
        basic_variables_values = []

        for basic_id in self._basic_variables:
            if basic_id in self._basis:
                index = self._basis.index(basic_id)
                basic_variables_values.append(self._constraints_rhs[index])
            else:
                basic_variables_values.append(0)

        return basic_variables_values

    # Returns True if there is at least one negative element in z-row
    def _can_continue(self):
        for elem in self._z:
            if elem < 0: return True
        return False

    # Returns True if for entering variable
    # there is at least one positive value in constraints
    def _is_applicable(self, entering_index):
        for i in range(self._constraints_number):
            if self._constraints[i][entering_index] > 0: return True
        return False

    # Formats the number for the defined accuracy
    def _format(self, num):
        return round(num, self._accuracy)


def main():
    accuracy = 4

    z_mx = [9, 10, 16]
    constraints_mx = [
        [18, 15, 12],
        [6, 4, 8],
        [5, 3, 3],
    ]
    constraints_rhs_mx = [360, 192, 180]

    z_mn = [-2, 2, -6]
    constraints_mn = [
        [2, 1, -2],
        [1, 2, 4],
        [1, -1, 2],
    ]
    constraints_rhs_mn = [24, 23, 10]

    z_inapplicable = [1, 1]
    constraints_inapplicable = [
        [-1, 1],
        [-1, -1],
    ]
    constraints_rhs_inapplicable = [1, -2]

    simplex_method_mx = Simplex(z_mx,
                                constraints_mx,
                                constraints_rhs_mx,
                                accuracy)
    maximum = simplex_method_mx.compute_maximum()
    print(maximum)

    simplex_method_mn = Simplex(z_mn,
                                constraints_mn,
                                constraints_rhs_mn,
                                accuracy)
    minimum = simplex_method_mn.compute_minimum()
    print(minimum)

    simplex_method_inapplicable = Simplex(z_inapplicable,
                                          constraints_inapplicable,
                                          constraints_rhs_inapplicable,
                                          accuracy)
    inapplicable = simplex_method_inapplicable.compute_maximum()
    print(inapplicable is None)




if __name__ == '__main__':
    main()
