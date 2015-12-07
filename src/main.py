import format

filenameIn = '../test_sample/codeE7.c'     #input testSample
filenameOut1 = "../output/output.c"        #output formatted codes
filenameOut2 = "../output/outputInfo.txt"  #output grammer analysis result
format.format(filenameIn, filenameOut1, filenameOut2)

filenameIn = '../output/output.c'                   #input testSample
filenameOut = "../output/outputSimplified.c"        #output simplified codes
format.simplify(filenameIn, filenameOut)

filenameIn = '../output/output.c'                   #input testSample
filenameOut = "../output/outputStyle1.c"            #output style1 codes
format.style1(filenameIn, filenameOut)

filenameIn = '../output/output.c'                   #input testSample
filenameOut = "../output/outputStyle2.c"            #output style2 codes
format.style2(filenameIn, filenameOut)