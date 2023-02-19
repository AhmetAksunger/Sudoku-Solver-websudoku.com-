import numpy as np

#---------------Take Data from Website and create a sudoku grid--------
from bs4 import BeautifulSoup
import requests
import re
#Sudoku Website
url = 'https://www.websudoku.com/'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
frame_url = soup.find('frame')['src']

response = requests.get(frame_url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

puzzle_grids = soup.find_all('td', {'class': True})
input_list = []
for td in puzzle_grids:

    input_element = td.find_all('input')
    input_list.append(input_element)

temp_list = []

for i in range(len(input_list)):
    if "value" in str(input_list[i][0]):
        index = str(input_list[i][0]).find("value")
        value = str(input_list[i][0])[index + 7]
        temp_list.append(int(value))
    else:
        temp_list.append(0)

sudoku_grid = []
for i in range(0,len(temp_list),9):
    sudoku_grid.append(temp_list[i:i+9])
grid = sudoku_grid
#--------------------------------------------------------
def print_sudoku_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

#--------------------------------------------------------
print("\033[91m" + "SUDOKU BOARD" + "\033[0m")
print_sudoku_board(grid)
possible_list = []
def possible(row,column,number):
    #Does the number appear in the row?
    for i in range(0,9):
        if grid[row][i] == number:
            return False

    #Does the number appear in the column?
    for i in range(0,9):
        if grid[i][column] == number:
            return False

    #Does the number appear in the square?
    
    #if index//3 = 0 that means they are at 0th triple
    #if index//3 = 1 that means they are at 1st triple
    #if index//3 = 2 that means they are at 2nd triple
    a = (row//3) * 3
    b = (column//3) * 3
    square = set()
    for i in range(0,3):
        for j in range(0,3):
            square.add(grid[a+j][b+i])

    if number in square:
        return False

    return True


def possible_list(row,column):
    for i in range(0,9):
        if possible(row,column,i):
            possible_list.append(i)

def solve():

    for row in range(0,9):
        for column in range(0,9):
            if grid[row][column] == 0:
                for num in range(1,10):
                    if possible(row,column,num):
                        grid[row][column] = num
                        solve()
                        grid[row][column] = 0
                    
                return
    print("\033[93m" + "*********************" + "\033[0m")
    print("\033[92m" + "SUDOKU BOARD [SOLVED]" + "\033[0m")                    
    print_sudoku_board(grid)

solve()