import tornado.ioloop as ioloop
import tornado.web as web
import os
import format

path = os.getcwd()
parent_path = os.path.dirname(path)
test_sample_path = parent_path +  "\\test_sample"
test_output_path = parent_path +  "\\output"
##TODO
#不跳转，只处理
#实时更新

class MainHandler(web.RequestHandler):
    def get(self):
        self.render('./index.html')

class CodeHandler(web.RequestHandler):
    def post(self):
        fileName = self.request.body
        print(fileName)
        global test_sample_path
        global test_output_path
        fileName = fileName.decode()
        filename = test_sample_path + '\\' + fileName
        fileReadObj = open(filename)
        returnString = ''
        for fileString in fileReadObj.readlines():
            returnString = returnString + fileString
        self.write(returnString)

class FormatHandler(web.RequestHandler):
    def post(self):
        fileName = self.request.body
        print(fileName)
        global test_sample_path
        global test_output_path
        fileName = fileName.decode()
        filenameIn = test_sample_path + '\\' + fileName
        filenameOut1 = test_output_path + '\\output.c'
        filenameOut2 = test_output_path + '\\outputInfo.txt'
        format.format(filenameIn, filenameOut1, filenameOut2)
        fileReadObj = open(filenameOut1)
        returnString = ''
        for fileString in fileReadObj.readlines():
            returnString = returnString + fileString
        self.write(returnString)

class SimplifyHandler(web.RequestHandler):
    def post(self):
        fileName = self.request.body
        print(fileName)
        global test_sample_path
        global test_output_path
        fileName = fileName.decode()
        filenameIn = test_sample_path + '\\' + fileName
        filenameOut = test_output_path + '\\outputSimplified.c'
        format.simplify(filenameIn, filenameOut)
        fileReadObj = open(filenameOut)
        returnString = ''
        for fileString in fileReadObj.readlines():
            returnString = returnString + fileString
        self.write(returnString)

class StyleHandler(web.RequestHandler):
    def post(self):
        fileName = self.request.body
        print(fileName)
        global test_sample_path
        global test_output_path
        fileName = fileName.decode()
        filenameIn = test_sample_path + '\\' + fileName
        filenameOut = test_output_path + '\\outputStyle1.c'
        format.style(filenameIn, filenameOut)
        fileReadObj = open(filenameOut)
        returnString = ''
        for fileString in fileReadObj.readlines():
            returnString = returnString + fileString
        self.write(returnString)

def make_app():
    return web.Application(
        handlers=[
            (r"/", MainHandler),
            (r'/code', CodeHandler),
            (r'/format', FormatHandler),
            (r'/simplify', SimplifyHandler),
            (r'/style', StyleHandler),
        ],
        default_host='', transforms=None,
        template_path=os.path.join(os.path.dirname(__file__), "web"),
        static_path=os.path.join(os.path.dirname(__file__), "web/static"),
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8800)
    ioloop.IOLoop.current().start()
