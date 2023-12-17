from flask import Flask

app = Flask(__name__)

@app.route("/")

def helloworld():
    return "Hello World!"
            
@app.route("/get_data")
def getdata():
    data = {
        'name' : 'My Name',
        'url' : 'My URL'
    }
    return json.dumps(data)   
    
if __name__ == "__main__":
    app.run()     
