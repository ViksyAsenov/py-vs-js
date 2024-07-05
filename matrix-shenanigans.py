import unittest

# TASK
# The input is a 9 by 9 matrix filled with zeros.
# If there are 5 or more adjacent positions of the same number in a straight line, they need to be printed.
# A straight line can be vertical, horizontal or a diagonal.
# 5 is a magical number, that can be used to complete any line.


def getAdjacentLinesIfOver5(matrix):
    matrixLength = 9
    directionToProcessedMap = {
        (0, 1): set(),  # right
        (1, 0): set(),  # down
        (1, 1): set(),  # down right
        (1, -1): set(),  # down left
    }

    def getLineIfExists(row, col, rowStep, colStep, processed):
        output = []
        currentValue = matrix[row][col]

        # If we are starting from a 5 that means it is possible to have a sequence, eg. 5,5,5,6,6
        # So we need to move on and take the next possible number (not 0 or 5) to use as a current value
        if currentValue == 5:
            newRow = row + rowStep
            newCol = col + colStep

            while (
                0 <= newRow < matrixLength
                and 0 <= newCol < matrixLength
                and (matrix[newRow][newCol] != 0 and currentValue == 5)
            ):
                currentValue = matrix[newRow][newCol]
                newRow += rowStep
                newCol += colStep

        # Save the start of the path so we can add it later to the processed set
        start = (row, col)

        while (
            0 <= row < matrixLength
            and 0 <= col < matrixLength
            and (
                matrix[row][col] == currentValue or matrix[row][col] == 5
            )  # If we are already in a sequence, eg. 6,6,5,6,6, we need to count 5 as if it is the current value
        ):
            output.append((row, col))
            row += rowStep
            col += colStep

        if len(output) >= 5:
            # Calculate end of the path, we remove the previous steps because they have been incremented
            # by the traversing algorithm
            end = (row - rowStep, col - colStep)

            processed.add((start, end))

            return tuple(output)

        return None

    def isOverlap(row, col, processed):
        for start, end in processed:
            # Check if we are inside a horizontal line
            if row == start[0] and row == end[1] and start[1] < col < end[1]:
                return True

            # Check if we are inside a vertical line
            if start[0] < row < end[0] and col == start[1] and col == end[1]:
                return True

            # Check if we are inside a diagonal line
            if start[0] < row < end[0] and start[1] < col < end[1]:
                return True

        return False

    output = []
    for row in range(matrixLength):
        for col in range(matrixLength):
            if matrix[row][col] != 0:
                for (rowStep, colStep), processed in directionToProcessedMap.items():
                    if not isOverlap(row, col, processed):
                        line = getLineIfExists(row, col, rowStep, colStep, processed)
                        if line:
                            output.append(line)

    return output


class TestGetAdjacentLinesIfOver5(unittest.TestCase):
    def test_horizontalMatrix(self):
        horizontalMatrix = [
            [1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 5, 5, 5, 5, 5, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Output for horizontalMatrix should be
        # ((0,0),(0,1),(0,2),(0,3),(0,4))
        # ((2,2),(2,3),(2,4),(2,5),(2,6))
        # ((5,4),(5,5),(5,6),(5,7),(5,8))
        # ((7,4),(7,5),(7,6),(7,7),(7,8))

        result = getAdjacentLinesIfOver5(horizontalMatrix)

        expected = [
            ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4)),
            ((2, 2), (2, 3), (2, 4), (2, 5), (2, 6)),
            ((5, 4), (5, 5), (5, 6), (5, 7), (5, 8)),
            ((7, 4), (7, 5), (7, 6), (7, 7), (7, 8)),
        ]
        self.assertEqual(result, expected)

    def test_verticalMatrix(self):
        verticalMatrix = [
            [2, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 2],
        ]

        # Output for verticalMatrix should be
        # ((0,0),(1,0),(2,0),(3,0),(4,0))
        # ((4,8),(5,8),(6,8),(7,8),(8,8))

        result = getAdjacentLinesIfOver5(verticalMatrix)

        expected = [
            ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)),
            ((4, 8), (5, 8), (6, 8), (7, 8), (8, 8)),
        ]
        self.assertEqual(result, expected)

    def test_diagonalMatrix(self):
        diagonalMatrix = [
            [7, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 7, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Output for diagonalMatrix should be
        # ((0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6))

        result = getAdjacentLinesIfOver5(diagonalMatrix)

        expected = [((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6))]
        self.assertEqual(result, expected)

    def test_comboMatrix(self):
        comboMatrix = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [3, 3, 5, 3, 3, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Output for comboMatrix should be
        # ((1,0),(1,1),(1,2),(1,3),(1,4))
        # ((1,2),(2,2),(3,2),(4,2),(5,2),(6,2))

        result = getAdjacentLinesIfOver5(comboMatrix)

        expected = [
            ((1, 0), (1, 1), (1, 2), (1, 3), (1, 4)),
            ((1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)),
        ]
        self.assertEqual(result, expected)

    def test_ultimateMatrix(self):
        ultimateMatrix = [
            [0, 0, 0, 3, 0, 0, 0, 0, 0],
            [3, 3, 5, 3, 3, 0, 0, 0, 0],
            [0, 0, 6, 3, 0, 5, 0, 0, 0],
            [0, 0, 6, 3, 5, 0, 0, 0, 0],
            [0, 0, 6, 5, 0, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0, 0, 0, 0],
            [0, 5, 6, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 5, 7, 5, 5],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Output for ultimateMatrix should be
        # ((0,3),(1,3),(2,3),(3,3),(4,3))
        # ((1,0),(1,1),(1,2),(1,3),(1,4))
        # ((1,2),(2,2),(3,2),(4,2),(5,2),(6,2))
        # ((2,5),(3,4),(4,3),(5,2),(6,1))
        # ((7,4),(7,5),(7,6),(7,7),(7,8))

        result = getAdjacentLinesIfOver5(ultimateMatrix)
        expected = [
            ((0, 3), (1, 3), (2, 3), (3, 3), (4, 3)),
            ((1, 0), (1, 1), (1, 2), (1, 3), (1, 4)),
            ((1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)),
            ((2, 5), (3, 4), (4, 3), (5, 2), (6, 1)),
            ((7, 4), (7, 5), (7, 6), (7, 7), (7, 8)),
        ]
        self.assertEqual(result, expected)

    def test_edgeCaseMatrix(self):
        edgeCaseMatrix = [
            [1, 1, 1, 1, 5, 6, 6, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Output for edgeCaseMatrix should be
        # ((0,0),(0,1),(0,2),(0,3),(0,4))
        # ((0,4),(0,5),(0,6),(0,7),(0,8))

        result = getAdjacentLinesIfOver5(edgeCaseMatrix)
        expected = [
            ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4)),
            ((0, 4), (0, 5), (0, 6), (0, 7), (0, 8)),
        ]
        self.assertEqual(result, expected)


unittest.main()
