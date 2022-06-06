from classes import Cell, LineInfo
from tkinter import messagebox

all_cells = Cell.all
all_lines = LineInfo.all


def group_unknown(line):
    if line.axis == 'column':
        coordinate = 'y'
    else:  # line.axis == 'row'
        coordinate = 'x'

    groups = []
    current = []
    for unknown in line.unknown_cells:
        if not current:
            current.append(unknown)
        else:
            pos = getattr(current[-1], coordinate)
            if getattr(unknown, coordinate) == pos + 1:
                current.append(unknown)
            else:
                groups.append(current)
                current = [unknown]
    groups.append(current)

    space = 0
    for group in groups:
        if not len(group) % 2:
            space += len(group) / 2
        else:
            space += len(group) // 2 + 1

    return groups, space


def resolve_groups(line):
    groups, space = group_unknown(line)

    if line.value == space:
        for group in groups:
            if not len(group) % 2:
                for cell in group:
                    for loc in cell.parallel_cells(line.axis):
                        loc.change_to_grass()
            else:
                for cell in group[::2]:
                    cell.change_to_tent()
    elif line.value == space - 1:
        for num, group in enumerate(groups):
            if (len(group) in [1, 3]
                    and num + 1 != len(groups)
                    and len(groups[num + 1]) in [1, 3]
                    and group[-1].count_intermediate(line.axis, groups[num + 1][0]) == 1):
                for cell in group[-1].next_cell(line.axis).parallel_cells(line.axis):
                    cell.change_to_grass()


def solve(event):
    for cell in all_cells:
        if len([loc for loc in cell.perpendicular_cells if loc.content == 'tree']) == 0:
            cell.change_to_grass()

    for line in all_lines:
        if line.value == 0:
            for cell in line.line_cells:
                cell.change_to_grass()
        resolve_groups(line)

    all_tents = [cell for cell in all_cells if cell.content == 'tent']
    for tent in all_tents:
        if tent.count_perpendicular('tree') == 1:
            tent.content = 'tent-c'
            for cell in tent.perpendicular_cells:
                if cell.content == 'tree':
                    cell.content = 'tree-c'

    all_trees = [cell for cell in all_cells if cell.content == 'tree']
    for tree in all_trees:
        if (tree.count_perpendicular(None) == 0) & (tree.count_perpendicular('tent') == 1):
            tree.content = 'tree-c'
            for cell in tree.perpendicular_cells:
                if cell.content == 'tent':
                    cell.content = 'tent-c'
        elif (tree.count_perpendicular(None) == 1) & (tree.count_perpendicular('tent') == 0):
            for cell in tree.perpendicular_cells:
                cell.change_to_tent()
        elif tree.count_perpendicular(None) == 2:
            for quadrant in tree.surrounding_quadrants:
                if quadrant[0].content is None and quadrant[2].content is None:
                    quadrant[1].change_to_grass()

    if Cell.cell_count == 0:
        messagebox.showinfo(title='We are done here', message='Puzzle solved!')
