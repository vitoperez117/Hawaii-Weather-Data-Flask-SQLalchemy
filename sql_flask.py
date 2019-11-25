from flask import Flask

# /
# Home page.
# List all routes that are available.

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    Available routes
    /
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/<start>
    /api/v1.0/<start>/<end>
    '''

if __name__ == '__main__':
    app.run(debug=True)