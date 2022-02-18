#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// N is the size of the 2D matrix N*N
#define N 9

/* A utility function to print grid */
void print(int arr[N][N])
{
    for (int i=0; i<N; i++) {
		for (int j=0; j<N; j++)
			printf("%d\t", arr[i][j]+1);
		printf("\n");
	}
}

// Checks whether it will be legal
// to assign num to the
// given row, col
int isSafe(int grid[N][N], int row,
					int col, int num)
{
	
	// Check if we find the same num
	// in the similar row , we return 0
	for (int x = 0; x <= 8; x++)
		if (grid[row][x] == num)
			return 0;

	// Check if we find the same num in the
	// similar column , we return 0
	for (int x = 0; x <= 8; x++)
		if (grid[x][col] == num)
			return 0;

	// Check if we find the same num in the
	// particular 3*3 matrix, we return 0
	int startRow = row - row % 3,
				startCol = col - col % 3;

    int z = 3;

	for (int i = 0; i < z; i++)
		for (int j = 0; j < z; j++)
			if (grid[i + startRow][j +
						startCol] == num)
				return 0;

	return 1;
}

/* Takes a partially filled-in grid and attempts
to assign values to all unassigned locations in
such a way to meet the requirements for
Sudoku solution (non-duplication across rows,
columns, and boxes) */
int solveSudoku(int grid[N][N], int row, int col)
{
	
	// Check if we have reached the 8th row
	// and 9th column (0
	// indexed matrix) , we are
	// returning true to avoid
	// further backtracking
	if (row == N - 1 && col == N)
		return 1;

	// Check if column value becomes 9 ,
	// we move to next row and
	// column start from 0
	if (col == N)
	{
		row++;
		col = 0;
	}

	// Check if the current position
	// of the grid already contains
	// value >0, we iterate for next column
	if (grid[row][col] > 0)
		return solveSudoku(grid, row, col + 1);

	for (int num = 1; num <= N; num++)
	{
		
		// Check if it is safe to place
		// the num (1-9) in the
		// given row ,col ->we move to next column
		if (isSafe(grid, row, col, num)==1)
		{
			/* assigning the num in the
			current (row,col)
			position of the grid
			and assuming our assigned num
			in the position
			is correct	 */
			grid[row][col] = num;
		
			// Checking for next possibility with next
			// column
			if (solveSudoku(grid, row, col + 1)==1)
				return 1;
		}
	
		// Removing the assigned num ,
		// since our assumption
		// was wrong , and we go for next
		// assumption with
		// diff num value
		grid[row][col] = 0;
	}
	return 0;
}

///----------------------------------------------

void read_grid_from_file(int size, char *ip_file, int grid[9][9]) {
	FILE *fp;
	int i, j;
	fp = fopen(ip_file, "r");
	for (i=0; i<size; i++) {
		for (j=0; j<size; j++) {
			fscanf(fp, "%d", &grid[i][j]);
		}
	}
} 

void solve(int grid[9][9]){
    if (solveSudoku(grid, 0, 0)==1)
		print(grid);
	else
		printf("No solution exists");
}

int main(int argc, char *argv[]) {
	int grid[9][9], size, i, j;
	
	if (argc != 3) {
		printf("Usage: ./sudoku.out grid_size inputfile");
		exit(-1);
	}
	
	size = atoi(argv[1]);
	read_grid_from_file(size, argv[2], grid);
	
	/* Do your thing here */

	solve(grid);
	
	/* The segment below prints the grid in a standard format. Do not change */
	// for (i=0; i<size; i++) {
	// 	for (j=0; j<size; j++)
	// 		printf("%d\t", grid[i][j]+100);
	// 	printf("\n");
	// }
	
	
}
