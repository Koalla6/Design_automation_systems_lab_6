import copy
import numpy as np


def Initial_Conditions():
    field = [["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],  # 1
             ["_", "H", "_", "_", "_", "_", "_", "_", "_", "_"],  # 2
             ["_", "_", "_", "_", "_", "C", "_", "_", "_", "_"],  # 3
             ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],  # 4
             ["_", "_", "B", "_", "_", "_", "_", "_", "_", "_"],  # 5
             ["_", "_", "_", "_", "_", "_", "_", "F", "_", "_"],  # 6
             ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"],  # 7
             ["_", "_", "_", "E", "_", "_", "_", "_", "_", "_"],  # 8
             ["_", "_", "_", "_", "_", "_", "D", "_", "_", "_"],  # 9
             ["_", "A", "_", "_", "_", "_", "_", "_", "_", "_"],  # 10
             ["_", "_", "_", "_", "_", "_", "_", "_", "_", "_"]]  # 11

    vertexes = ["A", "B", "C", "D", "E", "F", "H"]
    matr = [[0, 2, 0, 2, 0, 0, 0],  # A
            [2, 0, 1, 0, 0, 1, 0],  # B
            [0, 1, 0, 0, 1, 1, 0],  # C
            [2, 0, 0, 0, 2, 0, 0],  # D
            [0, 0, 1, 2, 0, 0, 1],  # E
            [0, 1, 1, 0, 0, 0, 2],  # F
            [0, 0, 0, 0, 1, 2, 0]]  # H
    #    A, B, C, D, E, F, H
    iter = 1
    field_list = []
    # print("Initial_Conditions")
    field_list.append(field)
    print("\n\t\tІтерація №", iter)
    Print_Field(field_list[-1])
    Selection_Of_Items(matr, vertexes, field, iter, field_list)


def Print_Field(field_list):
    print("\tМонтажне поле має вигляд:")

    for i in field_list:
        print(i)


def Selection_Of_Items(matr, vertexes, field, iter, field_list):
    # print("Selection_Of_Items")
    sum = []
    for i in range(len(vertexes)):
        sum.append(0)
        for j in range(len(vertexes)):
            sum[i] += matr[i][j]
    # print(sum)

    sum_sort = sum.copy()
    sum_sort.sort(reverse=True)
    # print("sum_sort", sum_sort)
    i = 0
    while i < len(sum) - 2:
        # print(vertexes[i], i)
        if sum[i] < sum_sort[0] and sum[-2] == sum[-1]:
            break
        elif sum[i] < sum_sort[0]:
            vertexes.append(vertexes.pop(vertexes.index(vertexes[i])))
            sum.append(sum.pop(sum.index(sum[i])))
            matr = Change_Matrix(matr, i)
        else:
            i += 1

    i = 0
    while i < len(sum):
        # changeVertexes = vertexes.copy()
        for j in range(len(sum)):
            if matr[sum.index(sum[0])][j] != 0:
                # print(matr[sum.index(sum[0])][j], "-", sum.index(sum[0])+1, ",", j+1)
                print("Проведемо шлях від ", vertexes[0], "до", vertexes[j])
                iter += 1
                # changeVertexes.remove(changeVertexes[j])
                field_list = Construction_Of_Routes(matr, vertexes, field, iter, field_list, vertexes[0], vertexes[j])
                # Construction_Of_Routes(matr, vertexes, field, iter, field_list, vertexes[0], vertexes[j])

        _ = matr.pop(0)
        for k in range(len(matr)):
            _ = matr[k].pop(0)

        sum.remove(sum[0])
        vertexes.remove(vertexes[0])

    Merge_Fields(field, field_list)


def Merge_Fields(field, field_list):
    montage = []
    for i in range(len(field_list)):
        montage.append(i)
    # print(montage)

    montage_field = copy.deepcopy(field)

    i = 0
    while i < len(montage) - 1:
        # print("i - ", i)
        for y in range(len(field_list[0])):  # ширина
            for x in range(len(field_list[0]) - 1):  # висота
                if field_list[i][y][x] == field_list[i + 1][y][x]:
                    montage_field[y][x] = field_list[i][y][x]
                elif field_list[i][y][x] != field_list[i + 1][y][x] and field_list[i][y][x] == "#" or \
                        field_list[i + 1][y][x] == "#":
                    montage_field[y][x] = "#"
        i += 1
    print("\n\t\tОстаточний вигляд")
    Print_Field(montage_field)


def Change_Matrix(matr, p):
    # print("Change_Matrix")
    arr = np.array(matr)
    while p < len(arr) - 1:
        # print(p)
        point1 = p
        point2 = p + 1
        for i in range(len(arr)):
            arr[i][point2], arr[i][point1] = arr[i][point1], arr[i][point2]
        arr[[point2, point1]] = arr[[point1, point2]]
        p += 1
    matr = arr.tolist()
    return matr


