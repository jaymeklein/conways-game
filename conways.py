import copy

def dies(x: int, y: int, matrix: list[list[int]]) -> bool:
  neighbours = count_neighbours(x, y, matrix)
  return neighbours < 2 or neighbours > 3

def lives(x: int, y: int, matrix: list[list[int]]) -> bool:
  return count_neighbours(x, y, matrix) in [2, 3]

def new_cell(x: int, y: int, matrix: list[list[int]]) -> bool:
  return count_neighbours(x, y, matrix) == 3

def count_neighbours(x: int, y: int, matrix: list[list[int]]) -> int:
  positions = [
      (x-1, y-1),
      (x-1, y),
      (x-1, y+1),
      (x, y-1),
      (x, y+1),
      (x+1, y-1),
      (x+1, y),
      (x+1, y+1)
  ]

  total = 0
  for position_x, position_y in positions:
    minor = position_x < 0 or position_y < 0
    no_index = position_x+1> len(matrix) or position_y+1 > len(matrix[position_x])

    if minor or no_index:
      continue

    if matrix[position_x] and matrix[position_x][position_y]:
      total += 1
      continue

  return total

def run_cells(matrix: list[list[int]]) -> list[list[int]]:
  validation_copy = copy.deepcopy(matrix)
  for row, row_elements in enumerate(validation_copy):
    for column, has_element in enumerate(row_elements):

      if dies(row, column, validation_copy) and has_element:
        matrix[row][column] = 0
        continue

      elif new_cell(row, column, validation_copy) and not has_element:
        matrix[row][column] = 1
        continue

  return matrix

def generate_empty_values(matrix: list[list[int]]) -> list[list[int]]:
  row_length = len(matrix[0]) + 2
  new_matrix = []
  if any(matrix[0]):
    new_matrix.append([0 for _ in range(row_length)])

  for row in matrix:
    new_matrix.append([0] + row + [0])
  
  if any(matrix[-1]):
    new_matrix.append([0 for _ in range(row_length)])

  return new_matrix

def remove_empty_values(matrix: list[list[int]]) -> list[list[int]]:
  result = []
  for row, elements in enumerate(matrix):
    if 1 not in elements and row in [0, len(matrix)-1]:
      continue

    result.append(elements)

  first_col_empty = not any([c[0] == 1 for c in result])
  last_col_empty = not any([c[-1] == 1 for c in result])

  for row, elements in enumerate(result):
    if first_col_empty:
      result[row] = result[row][1:]
    
    if last_col_empty:
      result[row] = result[row][:-1]
  
  if not any(matrix[0]) or not any(matrix[-1]):
    return remove_empty_values(result)

  return result

def get_generation(cells : list[list[int]], generations : int) -> list[list[int]]:
  for gen in range(generations):
    cells = generate_empty_values(cells)
    cells = run_cells(cells)
    cells = remove_empty_values(cells)

  return cells


def print_matrix(matrix, squares = True) -> None:
  result = ''
  for row in matrix:
    for value in row:
      if value == 1 and squares:
        result+= '■'
        continue

      elif value == 0 and squares:
        result+= '□'
        continue
      
      result += str(value)
    
    result += '\n'
  print(result)

if __name__ == '__main__':
  input = [
            [1,1,1,0,0,0,1,0],
            [1,0,0,0,0,0,0,1],
            [0,1,0,0,0,1,1,1]
        ]

  # Resulting 2D Matrix after 16 generations
  print_matrix(get_generation(input, 16)) 


