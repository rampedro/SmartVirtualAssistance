#var ibmdb = require('ibm_db');
import ibm_db
import sys
import urllib.request, json 
import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
        

def main(dict):
    max = 0
    min = 0
#Getting connected to db2 Databse

    dsn_hostname = "dashdb-txn-sbox-yp-dal09-08.services.dal.bluemix.net"
    dsn_uid = "xdw00062"
    dsn_pwd = "9cx^2mpfzc5bkjm7"

    dsn_driver = "{IBM DB2 ODBC DRIVER}"
    dsn_database = "BLUDB"            # e.g. "BLUDB"
    dsn_port = "50000"                # e.g. "50000" 
    dsn_protocol = "TCPIP"            # i.e. "TCPIP"


#Create database connection
    dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

    try:
        conn = ibm_db.connect(dsn, "", "")
        print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)
    except:
        print ("Unable to connect: ", ibm_db.conn_errormsg() )

    
    #Lets first drop the table EXISITNGTABLES in case it exists from a previous attempt
    #dropQuery = "drop table Users_table"
    #Now execute the drop statment
    #dropStmt = ibm_db.exec_immediate(conn, dropQuery)
    
    #Construct the Create Table DDL statement - replace the ... with rest of the statement
    #createQuery = "create table INSTRUCTOR(ID INTEGER PRIMARY KEY NOT NULL, FNAME VARCHAR(20), LNAME VARCHAR(20), CITY VARCHAR(20), CCODE CHAR(2))"

    #Now fill in the name of the method and execute the statement
    #createStmt = ibm_db.exec_immediate(conn, createQuery)
    
    
    
    
   
   
    # ---------------------------------Machine learning model ------------------------------
    
    
    if dict['actionname'] == "heartPredict":
       
        
        result = " result is not ready yet"
        
        data = pd.read_csv("http://www.sharecsv.com/dl/48a7ffbf15e4eb29b59d28d882241f7a/cardio_train.csv")
     
     
  
        out_filter = ((data["ap_hi"]>250) | (data["ap_lo"]>200))
        data = data[~out_filter]
     
        
        out_filter2 = ((data["ap_hi"] < 0) | (data["ap_lo"] < 0))
        data = data[~out_filter2]
        
        target_name = 'cardio'
        data_target = data[target_name]
        data = data.drop([target_name], axis=1)
        

        _, test, _, _ = train_test_split(data, data_target, test_size=0.2, random_state=0)
        
      
     
        # making a dummy variable 
        
        p = test[8:9:1]
        
        #calling the Machine Learning API with the parameters extracted form the chat 
        # These are same data that should also be passed to our databse later on when we want to save user data.
        # We may also collect the result and prompt the user on the next visit and remind them we know how they are doing in terms of their general HEALTH. 
        
        
        
        api_call_to = "https://adv-care.herokuapp.com/predict/?age="+str(dict['user_age'])+ "&gen="+str((2 if dict['user_gender']=="male" else 1)) + "&hei="+str(dict['user_height']) +"&wei="+str(dict['user_weight']) +"&aph=" +str(dict['user_systolic']) +"&apl="+str(dict['user_diastolic'])+"&cho="+str(dict['user_cholesterol'])+"&glu="+str(dict['user_gluc'])+"&smo="+str((1 if dict['user_smoke']=="yes" else 0))+"&alc="+str((1 if dict['user_alco']=="yes" else 0))+"&act="+str((1 if dict['user_active']=="yes" else 0))

        
        with urllib.request.urlopen(api_call_to) as url:
            data = json.loads(url.read().decode())
            



        return {"healthPredictResult": data['Answer']}
        
    # ------------------------------end of Machine learning model ------------------------------
    

    # ---------------------------accessing drug infor using FDA api------------------------------

    
    if dict['actionname'] == "drugInfo":
        
        
        
        api_call_to = "https://api.fda.gov/drug/label.json?search=" + dict['drugName']
        with urllib.request.urlopen(api_call_to) as url:
            data = json.loads(url.read().decode())
            
        return {"drugInfo": data["results"][0]}
        
        
    # ---------------------------end of accessing drug infor using FDA api------------------------------

 
 
 
    # ---------------------------accessing drug Interactions using https://rxnav.nlm.nih.gov api------------------------------

    
    if dict['actionname'] == "drugInteration":
        
        #drugName1
        #drugName2
        
        
        api_call_to_extract_id = "https://rxnav.nlm.nih.gov/REST/rxcui.json?name=" + dict['drugName1'] + "&search=1"
        with urllib.request.urlopen(api_call_to_extract_id) as url:
            data1 = json.loads(url.read().decode())
            
        # first drug ID : data1['idGroup']['rxnormId'][0]
        
            
            
        api_call_to_extract_id = "https://rxnav.nlm.nih.gov/REST/rxcui.json?name=" + dict['drugName2'] + "&search=1"
        with urllib.request.urlopen(api_call_to_extract_id) as url:
            data2 = json.loads(url.read().decode())
        
        # second drug ID : data2['idGroup']['rxnormId'][0]
        
        
        api_call_to_result = "https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=" + data1['idGroup']['rxnormId'][0] + "+" + data2['idGroup']['rxnormId'][0]
        with urllib.request.urlopen(api_call_to_result) as url:
            data3 = json.loads(url.read().decode())

        #print(str(data3['fullInteractionTypeGroup'][0]['fullInteractionType'][0]['interactionPair'][0]['description']))
        
        #api_call_to_extract_id = "https://rxnav.nlm.nih.gov/REST/rxcui.json?name=" + dict['drugName2'] + "&search=1"
        #with urllib.request.urlopen(api_call_to_extract_id) as url:
        #    data2 = json.loads(url.read().decode())
        
        #api_call_to = "https://api.fda.gov/drug/label.json?search=" + dict['drugName']
        #with urllib.request.urlopen(api_call_to) as url:
        #    data = json.loads(url.read().decode())
            
        #return {"interactionDescription":str(data)}
        return {"interactionDescription": str(data3['fullInteractionTypeGroup'][0]['fullInteractionType'][0]['interactionPair'][0]['description'])}
        
    # ---------------------------end of accessing drug Interactions using https://rxnav.nlm.nih.gov api------------------------------

 

    # --------------------------- Insert a new user record into Databse ------------------------------
 
