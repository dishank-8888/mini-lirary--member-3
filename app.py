from datetime import datetime

# --- Borrow/Return ---
@app.route('/transactions', methods=['GET', 'POST'])
def manage_transactions():
    if request.method == 'GET':
        return jsonify(transactions)
    elif request.method == 'POST':
        data = request.json
        action = data['action'] # 'borrow' or 'return'
        user_id = data['user_id']
        book_id = data['book_id']
        if user_id not in users or book_id not in books:
            return jsonify({'status':'error', 'message':'Invalid user or book'}), 400
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

