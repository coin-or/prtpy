import doctest
from Horowitz_And_Sahni import generate_subset_sum


def schroeppel_shamir(s):
    """
        Algorithm 2: get a list, return list that contain all the pair from the groups partitoins.
        This algorithm help to algorithm1 with the partition.
        
        >>> schroeppel_shamir([1, 2, 3, 4, 5])
        ([[], [0, 0], [0, 2], [1, 0], [1, 2]], [[], [3, 9], [3, 5], [3, 4], [3, 0], [0, 9], [0, 5], [0, 4], [0, 0]])

        >>> schroeppel_shamir([1, 2, 3])
        ([[], [0, 0], [0, 1]], [[], [2, 3], [2, 0], [0, 3], [0, 0]])

        >>> schroeppel_shamir([10, 20, 30, 40, 50, 60, 70, 80])
        ([[], [0, 0], [0, 30], [0, 40], [0, 70], [10, 0], [10, 30], [10, 40], [10, 70], [20, 0], [20, 30], [20, 40], [20, 70], [30, 0], [30, 30], [30, 40], [30, 70]], [[], [110, 150], [110, 80], [110, 70], [110, 0], [60, 150], [60, 80], [60, 70], [60, 0], [50, 150], [50, 80], [50, 70], [50, 0], [0, 150], [0, 80], [0, 70], [0, 0]])

       >>> schroeppel_shamir([100, 200, 100, 500])
       ([[], [0, 0], [0, 200], [100, 0], [100, 200]], [[], [100, 500], [100, 0], [0, 500], [0, 0]])

       >>> schroeppel_shamir([0, 0, 0, 0])
       ([[], [0, 0], [0, 0], [0, 0], [0, 0]], [[], [0, 0], [0, 0], [0, 0], [0, 0]])


    """

    # sort s in decrease order
    sorted(s, reverse=True)

    # divide to 4 subset sum

    left_sum = s[:len(s) // 2]
    right_sum = s[len(s) // 2:]

    a0 = left_sum[:len(left_sum) // 2]
    a1 = left_sum[len(left_sum) // 2:]
    b0 = right_sum[:len(right_sum) // 2]
    b1 = right_sum[len(right_sum) // 2:]

    # print("a0 is: ", a0)
    # print("a1 is: ", a1)
    # print("b0 is: ", b0)
    # print("b1 is: ", b1)

    # print()

    subset_sum_a0 = generate_subset_sum(a0)
    subset_sum_a1 = generate_subset_sum(a1)
    subset_sum_b0 = generate_subset_sum(b0)
    subset_sum_b1 = generate_subset_sum(b1)
    # print("subset_sum_a0: ", subset_sum_a0)
    # print("subset_sum_a1: ", subset_sum_a1)
    # print("subset_sum_b0: ", subset_sum_b0)
    # print("subset_sum_b1: ", subset_sum_b1)

    # print()

    list_of_sum_a0 = []
    for i in range(len(subset_sum_a0)):
        list_of_sum_a0.append(sum(subset_sum_a0[i]))
    # print("list_of_sum_a0: ", list_of_sum_a0)

    list_of_sum_a1 = []
    for i in range(len(subset_sum_a1)):
        list_of_sum_a1.append(sum(subset_sum_a1[i]))
    # print("list_of_sum_a1: ", list_of_sum_a1)

    list_of_sum_b0 = []
    for i in range(len(subset_sum_b0)):
        list_of_sum_b0.append(sum(subset_sum_b0[i]))
    # print("list_of_sum_b0: ", list_of_sum_b0)

    list_of_sum_b1 = []
    for i in range(len(subset_sum_b1)):
        list_of_sum_b1.append(sum(subset_sum_b1[i]))
    # print("list_of_sum_b1: ", list_of_sum_b1)
    # print()

    list_of_sum_a0.sort()
    list_of_sum_a1.sort()
    list_of_sum_b0.sort(reverse=True)
    list_of_sum_b1.sort(reverse=True)

    # print("sum of a0 is: ", list_of_sum_a0)
    # print("sum of a1 is: ", list_of_sum_a1)
    # print("sum of b0 is: ", list_of_sum_b0)
    # print("sum of b1 is: ", list_of_sum_b1)
    # print()

    # merge
    ans1 = [[]]
    for i in range(len(list_of_sum_a0)):
        for j in range(len(list_of_sum_a1)):
            pair = [list_of_sum_a0[i], list_of_sum_a1[j]]
            ans1.append(pair)
    # print("ans1 is: ", ans1)

    ans2 = [[]]
    for i in range(len(list_of_sum_b0)):
        for j in range(len(list_of_sum_b1)):
            pair = [list_of_sum_b0[i], list_of_sum_b1[j]]
            ans2.append(pair)
    # print("ans2 is: ", ans2)

    return ans1, ans2


if __name__ == '__main__':
    # doctest.testmod()
    # print(schroeppel_shamir([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    print(schroeppel_shamir([1, 2, 3, 4, 5]))