def Construction_Of_Routes(matr, vertexes, field, iter, field_list, point1, point2):
    # print("Construction_Of_Routes")
    # print(point1, point2)

    temporary_field = copy.deepcopy(field_list[-1])

    sx = sy = ex = ey = 0
    # Print_Field(iter, temporary_field)

    for i in range(len(temporary_field)):
        for j in range(len(temporary_field) - 1):
            if temporary_field[i][j] == point1:
                # print("початкова temporary_field[", i, "][", j, "]:", temporary_field[i][j], point1)
                sx = i
                sy = j
                # temporary_field_list[i][j] = 0
            elif temporary_field[i][j] == point2:
                # print("кінцева temporary_field[", i, "][", j, "]:", temporary_field[i][j], point2)
                ex = i
                ey = j

    temporary_field[sx][sy] = 0
    # print("\n")
    # Print_Field(iter, temporary_field)

    add = True
    step = 0
    while (add == True):
        # noChanges = 0
        num = 0
        stop = 0
        add = False
        for y in range(len(temporary_field)):  # ширина
            for x in range(len(temporary_field) - 1):  # висота
                if temporary_field[y][x] == step:
                    if x - 1 >= 0 and temporary_field[y][x - 1] != "#":  # зліва
                        if temporary_field[y][x - 1] == point2:
                            # Print_Field(iter, temporary_field)
                            # iter += 1
                            temporary_field = Change_Route(temporary_field, point2, iter, point1, vertexes)
                            break
                        elif temporary_field[y][x - 1] == "_":
                            temporary_field[y][x - 1] = step + 1
                            num += 1
                            # noChanges = 0
                            add = True
                        # elif temporary_field[y][x - 1] == "#": # or temporary_field[y][x - 1] == step - 1:
                        #     noChanges += 1

                    if x + 1 >= 0 and (x + 1) < (len(temporary_field) - 1) and \
                            temporary_field[y][x + 1] != "#":  # справа
                        if temporary_field[y][x + 1] == point2:
                            # Print_Field(iter, temporary_field)
                            # iter += 1
                            temporary_field = Change_Route(temporary_field, point2, iter, point1, vertexes)
                            break
                        elif temporary_field[y][x + 1] == "_":
                            temporary_field[y][x + 1] = step + 1
                            num += 1
                            # noChanges = 0
                            add = True
                        # elif temporary_field[y][x + 1] == "#":# or temporary_field[y][x + 1] == step - 1:
                        #     noChanges +=1

                    if y - 1 >= 0 and temporary_field[y - 1][x] != "#":  # знизу
                        if temporary_field[y - 1][x] == point2:
                            # Print_Field(iter, temporary_field)
                            temporary_field = Change_Route(temporary_field, point2, iter, point1, vertexes)
                            break
                        elif temporary_field[y - 1][x] == "_":
                            temporary_field[y - 1][x] = step + 1
                            num += 1
                            # noChanges = 0
                            add = True
                        # elif temporary_field[y - 1][x] == "#":# or temporary_field[y - 1][x] == step - 1:
                        #     noChanges += 1

                    if y + 1 >= 0 and (y + 1) < len(temporary_field) and temporary_field[y + 1][x] != "#":  # зверху
                        if temporary_field[y + 1][x] == point2:
                            # Print_Field(iter, temporary_field)
                            # iter += 1
                            temporary_field = Change_Route(temporary_field, point2, iter, point1, vertexes)
                            break
                        elif temporary_field[y + 1][x] == "_":
                            temporary_field[y + 1][x] = step + 1
                            num += 1
                            # noChanges = 0
                            add = True

                    # Print_Field(iter, temporary_field)
                    # print(y, "|", x, ":", temporary_field[y][x])
                    # print("iter =", iter)
                    # print("1)", y, "|", x - 1, "=", temporary_field[y][x - 1])
                    if x - 1 >= 0 and temporary_field[y][x - 1] == 0 or temporary_field[y][x - 1] == "#" or \
                            temporary_field[y][x - 1] == step - 1:  # зліва
                        # print((x + 1) < (len(field) - 1))
                        # print("2)", y, "|", x + 1, "=", temporary_field[y][x + 1])
                        if (x + 1 >= 0 and (x + 1) < (len(temporary_field) - 1)) and (temporary_field[y][x + 1] == 0 or \
                                                                                      temporary_field[y][x + 1] == "#" or \
                                                                                      temporary_field[y][x + 1] == step - 1):  # справа
                            # print("3)", y - 1, "|", x, "=", temporary_field[y - 1][x])
                            if y - 1 >= 0 and temporary_field[y - 1][x] == 0 or temporary_field[y - 1][x] == "#" or \
                                    temporary_field[y - 1][x] == step - 1:  # знизу
                                # print("4)", y + 1, "|", x, "=", temporary_field[y + 1][x])
                                if y + 1 >= 0 and (y + 1) < len(temporary_field) and temporary_field[y + 1][x] == 0 or \
                                        temporary_field[y + 1][x] == "#" or temporary_field[y + 1][x] == step - 1:  # зверху
                                    stop += 1

        # print("\tstop = ", stop)
        # print("num = ", num)

        if stop == 1 and num == 0:
            field_list.append(field)
            # print("inside")
            for i in field_list[-1]:
                print(i)
            field_list = Construction_Of_Routes(matr, vertexes, field, iter, field_list, point1, point2)
            return field_list

        if add:
            step += 1
        else:
            for y in range(len(temporary_field)):  # ширина
                for x in range(len(temporary_field) - 1):  # висота
                    if isinstance(temporary_field[y][x], int) and temporary_field[y][x] != 0:
                        temporary_field[y][x] = "_"
                    elif isinstance(temporary_field[y][x], int) and temporary_field[y][x] == 0:
                        temporary_field[y][x] = point1

    field_list[-1] = temporary_field

    return field_list


