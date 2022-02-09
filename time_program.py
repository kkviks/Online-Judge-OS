from http.server import executable
from subprocess import Popen, PIPE, call
import timeit
import os
import platform

flags = "g++"
tests_dir = 'test_cases'

FILE_PASSED = 'tcs_passed'
FILE_FAILED = 'tc_failed'


def readFileToString(filepath):
    with open(filepath, 'r') as file:
        data = file.read()  # .replace('\n', '')
        return data


def isCorrect(c_output, answer):
    n = len(c_output)

    if len(answer) != n:
        return False

    for i in range(n):
        if c_output[i] != answer[i]:
            return False

    return True


def runTestCase(filepath, input_path, outputPath):

    c_input = readFileToString(input_path)
    answer = readFileToString(outputPath)
    answer = answer.split()

    #print("Test case input: ", c_input)
    #print("Test case desired output: ", answer)

    # Sending STDIN to file and getting STDOUT
    platf = platform.system()
    if platf == "Windows":
        cmd = "a.exe"
    elif platf == "Linux" or platf == "Darwin":
        cmd = "./a.out"
    else:
        print("Unidentified System")
        return False

    tic = timeit.default_timer()
    p = Popen([cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True).communicate(c_input.encode('utf-8'))
    toc = timeit.default_timer()

    global t
    t = toc - tic

    c_output = p[0].decode('utf-8')
    c_output = c_output.split()

    res = isCorrect(c_output, answer)

    #print("Student Out: ", c_output)
    #print("\nAnswer : ", answer)
    #print("\nMatch = ", res)
    return res


def runTestCases(filepath):
    for test_case in os.listdir(tests_dir):
        input_path = tests_dir + '/' + test_case + '/input.txt'
        output_path = tests_dir + '/' + test_case + '/output.txt'

        is_test_passed = runTestCase(filepath, input_path, output_path)

        group = filepath.split('/')[1]

        if is_test_passed:
            print(group + ' passed test ' + test_case + ' succesfully ✓')
        else:
            print(group + ' failed test ' + test_case + ' succesfully ✗')
            return FILE_FAILED

    print(group + ' passed ALL test cases successfully ✓')

    return FILE_PASSED


def run_helper(parentPath, filepath):
    status = runTestCases(filepath)
    return status


def run(parentPath, filepath):
    # Compile the C file using flags
    print('\nCompiling: ' + filepath)
    call([flags, filepath])  # Need to check for compilation error

    status = run_helper(parentPath, filepath)
    return status, t
