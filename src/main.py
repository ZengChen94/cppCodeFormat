import format

filenameIn = '../test_sample/codeE7.c'     #imput testSample
filenameOut1 = "../output/output.c"        #output formatted codes
filenameOut2 = "../output/outputInfo.txt"  #output grammer analysis result
format.format(filenameIn, filenameOut1, filenameOut2)