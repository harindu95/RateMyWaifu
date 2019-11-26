from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

DATABASE = 'database.db'

@app.route('/')
def main():
    return render_template("main.html")

	
@app.route('/login')
def login():
	return "<H1> LOGIN </H1>"
	
@app.route('/waifu')
def new_student():
   return render_template('waifu.html')

@app.route('/newwaifu',methods = ['POST', 'GET'])
def newwaifu():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         descr = request.form['desc']
         imagurl = request.form['imgurl']
         aname = request.form['aname']
#         pin = request.form['pin']
         
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

@app.route('/waifulist')
def waifulist():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from character")
   
   rows = cur.fetchall();
   return render_template("waifulist.html",rows = rows)
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