def Change_Route(temporary_field, point2, iter, point1, vertexes):
    # print("Change_Route")
    change = True
    # sum = []
    max = 0
    while (change == True):
        change = False
        for y in range(len(temporary_field)):  # ширина
            for x in range(len(temporary_field) - 1):  # висота
                if temporary_field[y][x] == point2:
                    if isinstance(temporary_field[y][x - 1], int) == True and temporary_field[y][x - 1] > max:
                        max = temporary_field[y][x - 1]
                        maxij = [y, x - 1]
                        change = True
                    elif isinstance(temporary_field[y][x + 1], int) == True and temporary_field[y][x + 1] > max:
                        max = temporary_field[y][x + 1]
                        maxij = [y, x + 1]
                        change = True
                    elif isinstance(temporary_field[y - 1][x], int) == True and temporary_field[y - 1][x] > max:
                        max = temporary_field[y - 1][x]
                        maxij = [y - 1, x]
                        change = True
                    elif isinstance(temporary_field[y + 1][x], int) == True and temporary_field[y + 1][x] > max:
                        max = temporary_field[y + 1][x]
                        maxij = [y + 1, x]
                        change = True
    # print(maxij, ":", max)

    # Print_Field(iter, temporary_field)
    temporary_field = Replace_Numbers(temporary_field, max, maxij, iter, point1, vertexes)

    return temporary_field


def Replace_Numbers(temporary_field, max, maxij, iter, point1, vertexes):
    # print("Replace_Numbers")
    sum = max
    while max != 0:
        for y in range(len(temporary_field)):  # ширина
            for x in range(len(temporary_field) - 1):  # висота
                if y == maxij[0] and x == maxij[1]:
                    print(y+1, "|", x+1, "=", max)# "\t sum", sum)
                    if isinstance(temporary_field[y][x - 1], int) == True and temporary_field[y][x - 1] == max - 1:
                        max -= 1
                        maxij = [y, x - 1]
                        sum += max
                        temporary_field[y][x] = "#"
                        break
                    elif isinstance(temporary_field[y][x + 1], int) == True and temporary_field[y][x + 1] == max - 1:
                        max -= 1
                        maxij = [y, x + 1]
                        sum += max
                        temporary_field[y][x] = "#"
                        break
                    elif isinstance(temporary_field[y - 1][x], int) == True and temporary_field[y - 1][x] == max - 1:
                        max -= 1
                        maxij = [y - 1, x]
                        sum += max
                        temporary_field[y][x] = "#"
                        break
                    elif isinstance(temporary_field[y + 1][x], int) == True and temporary_field[y + 1][x] == max - 1:
                        max -= 1
                        maxij = [y + 1, x]
                        sum += max
                        temporary_field[y][x] = "#"
                        break

    for y in range(len(temporary_field)):  # ширина
        for x in range(len(temporary_field) - 1):  # висота
            if isinstance(temporary_field[y][x], int) == True and temporary_field[y][x] > max:
                temporary_field[y][x] = "_"
            elif isinstance(temporary_field[y][x], int) == True and temporary_field[y][x] == 0:
                temporary_field[y][x] = point1

    print("\tВага шляху:", sum)

    print("\n\t\tІтерація №", iter)
    Print_Field(temporary_field)
    return temporary_field


#####################

Initial_Conditions()
