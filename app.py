from datetime import datetime

# --- User Management ---
@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE'])
def manage_users():
    if request.method == 'GET':
        return jsonify(list(users.values()))
    elif request.method == 'POST':
        data = request.json
        name = data.get('name', '').strip()
        if not name:
            return jsonify({'error':'Name required'}), 400
        user_id = str(uuid.uuid4()) #generates unique uuid
        users[user_id] = {'id': user_id, 'name': name}
        return jsonify(users[user_id]), 201
    elif request.method == 'DELETE':
        user_id = request.args.get('id')
        if user_id in users:
            del users[user_id]
            # Remove user's borrowed books
            for tx in list(transactions):
                if tx['user_id'] == user_id:
                    transactions.remove(tx)
            return '', 204
        return 'User not found', 404
def delete_user(user_id):
    if user_id in users:
        
# --- Borrow/Return ---
@app.route('/transactions', methods=['GET', 'POST'])
def manage_transactions():
    if request.method == 'GET':from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'static/covers'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/covers/<filename>')
def cover_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
    from flask import request, jsonify, session

users = {}
books = {}
transactions = []

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'status':'error', 'message':'Name required'}), 400
    user = next((u for u in users.values() if u['name'].lower() == name.lower()), None)
    if not user:
        user_id = str(len(users) + 1)
        user = {'id': user_id, 'name': name}
        users[user_id] = user
    session['user_id'] = user['id']
    return jsonify({'status':'success', 'user': user})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'status':'success'})

@app.route('/session')
def check_session():
    user_id = session.get('user_id')
    if user_id and user_id in users:
        return jsonify({'logged_in':True, 'user':users[user_id]})
    return jsonify({'logged_in':False})
@app.route('/books')
def list_books():
    if 'user_id' not in session:
        return jsonify({'status':'error', 'message':'Login required'}), 401
    return jsonify({'books': list(books.values())})
        return jsonify(transactions)
    elif request.method == 'POST':
        data = request.json
if not all(k in data for k in ('action', 'user_id', 'book_id')):
    return jsonify({'status':'error', 'message':'Missing required fields'}), 400
action = data['action']
user_id = data['user_id']
book_id = data['book_id']
        if user_id not in users or book_id not in books:
            return jsonify({'status':'error', 'message':'Invalid user or book'}), 400
        is_borrowed = any(
            tx for tx in transactions
            if tx['book_id'] == book_id and tx['action']=='borrow' and
            not any(
                t2 for t2 in transactions
                if t2['book_id']==book_id and t2['action']=='return' and t2['date'] > tx['date']
            )
        )
        if action == 'borrow':
            if is_borrowed:
                return jsonify({'status':'error', 'message':'Book already borrowed'}), 400
        elif action == 'return':
            if not is_borrowed:
                return jsonify({'status':'error', 'message':'Book is not borrowed'}), 400
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transactions.append({
            'user_id': user_id,
            'user_name': users[user_id]['name'],
            'book_id': book_id,
            'book_title': books[book_id]['title'],
            'action': action,
            'date': date
        })
        return jsonify({'status': 'success'}), 201
    # --- User Borrowed Books ---
@app.route('/user_borrowed_books')
def user_borrowed_books():
    user_id = request.args.get('user_id')
    borrowed = []
    for tx in transactions:
        if tx['user_id'] == user_id and tx['action'] == 'borrow':
            # Check if not returned
            book_id = tx['book_id']
            returned = any(
                t2 for t2 in transactions
                if t2['book_id']==book_id and t2['user_id']==user_id and t2['action']=='return' and t2['date'] > tx['date']
            )
            if not returned:
                book = books[book_id].copy()
                if book['cover']:
                    book['cover_url'] = '/static/covers/' + book['cover']
                else:
                    book['cover_url'] = ''
                borrowed.append(book)
    return jsonify(borrowed)
from threading import Lock

transaction_lock = Lock()

# ... inside manage_transactions POST block ...
with transaction_lock:
    # Check book availability and process the transaction here
    is_borrowed = any(
        tx for tx in transactions
        if tx['book_id'] == book_id and tx['action']=='borrow' and
        not any(
            t2 for t2 in transactions
            if t2['book_id']==book_id and t2['action']=='return' and t2['date'] > tx['date']
        )
    )
    if action == 'borrow':
        if is_borrowed:
            return jsonify({'status':'error', 'message':'Book already borrowed'}), 400
    elif action == 'return':
        if not is_borrowed:
            return jsonify({'status':'error', 'message':'Book is not borrowed'}), 400
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transactions.append({
        'user_id': user_id,
        'user_name': users[user_id]['name'],
        'book_id': book_id,
        'book_title': books[book_id]['title'],
        'action': action,
        'date': date
    })
return jsonify({'status': 'success'}), 201
