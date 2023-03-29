import numpy as np


class Matrix:
    def __init__(self, data):
        self.data = data

    @property
    def shape(self):
        """
        We need property to return result as m.shape instead of m.shape()
        """
        return len(self.data), len(self.data[0])

    def __repr__(self):
        return "\n".join(["\t".join([str(cell) for cell in row]) for row in self.data])

    def __getitem__(self, index):
        return self.data[index]

    def __add__(self, other):
        n_rows, n_col = self.shape
        assert isinstance(other, Matrix), f" !!! Unsupported operand type for +: {type(self)} and {type(other)}"
        n_rows_other, n_col_other = other.shape
        assert n_rows == n_rows_other and n_col == n_col_other, \
            f"!!! operands could not be broadcast together with shapes {self.shape} and {other.shape}"

        result = [[self[i][j] + other[i][j] for j in range(n_col)] for i in range(n_rows)]
        return Matrix(data=result)

    def __mul__(self, other):
        n_rows, n_col = self.shape
        assert isinstance(other, Matrix), f" !!! Unsupported operand type for +: {type(self)} and {type(other)}"
        n_rows_other, n_col_other = other.shape
        assert n_rows == n_rows_other and n_col == n_col_other, \
            f"!!! operands could not be broadcast together with shapes {self.shape} and {other.shape}"
        result = [[self[i][j] * other[i][j] for j in range(n_col)] for i in range(n_rows)]
        return Matrix(result)

    def __matmul__(self, other):
        n_rows, n_col = self.shape
        assert isinstance(other, Matrix), f" !!! Unsupported operand type for +: {type(self)} and {type(other)}"
        n_rows_other, n_col_other = other.shape
        assert n_col == n_rows_other, \
            f"!!! operands could not be broadcast together with shapes {self.shape} and {other.shape}"
        result = [[sum(a * b for a, b in zip(X_row, Y_col)) for Y_col in zip(*other.data)] for X_row in self.data]
        return Matrix(result)

    def __ne__(self, other):
        return self.data != other.data

    def __eq__(self, other):
        return self.data == other.data


if __name__ == "__main__":
    a = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
    b = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

    operators = {"+": lambda a, b: a + b,
                 "*": lambda a, b: a * b,
                 "@": lambda a, b: a @ b}

    for op in operators:
        res = operators[op](a, b)
        with open(f"artifacts/easy/matrix{op}.txt", "w+") as f:
            f.write(str(res))

    for op in operators:
        res = operators[op](a, b)
        with open(f"artifacts/medium/matrix{op}.txt", "w+") as f:
            f.write(str(res))
