from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Predefined books for the "Buy" section
books = [
    {"name": "Into the Wild", "author": "Jon Krakauer", "genre": "Adventure", "price": "$10", "ratings": "4.5/5", "edition": "1st Edition", "image": "adventure.jpg"},
    {"name": "It", "author": "Stephen King", "genre": "Horror", "price": "$15", "ratings": "4.8/5", "edition": "2nd Edition", "image": "horror.jpg"},
    {"name": "Pride and Prejudice", "author": "Jane Austen", "genre": "Love Story", "price": "$12", "ratings": "4.7/5", "edition": "3rd Edition", "image": "love_story.jpg"},
    {"name": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Novel", "price": "$18", "ratings": "4.9/5", "edition": "1st Edition", "image": "novels.jpg"},
    {"name": "The Diary of a Young Girl", "author": "Anne Frank", "genre": "Biography", "price": "$10", "ratings": "4.6/5", "edition": "1st Edition", "image": "biographies.jpg"},
]

# Global variable to track checkout actions
checkout_actions = []

@app.route('/')
def home():
    return render_template('index.html', books=books, checkout_count=len(checkout_actions))

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_price = request.form['book_price']
        action_message = f"Book purchased: {book_name} for {book_price}."
        checkout_actions.append({"action": "Buy", "details": action_message, "amount": float(book_price.strip('$'))})
        return redirect(url_for('checkout'))
    return render_template('buy.html', books=books, checkout_count=len(checkout_actions))

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        book_name = request.form['name']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']
        cost_price = float(price) * 0.6
        action_message = f"Your book '{book_name}' can be sold for ${cost_price:.2f}."
        checkout_actions.append({"action": "Sell", "details": action_message, "amount": -cost_price})
        return render_template('sell.html', message=action_message, success=True, confirm=True, checkout_count=len(checkout_actions))
    return render_template('sell.html', checkout_count=len(checkout_actions))

@app.route('/exchange', methods=['GET', 'POST'])
def exchange():
    if request.method == 'POST':
        book_name = request.form['name']
        exchange_book = books[0]  # Giving the first book in the list for exchange
        action_message = f"Exchange '{book_name}' with '{exchange_book['name']}'."
        checkout_actions.append({"action": "Exchange", "details": action_message, "amount": 0})
        return render_template('exchange.html', exchange_book=exchange_book, message=action_message, confirm=True, checkout_count=len(checkout_actions))
    return render_template('exchange.html', checkout_count=len(checkout_actions))

@app.route('/checkout')
def checkout():
    # Calculate the total amount to pay or receive
    total_amount = sum(action['amount'] for action in checkout_actions)
    return render_template('checkout.html', actions=checkout_actions, total_amount=total_amount, checkout_count=len(checkout_actions))

if __name__ == '__main__':
    app.run(debug=True)
