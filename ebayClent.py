import json
import string 
import os
from os.path import join, dirname 
from os import environ
from flask import Flask, render_template,request 
from flask import flash,redirect,jsonify,url_for
import imageStats as ist
app = Flask(__name__)

@app.route('/')
def index():
  print ("I am in root")
  return render_template('UIobj.html')
  
@app.route('/headCount/', methods=['POST'])
def getHeadCount():
    print ("in Head count")
    if request.method == 'POST':
      image1 = request.files['pic1']
      my_object = request.form['my_object']
      print ("my_object: ", my_object)
      path=os.getcwd()
      staticPath1=path+"/static/"+image1.filename
      print ("staticPath1 :" ,staticPath1)
      image1.save(staticPath1)
      quality = ist.get_stats(staticPath1)
      if (quality=="Bad"):
        return jsonify(success=0,category="warning",error_msg="Bad quality image! Please upload another one")
        #flash(u"Bad quality image! Please upload another one","warning")
        #return redirect('/')
      else:
        import background_removal as br
        outfilepath=br.remove_bg(staticPath1,my_object)
        print (outfilepath)
        filNameToBeSent = url_for('static', filename=outfilepath)
        return jsonify(success=1,output=fileNameToBeSent)
        #return render_template('CountOutput.html',output=outfilepath)
        

#        filePath1=string.replace(staticPath1,"\\","\\")
#        print("filePath1",filePath1)
#        try:
#            with open(filePath1,'rb') as imageFile1:
#                Image1Details=[]
#                Image1Details.append(image1.filename)
#                Image1Details.append("Hi") 
#        except Exception as e:
#            print("Exception : " , e)
            
if __name__ == '__main__':
    app.secret_key='kkhjlqierpioiuqiewuioue87u8973248uiouiosfu89743ui'
    app.run(host='0.0.0.0',port=5001)