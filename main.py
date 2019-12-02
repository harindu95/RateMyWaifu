from flask import Flask, render_template, request
import sqlite3 as sql
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)

DATABASE = 'database.db'

@app.route('/')
def main():
    return render_template("main.html")

	
@app.route('/login')
def login():
	return "<H1> LOGIN </H1>"

@app.route('/anime')
def new_anime():
#   dropdown_list = ['Air', 'Land', 'Sea']
   return render_template('anime.html')

@app.route('/newanime',methods = ['POST', 'GET'])
def newanime():
   if request.method == 'POST':
      class inputError(Exception):
         pass
      try:
         
         nm = request.form['nm']
         descr = request.form['desc']
         imagurl = request.form['imgurl']
         season = request.form['season']
         yr = request.form['yr']
         numEps = request.form['eps']
         esrb = request.form['esrb']
         sname = request.form['snm']
#         pin = request.form['pin']
         if (len(nm)<1 or len(sname)<1):
            msg = "required field is empty"
            raise inputError         
         with sql.connect("database.db") as con:
             
            cur = con.cursor()

            cur.execute("INSERT INTO anime (name,coverImage,description,season,year,numEpisodes,esrb,sName) VALUES (?,?,?,?,?,?,?,?)",(nm,imagurl,descr,season,yr,numEps,esrb,sname) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()
	
@app.route('/waifu')
def new_waifu():
   return render_template('waifu.html')

@app.route('/newwaifu',methods = ['POST', 'GET'])
def newwaifu():
   if request.method == 'POST':
      class inputError(Exception):
         pass
      try:
         nm = request.form['nm']
         descr = request.form['desc']
         imagurl = request.form['imgurl']
         aname = request.form['aname']
#         pin = request.form['pin']
         if (len(nm)<1 or len(aname)<1):
            msg = "required field is empty"
            raise inputError         
         with sql.connect("database.db") as con:
             
            cur = con.cursor()
            charID = len(cur.execute("select * from character").fetchall())+1

            cur.execute("INSERT INTO character (charID,name,description,image,aName) VALUES (?,?,?,?,?)",(charID,nm,descr,imagurl,aname) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/user')
def new_user():
   return render_template('user.html')

@app.route('/newuser',methods = ['POST', 'GET'])
def newuser():
   if request.method == 'POST':
      class pwMismatch(Exception):
         pass
      class emptyField(Exception):
         pass
      try:
         unm = request.form['uname']
         pword = request.form['pw']
         cpword = request.form['cpw']
         fnm = request.form['fname']
         lnm = request.form['lname']
         dob = request.form['dob']
#         month = request.form['mn']
#         year = request.form['yr']
         descr = request.form['desc']
         imagurl = request.form['imgurl']
         moderator = 0
         if (request.form.get('mflag')):
            moderator = 1
         admin = 0
         if (request.form.get('aflag')):
            admin = 1
#         moderator = request.form['mflag']
#         admin = request.form['aflag']
#         pin = request.form['pin']
         if (pword != cpword): 
            msg = "password does not match"
            raise pwMismatch
         if (len(unm)<1 or len(pword)<1 or len(fnm)<1 or len(lnm)<1 ):
            msg = "required field is empty"
            raise emptyField
         with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("INSERT INTO user (username,password,firstName,lastName,dob,image,description,modFlag,adminFlag) VALUES (?,?,?,?,?,?,?,?,?)",(unm,pword,fnm,lnm,dob,imagurl,descr,moderator,admin) )
            
            con.commit()
            msg = "User successfully added"
#      except pwMismatch:
#         con.rollback()
#         msg = "password does not match"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

		 
@app.route('/waifulist')
def waifulist():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from character")
#   cur.execute("select * from (character AS C JOIN anime AS A On C.aName=A.name) WHERE year=2015")
   
   rows = cur.fetchall();
   return render_template("waifulist.html",rows = rows)
   
@app.route('/userlist')
def userlist():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from user")
   
   rows = cur.fetchall();
   return render_template("userlist.html",rows = rows)

@app.route('/animelist')
def animelist():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from anime")
   
   rows = cur.fetchall();
   return render_template("animelist.html",rows = rows)
"""
@app.route('/test')
def test():
	g.db = sqlite3.connect(DATABASE, timeout=10)
	cur = g.db.execute('SELECT name from test')
	Tests = [dict(ID=row[0],city=row[1]) for row in cur.fetchall()]
	g.db.close()
	return render_template('test.html', Tests=Tests)
	
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
"""
if __name__ == '__main__':
	app.run(debug=True)