#// Insert a new event record
# function insertEvent(dsn, eventValues) {
#    try {
#       var conn=ibmdb.openSync(dsn);
#       // The timestamp value is derived from date and time values passed in
#       var data=conn.querySync("insert into events(shortname, location, begindate, enddate, contact) values(?,?,timestamp_format(?||' '||?,'YYYY-MM-DD HH24:MI:SS'),timestamp_format(?||' '||?,'YYYY-MM-DD HH24:MI:SS'),?)", eventValues);
#       conn.closeSync();
#       return {result: data, input: eventValues};
#    } catch (e) {
#        return { dberror : e }
#    }
#   }   
               
    # if dict['actionname']  == "insert":
    #     #Construct the query that retrieves all rows from the evenDB table
        
    #     insertQuery = "insert into events(firstname, lastname) values(" +"'" + str(dict['user_name']) +"'" + "," + "'" + str(dict['user_lastname']) +"'"+ ")"

    #     #Execute the statement
    #     selectStmt = ibm_db.exec_immediate(conn, insertQuery)

        
    #     #result = ibm_db.fetch_both(selectStmt)
    #     return {"msg": "I have succefully saved your information"}


        
    # else:
    #     data = "no-info"   
    
# ======== REZA edits =========

    if dict['actionname']  == "insert":
            #Construct the query that retrieves all rows from the evenDB table
            
            insertQuery = "INSERT INTO person(PID,FULLNAME, EMAIL) values(" +"'" + str(dict['pid']) +"'"+","+"'" + str(dict['user_name']) +"'" + "," + "'" + str(dict['email_addr']) +"'"+ ")"
    
            #Execute the statement
            selectStmt = ibm_db.exec_immediate(conn, insertQuery)
    
            
            #result = ibm_db.fetch_both(selectStmt)
            return {"msg": "I have successfully saved your information"}
    
    
            
    else:
            data = "no-info"    
            
