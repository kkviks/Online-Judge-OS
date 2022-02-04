from http.server import executable
from subprocess import Popen, PIPE, call
import timeit
import os
import errno
import pexpect, sys

flags = "g++"
tests_dir = 'test_cases'

FILE_PASSED = 'tcs_passed'
FILE_FAILED = 'tc_failed'


def readFileToString(filepath):
    with open(filepath, 'r') as file:
        data = file.read()#.replace('\n', '')
        return data


def runTestCase(filepath, inputPath, outputPath):
    input = readFileToString(inputPath)
    output = readFileToString(outputPath)

    print("Test case input: ", input)
    print("Test case desired output: ", output)
    

    #Sending STDIN to file and getting STDOUT
    executablePath = './a.out'
    p = Popen(executablePath,stdin=PIPE, stdout = PIPE)
    inp, out = p.stdin, p.stdout

    inp.write( bytes(input, encoding='utf-8'))
    student_output = out.read().decode()

    inp.close()
    out.close()

    print("Student Out: ", student_output)
    return True


    # p = pexpect.spawn(executablePath, encoding='utf-8')
    # p.send(input)

    # child = pexpect.spawn(executablePath)
    # child.send(input)
    # child.logfile_read = sys.stdout.buffer
    # index = child.expect_exact([output, pexpect.EOF, pexpect.TIMEOUT])
    # child.close()

    # if index==0:
    #     print('Matched!')
    # elif pexpect.EOF or pexpect.TIMEOUT:
    #     print('Pexpect exception')

    # isMatch = False

    # try:
    #     index = p.expect_exact([output,pexpect.EOF,pexpect.TIMEOUT], timeout=10000)
    #     if index == 0:
    #         #isMatch = True
    #         return True
    # except pexpect.EOF or pexpect.TIMEOUT:
    #     print('Error from sending/reading input/output from our side .... ')
    #     isMatch = False

    # #Comparing STDOUT with correct answer
    # print("p.after: ",p.after)
    return True

def runTestCases(filepath):

    for test_case in os.listdir(tests_dir):
        inputPath = tests_dir + '/' + test_case+'/input.txt'
        outputPath = tests_dir + '/' + test_case+'/output.txt'

        isTestPassed = runTestCase(filepath, inputPath,outputPath)

        if isTestPassed:
            print(filepath+' passed test ' + test_case + ' succesfully ✓')
        else:
            print(filepath+' failed test ' + test_case + ' succesfully ✗')
            return FILE_FAILED

    print('\n'+filepath + ' passed ALL test cases successfully ✓')

    return FILE_PASSED

def run_helper(parentPath, filepath):

    print("Running test cases on " + filepath)

    status = runTestCases(filepath)

    # p.stdin.close()
    #p.wait()

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

 
