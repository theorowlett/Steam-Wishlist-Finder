from flask import Flask, render_template, request
import steam
app = Flask('__name__')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        username = request.values.get('username')
        print(username)
        steamID = steam.get_steamid(username)
        wishlist_games = steam.get_wishlist(steamID)
        wishlist = steam.Wishlist(wishlist_games)
        wishlist = steam.itad(wishlist)
        print(wishlist)
        return render_template('result.html',wishlist = wishlist.games)
    else:
        return render_template('index.html')
app.run(debug=True)

if __name__=='__main__':
    index()