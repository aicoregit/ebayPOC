import json
import string 
import os
from os.path import join, dirname 
from os import environ
from flask import Flask, flash, redirect, render_template,request 

app = Flask(__name__)

@app.route('/')
def index():
  print ("I am in root")
  return render_template('faceMain.html')

@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    
  
@app.route('/headCount/', methods=['POST'])
def getHeadCount():
    print ("in Head count")
    # a=1
    # if (a==1):
        # flash(u"Authentication Failed.Please try again","warning")
        # return redirect('/')
    
    if request.method == 'POST':
        image1 = request.files['pic1']
        path=os.getcwd()
        staticPath1=path+"/static/"+image1.filename
        print ("staticPath1 :" ,staticPath1)
        image1.save(staticPath1)
        import darknettest
        darknettest.darktest(staticPath1)
        #filePath1=string.replace(staticPath1,"\\","\\") 
	#	print("filePath1",filePath1)
        #try:
        #    with open(filePath1,'rb') as imageFile1:
         #       Image1Details=[]
         #       Image1Details.append(image1.filename)
         #       Image1Details.append("Hi")
        return render_template('CountOutput.html',output=Image1Details) 
        #except Exception as e:
            #print("Exception : " , e)
            
if __name__ == '__main__':
    app.secret_key='kkhjlqierpioiuqiewuioue87u8973248uiouiosfu89743ui'
    app.run(host='0.0.0.0')