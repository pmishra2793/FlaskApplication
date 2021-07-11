from os import EX_CANTCREAT
from flask import Flask, render_template, request
from flask.wrappers import Response
app = Flask(__name__)

'''
NOTE
1. If user select a file which are not present in the list then it will take file1 as default.
2. If start_line_number > end_line_numer, then it will display all the lines
3. please used this url: http://localhost:5000?fileName=file1&start_line_number=10&end_line_number=30
'''

@app.route('/', methods=['GET'])
def read_files():
    try:
        if request.method=='GET':
            file_name_list = ['file1', 'file2', 'file3', 'file4']
            start_line_number = request.args.get('start_line_number')
            end_line_numer = request.args.get('end_line_number')
            file_name = request.args.get('fileName')
            print('file_name = ',file_name)
            if file_name == None or file_name not in file_name_list:
                file_name = 'file1'
            else:
                file_name = file_name  
            if file_name == 'file2' or file_name == 'file4':
                file_encoding = 'utf16' 
            else:
                file_encoding = 'utf8' 
            file_path = './static/'+str(file_name)+'.txt'
            file = open(file_path, encoding=file_encoding)
            content = file.readlines()
            if start_line_number is not None and end_line_numer is not  None:
                if start_line_number <= end_line_numer:
                    content = content[int(start_line_number):int(end_line_numer)]
            if start_line_number is not None and end_line_numer == None:   
                content = content[int(start_line_number):]                   
            if start_line_number == None and end_line_numer is not None:
                content = content[:int(end_line_numer)] 
            file.close()    
            return render_template('index.html', details = content, filename = file_name)
    except Exception as e:
        return Response({'Error : '+str(e)})

@app.errorhandler(404)
def page_not_found(e):
    title = 'Opps. Page Not Found (404)'
    para = 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again'
    return render_template("error.html", title=title, para = para), 404   

@app.errorhandler(403)
def page_not_found(e):
    title = 'You dont have permission to do that (403)'
    para = 'Please check your account and try again'
    return render_template("error.html", title=title, para = para), 403   

@app.errorhandler(500)
def page_not_found(e):
    title = 'Something went wrong (500)'
    para = 'We are experiencing some trouble on our end. Please try again in the near future'
    return render_template("error.html", title=title, para = para), 500       

@app.errorhandler(405)
def page_not_found(e):
    title = 'Method Not Allowed (405)'
    para = 'The method is not allowed for the requested URL'
    return render_template("error.html", title=title, para = para), 405   

if __name__ == '__main__':
    app.run(debug=True)
   