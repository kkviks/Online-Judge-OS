from http.server import executable
from subprocess import Popen, PIPE, call
import timeit
import os
import errno

flags = "gcc"
tests_dir = 'test_cases'

FILE_PASSED = 'tcs_passed'
FILE_FAILED = 'tc_failed'


def readFileToString(filepath):
    with open(filepath, 'r') as file:
        data = file.read()#.replace('\n', '')
        return data


def work():
    #result = subprocess.call("./a.out") 
    p = Popen(["./a.out"],stdin=PIPE, stdout=PIPE, stderr=PIPE)

    #### Reading and running input test case
    test_case = readFileToString('test_case.txt')
    test_case_bytes = bytes(test_case, 'utf-8')
    student_output, err = p.communicate(test_case_bytes)
    student_output_str = student_output.decode("utf-8") 

    #### Checking correctness
    #print(student_output_str)
    test_case_ans = readFileToString('desired_output.txt')
    print(bytes(student_output_str, 'utf-8'))
    print("---output---\n")
    print(bytes(test_case_ans, 'utf-8'))

    print("Sudukos: \n")
    print(student_output_str)
    print("----")
    print(test_case_ans)

    if(test_case_ans is student_output_str):
        print("Matched!")
    else:
        print("Wrong answer!")
    return

def runTestCase(p, inputPath, outputPath):
    input = readFileToString(inputPath)
    output = readFileToString(outputPath)

    #Sending STDIN to file and getting STDOUT
    stdInput = bytes(input, 'utf-8')
    #stdOutInbytes, err = p.communicate(stdInput)[0] --- can only read once
    stdOutInbytes = p.stdin.write(stdInput)
    #stdOutput = stdOutInbytes.decode('utf-8')
    #print(stdOutInbytes)

    #Comparing STDOUT with correct answer

    return True

def runTestCases(p, filepath):

    for test_case in os.listdir(tests_dir):
        inputPath = tests_dir + '/' + test_case+'/input.txt'
        outputPath = tests_dir + '/' + test_case+'/output.txt'

        isTestPassed = runTestCase(p,inputPath,outputPath)

        if isTestPassed:
            print(filepath+' passed test ' + test_case + ' succesfully ✓')
        else:
            print(filepath+' failed test ' + test_case + ' succesfully ✗')
            return FILE_FAILED

    print('\n'+filepath + ' passed ALL test cases successfully ✓')

    return FILE_PASSED

def run_helper(parentPath, filepath):

    print("Running test cases on " + filepath)

    #executablePath = parentPath + './a.out'
    executablePath = './a.out'
    p = Popen([executablePath],stdin=PIPE,stdout=PIPE, stderr = PIPE)

    status = runTestCases(p, filepath)

    p.stdin.close()
    p.wait()

    return status

def run(parentPath, filepath):
    #Compile the C file using flags
    print('\nCompiling: '+filepath)
    call([flags, filepath])

    tic = timeit.default_timer()
    status = run_helper(parentPath, filepath)
    toc = timeit.default_timer()

    t = toc-tic
    return status, t

 
