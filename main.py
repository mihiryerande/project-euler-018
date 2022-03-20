# Problem 18:
#     Maximum Path Sum 1
#
# Description:
#     By starting at the top of the triangle below and moving to adjacent numbers on the row below,
#       the maximum total from top to bottom is 23.
#
#            (3)
#           (7) 4
#          2 (4) 6
#         8  5 (9) 3
#
#     That is, 3 + 7 + 4 + 9 = 23.
#
#     Find the maximum total from top to bottom of the triangle below:
#
#                                    75
#                                  95  64
#                                17  47  82
#                              18  35  87  10
#                            20  04  82  47  65
#                          19  01  23  75  03  34
#                         88  02  77  73  07  63  67
#                       99  65  04  28  06  16  70  92
#                     41  41  26  56  83  40  80  70  33
#                   41  48  72  33  47  32  37  16  94  29
#                 53  71  44  65  25  43  91  52  97  51  14
#               70  11  33  28  77  73  17  78  39  68  17  57
#             91  71  52  38  17  14  91  43  58  50  27  29  48
#           63  66  04  68  89  53  67  30  73  16  69  87  40  31
#         04  62  98  27  23  09  70  98  73  93  38  53  60  04  23
#
#     NOTE:
#       As there are only 16384 routes, it is possible to solve this problem by trying every route.
#       However, Problem 67, is the same challenge with a triangle containing one-hundred rows;
#         it cannot be solved by brute force, and requires a clever method! ;o)

def read_triangle(filename):
    """
    Reads the number triangle written in the given `filename`.

    Args:
        filename (str): Name of file containing number triangle

    Returns:
        Number triangle as a list of int list
    """
    assert type(filename) == str

    with open(filename, 'r') as f:
        triangle = [list(map(int, line.strip().split())) for line in f.readlines()]
    return triangle


def compute_trellis(triangle):
    """
    Given a number `triangle`, returns a 'trellis',
      computed using dynamic programming,
      which is the same shape as the triangle,
      and each element holds information about the best paths
      starting from the top of the triangle to each cell.

    Args:
        triangle (List[List[int]]): Number triangle

    Returns:
         List[List[Tuple[int, int]]]:
           Trellis storing the best paths from top to each cell.
    """
    # Dynamic programming structure to keep track of the
    #   best paths landing at each point in the triangle
    # Trellis will hold a tuple of...
    #   * Maximum sum achievable by landing at this point in triangle
    #   * -1 or 0, indicating whether best path from above went through left or right element
    trellis = [[(0, 0) for _ in line] for line in triangle]

    # Initialize trellis using first triangle element
    trellis[0][0] = (triangle[0][0], 1)  # 1 here is a dummy value

    # Populate each row of the trellis
    for i in range(1, len(trellis)):
        # Fill in leftmost and rightmost elements, as they both have only one possible incoming path
        trellis[i][0] = (trellis[i-1][0][0] + triangle[i][0], 0)
        trellis[i][-1] = (trellis[i-1][-1][0] + triangle[i][-1], -1)

        # Fill in remaining (inner) entries of trellis row
        for j in range(1, len(trellis[i])-1):
            best_s = max([-1, 0], key=lambda s: trellis[i-1][j+s])
            this_elt = triangle[i][j]
            trellis[i][j] = (trellis[i-1][j+best_s][0] + this_elt, best_s)

    return trellis


def compute_best_path(triangle, trellis):
    """
    Given a number `triangle`, and the corresponding `trellis`,
        returns the maximum achievable total path sum
        walking down the triangle from top to bottom,
        as well as the path elements which produce that total.

    Args:
       triangle (List[List[int]]): Number triangle
       trellis (List[List[Tuple[int, int]]]): Computed trellis

    Returns:
        Tuple of...
          * (int)      Maximum Path Sum
          * (int list) Maximum Path elements
    """
    # First find the index of the best path's endpoint in the final row
    endpoint = max(enumerate(trellis[-1]), key=lambda x: x[1][0])

    # Unpack relevant values
    curr_j = endpoint[0]
    best_sum = endpoint[1][0]

    # Start at that point in the last row,
    #   and walk backwards (up the trellis)
    #   to figure out the path which led there
    curr_i = len(trellis) - 1
    best_path = []  # Best path (first determined in reverse order)
    while curr_i >= 0:
        best_path.append(triangle[curr_i][curr_j])
        step_j = trellis[curr_i][curr_j][1]
        curr_i -= 1  # Step up to previous row
        curr_j += step_j  # Step left/right to the best incoming point
    best_path.reverse()

    return best_sum, best_path


def main(filename):
    """
    Returns the maximum achievable total path sum
      walking down the triangle from top to bottom,
      as well as the path elements which produce that total.

    Args:
        filename (str): Name of file containing number triangle

    Returns:
        Tuple of...
          * (int)      Maximum Path Sum
          * (int list) Maximum Path elements
    """
    assert type(filename) == str

    triangle = read_triangle(filename)

    trellis = compute_trellis(triangle)

    return compute_best_path(triangle, trellis)


if __name__ == '__main__':
    max_sum, max_path = main('triangle.txt')
    print('Maximum Path Sum in provided triangle:')
    print('  {}'.format(max_sum))
    print('Path producing the Maximum Sum:')
    print('  {}'.format('\n  → '.join(map(str, max_path))))
