from tkinter import Button
import settings


class Cell:
    all = []
    cell_count = settings.CELL_COUNT

    def __init__(self, x, y):
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self.content = None

        Cell.all.append(self)

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    def left_click_actions(self, event):
        self.cell_btn_object.configure(text='T', fg='brown', bg='green')
        if self.content is None:
            Cell.cell_count -= 1
        self.content = 'tree'

    def right_click_actions(self, event):
        self.cell_btn_object.configure(text='', bg='SystemButtonFace')
        if self.content is not None:
            Cell.cell_count += 1
        self.content = None

    def change_to_grass(self):
        if self.content is None:
            self.cell_btn_object.configure(bg='light green')
            self.content = 'grass'
            Cell.cell_count -= 1

    def change_to_tent(self):
        if self.content is None:
            self.cell_btn_object.configure(text='\u0394', fg='red', bg='light green')
            self.content = 'tent'
            Cell.cell_count -= 1
            LineInfo.update_values(self.x, self.y)
            for cell in self.surrounding_cells:
                cell.change_to_grass()

    @staticmethod
    def get_cell_by_axis(x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    def surrounding_positions(self):
        positions = [
            Cell.get_cell_by_axis(self.x, self.y + 1),
            Cell.get_cell_by_axis(self.x + 1, self.y + 1),
            Cell.get_cell_by_axis(self.x + 1, self.y),
            Cell.get_cell_by_axis(self.x + 1, self.y - 1),
            Cell.get_cell_by_axis(self.x, self.y - 1),
            Cell.get_cell_by_axis(self.x - 1, self.y - 1),
            Cell.get_cell_by_axis(self.x - 1, self.y),
            Cell.get_cell_by_axis(self.x - 1, self.y + 1)
        ]
        return positions

    @property
    def surrounding_cells(self):
        cells = [cell for cell in self.surrounding_positions() if cell is not None]
        return cells

    @property
    def surrounding_quadrants(self):
        positions = self.surrounding_positions()
        quadrants = [
            positions[:3],
            positions[2:5],
            positions[4:7],
            positions[6:] + positions[:1]
        ]
        quadrants = [quadrant for quadrant in quadrants if all(quadrant)]

        return quadrants

    @property
    def perpendicular_cells(self):
        cells = [cell for cell in self.surrounding_cells
                 if self.x == cell.x or self.y == cell.y]
        return cells

    def count_perpendicular(self, content):
        return len([cell for cell in self.perpendicular_cells if cell.content == content])

    def parallel_cells(self, axis):
        if axis == 'column':
            cells = [cell for cell in self.perpendicular_cells
                     if self.y == cell.y]
        else:  # axis == 'row':
            cells = [cell for cell in self.perpendicular_cells
                     if self.x == cell.x]
        return cells

    def next_cell(self, axis):
        if axis == 'column':
            cell = Cell.get_cell_by_axis(self.x, self.y + 1)
        else:  # axis == 'row':
            cell = Cell.get_cell_by_axis(self.x + 1, self.y)
        return cell

    def count_intermediate(self, axis, cell):
        if axis == 'column':
            distance = cell.y - self.y
        else:  # axis == 'row':
            distance = cell.x - self.x
        return distance - 1


class LineInfo:
    all = []

    def __init__(self, axis, position):
        self.line_btn_object = None
        self.axis = axis
        self.position = position
        self.value = None

        LineInfo.all.append(self)

    def __repr__(self):
        return f"Line({self.axis}: {self.position})"

    def create_btn_object(self, location):
        btn = Button(
            location,
            bg='gray',
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.line_btn_object = btn

    @staticmethod
    def get_line_info(axis, position):
        for info in LineInfo.all:
            if info.axis == axis and info.position == position:
                return info

    @staticmethod
    def update_values(x, y):
        column = LineInfo.get_line_info('column', x)
        row = LineInfo.get_line_info('row', y)
        if column.value is not None:
            column.value -= 1
        if row.value is not None:
            row.value -= 1

    def left_click_actions(self, event):
        if self.value is None:
            self.value = -1
        if self.value < settings.GRID_SIZE:
            self.value += 1
        self.line_btn_object.configure(text=self.value)

    def right_click_actions(self, event):
        self.value = None
        self.line_btn_object.configure(text='')

    @property
    def line_cells(self):
        if self.axis == 'column':
            return [cell for cell in Cell.all if cell.x == self.position]
        else:  # line.axis == 'row'
            return [cell for cell in Cell.all if cell.y == self.position]

    @property
    def unknown_cells(self):
        return [cell for cell in self.line_cells if cell.content is None]
