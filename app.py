from datetime import datetime

# --- Borrow/Return ---
@app.route('/transactions', methods=['GET', 'POST'])
def manage_transactions():
    if request.method == 'GET':
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
