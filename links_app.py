# -*- coding: utf-8 -*-
import sqlite3
from flask import Flask, url_for, render_template, request, session, redirect

from hello import print_hello

# Connection DB SQLITE 3
########################################
#conn = sqlite3.connect('links_db.db')
#c = conn.cursor()
'''
# Create table
c.execute('CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# cur.execute("insert into people values (?, ?)", (who, age))

# Do this instead
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print c.fetchone() # print c.fetchall()


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
'''
########################################

app = Flask(__name__)

app.secret_key = 'QGhdfjFDGHhd77834bhHJ8436523827Duiuifd'








## INDEX PAGE
@app.route('/')
def index():
	if ('login' in session) and ('auth' in session):
		str = 'List links'

		conn = sqlite3.connect('links_db.db')
		c = conn.cursor()
		c.execute('SELECT * FROM links')
		list_links = c.fetchall()
		# Save (commit) the changes
		conn.commit()
		c.close()
		return render_template('index.html', string=str, list_links=list_links)
	else:
		return redirect(url_for('login'))

## ADD FORM
@app.route('/add_form', methods=['GET', 'POST'])
def add_form():
	if 'login' in session:
		error_message = '' # Error!!!
		
		if request.method == 'POST':
			# Если данные дошли
			link = request.form['link']
			
			# Если пустая строка, то выводим сообщение об ошибке
			if link == '':
				error_message = 'Link zero!'
				return render_template('add_form.html', error_message = error_message)
			# Иначе, обрабатываем...
			else:
				label 		= request.form['label']
				description = request.form['description']
				
				conn = sqlite3.connect('links_db.db')
				c = conn.cursor()
				c.execute("INSERT INTO links(link, label, description) VALUES (?, ?, ?)", (link, label, description))
				# Save (commit) the changes
				conn.commit()
				c.close() 
				return 'Data add... <a href="/" alt="">Home</a>'
		else:
			# Если данные НЕ дошли, показываем форму для ввода
			form = '''<form action="/add_form" method="post">
						<label>Link: </label>
						<input name="link" type="text" size="45" maxlength="45" value=""><br />
						<label>Label: </label>
						<input name="label" type="text" size="25" maxlength="25" value=""><br />
						<link>Description:</link>
						<textarea cols=50 rows=8 name="description"></textarea><br />
						<input type="submit" name="submit" value="Send">
					</form>'''
			return render_template('add_form.html', error_message = error_message)
	else:
		return redirect(url_for('login'))








### EDIT
@app.route('/edit_form/', methods=['GET', 'POST'])
@app.route('/edit_form/<int:id>', methods=['GET', 'POST'])
# Если id нет, то присваиваем ей 1
def edit_form(id = 1):
	if 'login' in session:
		if request.method == 'POST':
			link 		= request.form['link']
			label 		= request.form['label']
			description = request.form['description']

			conn = sqlite3.connect('links_db.db')
			c = conn.cursor()
			c.execute("UPDATE links SET link = ?, label = ?, description = ? WHERE id = ?", (link, label, description, id))
			# Save (commit) the changes
			conn.commit()
			c.close()
			return redirect(url_for('index'))
		else:
			conn = sqlite3.connect('links_db.db')
			c = conn.cursor()
			c.execute('SELECT * FROM links WHERE id = ?', (id,))
			list_links = c.fetchone()
			# Save (commit) the changes
			conn.commit()
			c.close()
			return render_template('edit_form.html', list_links = list_links, id = id)
	else:
		return redirect(url_for('login'))







### VIEW
# Если id нет, то присваиваем ей 1
@app.route('/view/', methods=['GET', 'POST'])
@app.route('/view/<int:id>', methods=['GET', 'POST'])
def view(id = 1):
	if 'login' in session:
		conn = sqlite3.connect('links_db.db')
		c = conn.cursor()
		c.execute('SELECT * FROM links WHERE id = ?', (id,))
		list_links = c.fetchone()
		# Save (commit) the changes
		conn.commit()
		c.close()
		return render_template('view.html', list_links = list_links, id = id)
	else:
		return redirect(url_for('login'))





### DELELE
# Если id нет, то присваиваем ей 1
@app.route('/del/', methods=['GET'])
@app.route('/del/<int:id>', methods=['GET'])
def delete(id = 1):
	if 'login' in session:
		conn = sqlite3.connect('links_db.db')
		c = conn.cursor()
		c.execute('DELETE FROM links WHERE id = ?', (id,))
		conn.commit()
		return 'Deleting... <a href="/" alt="">Home</a>'
		# DELETE FROM CLIENTS WHERE C_NO > 5;
		#return render_template('del.html', id=id)
	else:	
		return redirect(url_for('login'))





		
### LOGIN
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if not 'login' in session:
		if request.method == 'POST':
			login 		= request.form['login']
			password 	= request.form['password']
			if login == '':
				error_message = 'Form empty...'
				return render_template('login.html', error_message = error_message)
			else:
				if auth(login, password):
					session['auth'] = 1
					session['login'] = login # Save Sessions
					#error_message = 'DATA SAVE!'
					#return render_template('login.html', error_message = error_message)
					return redirect(url_for('index')) #'Session - %s' %(session['login'])

				else:
					error_message = 'User not in DB!'
					return render_template('login.html', error_message = error_message)
		else:
			return render_template('login.html')
	else:
		return redirect(url_for('index'))




### LOGOUT
@app.route('/logout', methods = ['GET'])
def logout():
	del(session['auth']) # Delete Sessions
	del(session['login'])
	return 'Log out - <a href="' + url_for('index') + '">Home</a>'
	
	



### INSTALL DB
@app.route('/install', methods = ['GET'])
def install():
	conn = sqlite3.connect('links_db.db')
	c = conn.cursor()
	c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, login VARCHAR(100), password VARCHAR(100))") # Создание таблицы БД
	c.execute("CREATE TABLE links (id INTEGER PRIMARY KEY, link VARCHAR(100), label VARCHAR(100), description TEXT)") # Создание таблицы БД
	# Insert a row of data	
	c.execute("INSERT INTO users(login, password) VALUES ('admin','12345')")
	c.execute("INSERT INTO links(link, label, description) VALUES ('www.cesis.ru','cesis.ru', 'ЗАО ЦеСИС НИКИРЭТ')")
	# Save (commit) the changes
	conn.commit()
	c.close()
	'''	sqlite_query($db, "CREATE TABLE users (
                      id INTEGER PRIMARY KEY,
                      login TEXT,
                      password TEXT
                      );")
	sqlite_query($db, "INSERT INTO users(login, password) VALUES
                      ('admin', '12345''".time()."');")
	'''

	return 'Install db!'


	

### AUTH Function
def auth(login, password):
	conn = sqlite3.connect('links_db.db')
	c = conn.cursor()
	c.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password))
	users = c.fetchone() #users = c.fetchall()
	if users != None: # Если не найдено, то False
		return login
	else:
		return False
	#for row in c.execute('SELECT * FROM stocks ORDER BY price'):
	#	print row
	#return '%s' %(users[1])







@app.route('/hello', methods = ['GET'])
def hello():
	str = print_hello() # Вызов функции из модуля!
	return '%s' % str




if __name__ == '__main__':
	#app.debug = True
    app.run(debug=True)
