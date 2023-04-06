from flask import Flask
import SupermaketItems
app = Flask(__name__)
@app.get('/items')
def getItems():
    return {'items': SupermaketItems.fetchAll()}

@app.route('/items/<categories>')
def get_programming_language(categories):
   return SupermaketItems.fetchCategories(categories)


if __name__ == '__main__':
    app.run()  # run our Flask app