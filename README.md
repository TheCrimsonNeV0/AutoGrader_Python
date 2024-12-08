# AutoGrader_Python
Auto grading tool for C files written in Python. The tool runs every .c file in the submissions folder and provides the arguments and the inputs in the code. The tool compares the output with the expected output and outputs a .csv file containing the matching information. Also, the tool writes all of the outputs to a text file.

## Operation Steps
1 - The tool creates the .csv and the .txt file
2 - Each code is compiled and compilation errors are reported
3 - Codes are executed with the provided arguments
4 - Checks if the code outputs the expected output and flushes the result. If the execution takes londer than 5 seconds, the system outputs a timeout message
5 - After the completion, .o binary files are removed from the system
