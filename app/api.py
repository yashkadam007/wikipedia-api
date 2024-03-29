from flask import Flask, request, jsonify, json
from flask_restful import Resource, Api
from word_counter import get_top_words
from models import db, SearchHistory
from flask_caching import Cache

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wikipedia_search.db'  # SQLite database file
db.init_app(app)
api = Api(app)

# Configure Flask-Caching for improving performance
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class WordFrequency(Resource):
    #cache to handle same query
    @cache.cached(timeout=300, make_cache_key=lambda *args, **kwargs: f"word_frequency_{str(hash(frozenset(request.args.items())))}")
    def get(self):
        try:
            topic = request.args.get('topic')
            n = request.args.get('n', 10)

            # Check if n is not present or negative
            if n is None or int(n) < 1:
                raise ValueError("Invalid value for 'n'. Please provide a non-negative integer.")
            n = int(n)
            # Get word frequency result
            result = get_top_words(topic, n)

            status = "success" if "top_n_words" in result else "error"
            
            # Save the search history in the database
            search_history_entry = SearchHistory(
                topic=topic,
                result=jsonify(result).data.decode('utf-8'),
                status=status,
            )

            db.session.add(search_history_entry)
            db.session.commit()

            return jsonify(result)
        
        except ValueError:
            return {"status": "error", "message": "Invalid value for n. provide non negative integer"}

class WordFrequencySearchHistory(Resource):
    def get(self):
        # Retrieve the search history from the database
        search_history = SearchHistory.query.all()

        # Format the result for the API response
        response_data = []

        for entry in search_history:
            result = json.loads(entry.result)
            status = "success" if "top_n_words" in result else "error"

            entry_data = {
                "topic": entry.topic,
                "result": {
                    "status": status,
                    "message": result.get("message", None),  # Include an error message if present
                    "top_n_words": result.get("top_n_words", None)
                }
            }

            response_data.append(entry_data)

        return jsonify(response_data)  

# error handling for invalid routes
@app.errorhandler(404)
def not_found(e):
    return {"status": "error", "message": "Invalid route. Please check the URL."}, 404

#apis
api.add_resource(HelloWorld, '/')
api.add_resource(WordFrequency, '/api/word-frequency')
api.add_resource(WordFrequencySearchHistory, '/api/search-history')

if __name__ == '__main__':
    with app.app_context():
        # uncomment below line to clear the db
        #db.drop_all()
        db.create_all()
    app.run(debug=True)