from flask import *
import pymysql
import sms



#the imports for the Mpesa function
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

app.secret_key="1stughndiekgy58"

@app.route("/")
def home():
    return render_template("home.html")



@app.route("/login",methods=["POST","GET"]) 
def login():
    if request.method=="GET":
        return render_template("login.html") 
    else:
        #get the details entered on the form and store them on variables
        username=request.form["username"]
        password=request.form["password"]
        #establish a connection to the database
        connection=pymysql.connect(host="localhost",user="root", password="" ,database="project")
        sql="SELECT *FROM register WHERE username=%s and password =%s"
        #strumethod=["POST","GET"] a cursor that will be used to execute the above sql
        cursor=connection.cursor()
        #create a variable that will hold both the user name and the password entered on the form
        data=(username,password)
        #use the cursor to execute
        cursor.execute(sql,data)

        if cursor.rowcount==0:
            return render_template("login.html",error="Invalid credentials")
        else:
            session["key"]=username
            return redirect("/")
@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    #requesting details entered on the form
    if request.method=="POST":
        username=request.form["username"]
        password1=request.form["password1"]
        password2=request.form["password2"]
        email = request.form["email"]
        phone=request.form["phone"]
         
         #check whether the length of the password is greater or equal to 8
        if len(password1)  <8:
            return render_template("register.html",error="password must be more than 8 characters ")
        elif password1 !=password2:
            return render_template("register.html",error="password must be the same")
        else:
            #create a database connection
            connection=pymysql.connect(host="localhost",user="root",password="",database="project")
            #create the sql to insert data.The %sis a placeholder.To be replaced with actual data when the query executes

            sql="insert  into register(username,password,email,phone) values(%s,%s ,%s, %s)" 
            #create a variable data to hold the data obtained from th form
            data=(username,password1,email,phone) 
            #create a cursor tpo execute the query above
            cursor=connection.cursor()  
            #use the cursor to execute
            cursor.execute(sql,data)
            #Finish the action by use of the  commit function 
            connection.commit()

            #Sending an sms after a successful registration(it will contain the password and the username)
            sms.send_sms(phone,f"{username},Thank you for registering.Welcome to Kawasi Hostels.Your password is: {password1}")

            return render_template("register.html",success="Registered Successfully") 
    else:
        return render_template("register.html")
    
@app.route("/booknow", methods=["POST", "GET"])
def booknow():
    if request.method=="POST":
        FirstName=request.form["FirstName"]
        LastName=request.form["LastName"]
        TelephoneNumber=request.form["TelephoneNumber"]
        Email = request.form["Email"]
        Age=request.form["Age"]
        Gender=request.form["Gender"]
        University=request.form["University"]
        RoomType=request.form["RoomType"]


        #create a database connection
        connection=pymysql.connect(host="localhost",user="root",password="",database="project")
        #create the sql to insert data.The %s is a placeholder.To be replaced with actual data when the query executes

        sql="insert into booknow(FirstName,LastName,Email,TelephoneNumber,Age,Gender,University,RoomType) values(%s,%s ,%s, %s, %s, %s, %s, %s)" 
        #create a variable data to hold the data obtained from the form
        data=(FirstName,LastName,Email,TelephoneNumber,Age,Gender,University,RoomType) 
        #create a cursor tpo execute the query above
        cursor=connection.cursor()  
        #use the cursor to execute
        cursor.execute(sql,data)
        #Finish the action by use of the  commit function 
        connection.commit()



        return render_template("booknow.html", success="Booked Successfully")

    else:
        return render_template("booknow.html")





@app.route("/universities")
def universities():
    return render_template("universities.html")

@app.route("/residencies")
def residencies():
    return render_template("residencies.html")

@app.route("/houses",methods=["POST","GET"])
def houses():
    if request.method == "GET":

        return render_template("houses.html")
    else:
        data = request.form
        bedrooms = data["bedrooms"]
        lights = data["lights"]
        wardrobe = data["wardrobe"]


         #create a database connection
        connection=pymysql.connect(host="localhost",user="root",password="",database="project")
        #create the sql to insert data.The %sis a placeholder.To be replaced with actual data when the query executes

        sql="insert  into housedetails(no_of_bedrooms,lights,wardrobe) values(%s,%s ,%s)" 
        #create a variable data to hold the data obtained from th form
        data=(bedrooms,lights,wardrobe) 
        #create a cursor tpo execute the query above
        cursor=connection.cursor()  
        #use the cursor to execute
        cursor.execute(sql,data)
        #Finish the action by use of the  commit function 
        connection.commit()

        

        return render_template("houses.html",success="House Registered Successfully") 

@app.route("/reviews",methods=["GET"])
def reviews():
     #create a database connection
    connection=pymysql.connect(host="localhost",user="root",password="",database="project")
    #sql to fetch the records in the category of smartphones
    sql="SELECT * FROM `reviews`"
    #creat a cursor to excecute the query
    cursor=connection.cursor()
    #use the cursor created above to execute the query
    cursor.execute(sql)
    #fetch all the details entry that are in category smartphones
    reviews=cursor.fetchall()
    return render_template("reviews.html", reviews = reviews)


@app.route("/single_item/<product_id>")
def single_item(product_id):

    #create a database connection
    connection=pymysql.connect(host="localhost",user="root",password="",database="project")
    #sql to fetch a single product from the database
    sql="SELECT * FROM `housedetails` WHERE house_number=%s "
    #cursor mto execute the query
    cursor=connection.cursor()
    #Execute the cursor.The %s placeholder will be replaced with real data when we execute the cursor
    cursor.execute(sql,(product_id))
    #create a variable that will store the data of one entry/record
    x=cursor.fetchone()

    
    return render_template('single_item.html',x=x)




@app.route('/mpesapayment', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and join us in our hostels</h3>' \
               '<a href='"/"' class="btn btn-dark btn-sm">Back to Products</a>'
    

@app.route ("/reviewsform",methods=["POST","GET"])
def reviewsform():
    if request.method=="POST":
     
        email=request.form["email"]
        feedback=request.form["feedback"]
        name=request.form["name"]
        

        
        connection=pymysql.connect(host="localhost", user="root",database="project",password="")
        sql="insert  into reviews(email,feedback,name) values(%s,%s ,%s)"
        data=(email,feedback,name)
        cursor=connection.cursor()
        cursor.execute(sql,data)
        connection.commit()
        return render_template("reviews.html",success="Uploaded successfully")
            
    else:
      
        return render_template("reviews.html")

@app.route("/residencies1")
def res1():
    return render_template("residencies1.html")

@app.route("/residencies2")
def res2():
    return render_template("residencies2.html")
    











app.run(debug= True)