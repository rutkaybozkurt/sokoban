import os,copy


class Level:
    matrix = []
    hist_matrix = []

    def __init__(self, level_num):

        del self.matrix[:]
        del self.hist_matrix[:]

        # Create level
        with open(os.path.dirname(os.path.abspath(__file__)) + '/Levels/level' + str(level_num), 'r') as f:
            for row in f.read().splitlines():
                self.matrix.append(list(row))

    def __del__(self):
        "Destructor"

    def get_matrix(self):
        return self.matrix

    def save_history(self, matrix):
        self.hist_matrix.append(copy.deepcopy(matrix))

    def undo(self):
        if len(self.hist_matrix) > 0:
            last_matrix = self.hist_matrix.pop()
            self.matrix = last_matrix
            return last_matrix
        else:
            return self.matrix

    def get_pos(self):
        # Iterate all Rows
        for i in range(0, len(self.matrix)):
            # Iterate all columns
            for k in range(0, len(self.matrix[i]) - 1):
                if self.matrix[i][k] == "@":
                    return [i, k]

    def get_boxes(self):
        boxes = []
        for i in range(0, len(self.matrix)):
            for k in range(0, len(self.matrix[i]) - 1):
                if self.matrix[i][k] == "$":
                    boxes.append([k, i])
        return boxes

    def get_size(self):
        max_row_length = 0
        for i in range(0, len(self.matrix)):
            row_length = len(self.matrix[i])
            if row_length > max_row_length:
                max_row_length = row_length
        return [max_row_length, len(self.matrix)]
