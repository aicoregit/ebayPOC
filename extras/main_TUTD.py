# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:48:18 2018

@author: SAimCognitiveSP
"""

from flask import Flask, flash, jsonify,redirect,render_template,request,url_for 

from os.path import join, dirname 
from os import environ 
import ldap_auth as auth
import DB_queries as dbq
import table_withPlotly as tp
import datetime
import calendar
user_Role=""
import pandas as pd
Vertical_Name=""    
    
app = Flask(__name__, static_url_path = "", static_folder = "static")
app.secret_key = 'the_secret_key_is_aws'

@app.route('/')
def index():
  
  return render_template('page1.html')

@app.route('/logIn/', methods=['POST'])
def logIn():
  print ("LoginCheck !!")
  if request.method == 'POST':
      user_id = request.form['email']
      password = request.form['password']
      #print("@@@@ .. ", user_id,password)
      ret_status = auth.check_credentials(user_id,password)
      print ("ret status",ret_status)
      global user_Role
      vert_list,user_Role = dbq.get_UserDetails(user_id)
      print("len(vert_list)  :" ,len(vert_list))
      if((ret_status=='Success') and (len(vert_list) > 0)):
          print("vert_list : ", vert_list)
          return render_template('page2_view.html',vert_list=vert_list)
      elif((ret_status!='Success')):
          print("Authentication Failed!!!")
          flash(u"Authentication Failed.Please try again","warning")
          return redirect('/')
      elif((len(vert_list) == 0)):
          print("You are not authorized to view the portal. Sorry for the inconvenience.")
          flash(u"You are not authorized to view the portal. Sorry for the inconvenience.","danger")
          return redirect('/')

#raghav code starts
@app.route('/account_list')
def select_account():
    verticalname = request.args.get('vertname','NA',type=str)

    if verticalname!='NA':
        accArray = dbq.get_AccountDetails(verticalname)
    
    
    return jsonify(accounts=accArray)

@app.route('/project_list')
def select_project():
    verticalname = request.args.get('vertname','NA',type=str)
    accountID = request.args.get('accountname',0,type=int)
    #print("@@",verticalname,accountname)
    if verticalname!='NA' and accountID !=0:
        prjArray = dbq.get_ProjectDetails(verticalname,accountID)
        print ("prjarray",prjArray)
    
    
    return jsonify(projects=prjArray)


#raghav code ends



@app.route('/selectdate/', methods=['POST','GET'])      
def function_name(): 
    listofmonths=dbq.get_monthlist() 
#    current_year=datetime.datetime.now().year
#    current_month=datetime.datetime.now().month
    return render_template('page3.html',listofmonths=listofmonths)

@app.route('/selectdate/give_historical_vsforecast/', methods=['POST'])      
def give_historical_vsforecast(): 
    dateRange= request.form['dateRange']
    pred_df, act_df =dbq.create_prediction_month_list(Vertical_Name,dateRange)
    monthlist = act_df['month'].tolist()
    new_month_list=[]
    
    for item in monthlist:
        new_month=calendar.month_abbr[int(item.split("-")[1])]+"-" + str(item.split("-")[0])[2:4] 
        new_month_list.append(new_month)
    print("@@@@@@@@@",new_month_list)
    
    selected_pred_df=pred_df.loc[pred_df['month'].isin(new_month_list)] 
    
#    print("@@@@@@@@@",monthlist)
#    print (selected_pred_df)
#    print("@@@@@@@@@@@@@")
#    print(act_df)
#    print("************")
#    selected_pred_df.to_csv("pred.csv")
#    act_df.to_csv("hist.csv")

    cum_plotLink, hist_png = tp.createcumulative_plot(selected_pred_df, act_df,Vertical_Name,dateRange)
    table_plotLink,hist_csv = tp.createHist_table(selected_pred_df, act_df,Vertical_Name,dateRange)
    selected_pred_df.to_csv("selected_pred.csv")
    
    print(cum_plotLink)
    cum_plotLink = cum_plotLink+".embed"
    table_plotLink = table_plotLink+".embed"
    print("TABLE : " , table_plotLink)
    hist_png = hist_png.split("/")[2]
    hist_csv = hist_csv.split("/")[2]
    return render_template('page4.html',cum_plotLink=cum_plotLink, hist_png = hist_png, table_plotLink=table_plotLink,hist_csv = hist_csv)


@app.route('/logIn/Dashboard/', methods=['GET'])      
def give_Vertical_predictions1():
    global Vertical_Name
    #Vertical_Name= request.form['verticalname']
    
    print(Vertical_Name)
    print("!@!@#!#$!!," ,user_Role)
    return_predict=dbq.get_VerticalPredictions(Vertical_Name)
 
    if((len(return_predict) >0) and user_Role== "Consultant"):
        print(return_predict.head(3))
        #htmlOutput=Vertical_Name+"_forecast.html" 
        tableLink,csvPath = tp.create_prediction_table(return_predict[0:12],Vertical_Name)
        csvPath = csvPath.split("/")[2]
        graphLink,imageLink = tp.create_plotly_graphs(return_predict[0:12],Vertical_Name)
        imageLink = imageLink.split("/")[2]
        tableLink=tableLink+".embed"
        graphLink=graphLink+".embed"
        print("ALL LINKS CREATED >>>> ",tableLink,graphLink)
        return render_template('page2_next.html',tableLink= tableLink,graphLink=graphLink,imageLink=imageLink,csvPath=csvPath)
    elif((len(return_predict) >0) and user_Role== "Admin"):
        tableLink,csvPath = tp.create_prediction_table(return_predict[0:12],Vertical_Name)
        csvPath = csvPath.split("/")[2]
        graphLink,imageLink = tp.create_plotly_graphs(return_predict[0:12],Vertical_Name)
        imageLink = imageLink.split("/")[2]
        tableLink=tableLink+".embed"
        graphLink=graphLink+".embed"
        print("ALL LINKS CREATED >>>> ",tableLink,graphLink)
        return render_template('pag2_next_admin.html',tableLink= tableLink,graphLink=graphLink,imageLink=imageLink,csvPath=csvPath)

        
        
    else:
        return render_template('error_NodataInDB.html')


     
        
@app.route('/logIn/give_Vertical_predictions/', methods=['POST'])      
def give_Vertical_predictions():
    global Vertical_Name
    Vertical_Name= request.form['verticalname']
    print(Vertical_Name)
    print("!@!@#!#$!!," ,user_Role)
    return_predict=dbq.get_VerticalPredictions(Vertical_Name)
 
    if((len(return_predict) >0) and user_Role== "Consultant"):
        print(return_predict.head(3))
        #htmlOutput=Vertical_Name+"_forecast.html" 
        tableLink,csvPath = tp.create_prediction_table(return_predict[0:12],Vertical_Name)
        csvPath = csvPath.split("/")[2]
        graphLink,imageLink = tp.create_plotly_graphs(return_predict[0:12],Vertical_Name)
        imageLink = imageLink.split("/")[2]
        tableLink=tableLink+".embed"
        graphLink=graphLink+".embed"
        print("ALL LINKS CREATED >>>> ",tableLink,graphLink)
        
        return render_template('page2_next.html',tableLink= tableLink,graphLink=graphLink,imageLink=imageLink,csvPath=csvPath)
    elif((len(return_predict) >0) and user_Role== "Admin"):
        tableLink,csvPath = tp.create_prediction_table(return_predict[0:12],Vertical_Name)
        csvPath = csvPath.split("/")[2]
        graphLink,imageLink = tp.create_plotly_graphs(return_predict[0:12],Vertical_Name)
        imageLink = imageLink.split("/")[2]
        tableLink=tableLink+".embed"
        graphLink=graphLink+".embed"
        print("ALL LINKS CREATED >>>> ",tableLink,graphLink)
        return render_template('pag2_next_admin.html',tableLink= tableLink,graphLink=graphLink,imageLink=imageLink,csvPath=csvPath)

        
        
    else:
        return render_template('error_NodataInDB.html')




if __name__ == '__main__':
  app.run(debug=True)