# Wikipedia Search amd History APIs

This project is a simple Flask-based API for retrieving word frequency information and search history from Wikipedia.

### Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yashkadam007/wikipedia-api.git
   cd wikipedia-api
   ```
2. Install virtualenv
   ```bash
   pip3 install virtualenv
   ```
4. Initialize virtualenv
   ```bash
   python3 -m venv env
   ```
5. Start virtualenv
   `source env/bin/activate`
6. Install dependencies
   `pip install -r requirements.txt`
7. Run Flask server
   `python3 app/api.py`
8. Run tests on Flask server
   `python3 app/test_api.py`

### Usage
1. Start the server using the command mentioned above for Run Flask server
2. Visit `http://127.0.0.1:5000/` on your browser this should print
   ```json
    {
    "hello": "world"
    }
   ```
3. Visit `http://127.0.0.1:5000/?topic=color&n=5` on your browser this should print word frequency information for the topic. You can play around this and try different values for topic and n
4. Visit  `http://127.0.0.1:5000/api/search-history` on your browser to see your search history
   
