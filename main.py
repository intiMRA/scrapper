from flask import Flask
import SupermaketItems
app = Flask(__name__)
@app.get('/items/<page>')
def getPage(page):
    return {'items': SupermaketItems.fetchPage(page)}

@app.route('/items/<categories>')
def get_programming_language(categories):
   return SupermaketItems.fetchCategories(categories)


if __name__ == '__main__':
    app.run()  # run our Flask app