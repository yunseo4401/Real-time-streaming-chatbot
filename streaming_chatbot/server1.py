from flask import Flask, render_template, request
import os


app=Flask(__name__)
@app.route("/",methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index_making.html')
    
if __name__ == '__main__':
   app.run(debug=True)