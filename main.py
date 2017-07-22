from flask import Flask
from flask import json
import redis
import subprocess

app = Flask(__name__)

def _redisConnect():
   return redis.StrictRedis(host='redis', port=6379, db=0);

@app.route("/")
def index():
   return "Hello World"

@app.route("/visits")
def visits():
   r = _redisConnect()
   if r.exists('visits') == False:
      r.set('visits',0)
   visits = int(r.get('visits'))+1
   r.set('visits',visits)
   return "Total visits %d" % visits

@app.route("/keys")
def keys():
   r = _redisConnect()
   response = app.response_class(
        response=json.dumps(r.keys()),
        status=200,
        mimetype='application/json'
    )
   return response

@app.route("/version")
def version():
   ver = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
   output = ver.stdout.read()
   return "Commit %s" % output

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=80)