# ======== REZA edits =========
    
 
 
 
 
            
 #   if dict['actionname']  == "searchByName":
        #Construct the query that retrieves all rows from the evenDB table
        
 #       selectQuery = "select CONTACT from events where shortname=" + "'" +dict['eventname'] + "'"

 #       #Execute the statement
 #       selectStmt = ibm_db.exec_immediate(conn, selectQuery)
#
        
 #       result = ibm_db.fetch_both(selectStmt)
 #       return {"byName": result['CONTACT']}



   

    #Construct the query - replace ... with the insert statement
    #insertQuery = "insert into eventDB values (1, 'Rav', 'Ahuja', 'TORONTO', 'CA')"

    #execute the insert statement
    #insertStmt = ibm_db.exec_immediate(conn, insertQuery)



#// Retrieve event information by searching the shortname
 #function fetchEventByShortname(dsn, eventname) {
  #  try {
#   #    var conn=ibmdb.openSync(dsn);
#    #   // Search for exact match only, could be extended with lIKE
#     #  var data=conn.querySync("select shortname, location, begindate, enddate, contact from events where shortname=? fetch first 10 rows only", [eventname]);
#      # conn.closeSync();
#       var resString="Data: \n";
#       for (var i=0;i<data.length;i++) {
#         resString+="name: "+data[i]['SHORTNAME']+" location: "+data[i]['LOCATION']+" info: "+data[i]['CONTACT']+" Start: "+data[i]['BEGINDATE']+" End: "+data[i]['ENDDATE']+"\n";
#       }
#       // Return both generated string and data
#       return {result : resString, data : data, input: eventname};
#    } catch (e) {
#        return { dberror : e }
#    }
#   }
   

#// Retrieve event information by searching the dates
# function fetchEventByDates(dsn, eventdates) {
#    try {
#       var conn=ibmdb.openSync(dsn);
#       // Base data is timestamp
#       var data=conn.querySync("select shortname, location, begindate, enddate, contact from events where begindate between ? and ?", eventdates.split(","));
#       conn.closeSync();
#       var resString="Data: \n";
#       for (var i=0;i<data.length;i++) {
#         resString+="name: "+data[i]['SHORTNAME']+" location: "+data[i]['LOCATION']+" info: "+data[i]['CONTACT']+" Start: "+data[i]['BEGINDATE']+" End: "+data[i]['ENDDATE']+"\n"
#       }
#       // Return both generated string and data
#       return {result: resString, data: data, input: eventdates};
#    } catch (e) {
#        return { dberror : e }
#    }
#   }

#// Insert a new event record
# function insertEvent(dsn, eventValues) {
#    try {
#       var conn=ibmdb.openSync(dsn);
#       // The timestamp value is derived from date and time values passed in
#       var data=conn.querySync("insert into events(shortname, location, begindate, enddate, contact) values(?,?,timestamp_format(?||' '||?,'YYYY-MM-DD HH24:MI:SS'),timestamp_format(?||' '||?,'YYYY-MM-DD HH24:MI:SS'),?)", eventValues);
#       conn.closeSync();
#       return {result: data, input: eventValues};
#    } catch (e) {
#        return { dberror : e }
#    }
#   }
   

#function main(params) {
#    dsn=params.__bx_creds[Object.keys(params.__bx_creds)[0]].dsn;

   # switch(params.actionname) {
  #      case "insert":
 #           return insertEvent(dsn,params.eventValues.split(","));
#        case "searchByDates":
      #      return fetchEventByDates(dsn,params.eventdates);
     #   case "searchByName":
    #        return fetchEventByShortname(dsn,params.eventname);
   #     default:
  #          return { dberror: "No action defined", actionname: params.actionname}
 #   }
#}



        


