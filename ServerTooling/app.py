import json
from flask import Flask, render_template, jsonify, request
from static.pyfiles.server import MonitorToolManage
from static.pyfiles.server2 import MonitorToolManage2
app = Flask(__name__)

machinename = ""
ip = ""
password = ""
command_ = ""

dict_ = {
    'cpu' : "",
    'disk' : "",
    'battery' : "",
}

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/getoutput", methods =["GET", "POST"])
def getOutput():
    global machinename,ip, password, command_
    if request.method == "POST" : 
        data = json.loads(request.data)
        try:
            machinename = data['machine_name']
            ip =  data['ip']
            password = data['passowrd']
        except KeyError:
            pass
        
        try:
            command_ = data['inputcmd']
        except KeyError:
            pass

        # obj = MonitorToolManage(ip, machineName, password, command_, numb)
        if not command_ :
            value = {
                'text' : "Please enter the command."
            }
            return jsonify(values= value)
        # obj = MonitorToolManage("127.0.0.1", "spartan", "l", "ls", 7)
        # print("\n\n",ip, machinename, password, command_, "\n\n")
        obj = MonitorToolManage(ip, machinename, password, command_, 7)

        text = obj.getCommandInfo()
        value = {
            'text' : text
        }
        return jsonify(values= value)
    return render_template("runcommands.html")


@app.route("/getstatus", methods =["GET", "POST"])
def getStatus():
    if request.method == "POST" : 
        data = json.loads(request.data)
        # MonitorToolManage2("127.0.0.1", "spartan", "l", 7)
        MonitorToolManage2(data['ip'], data["machine_name"], data["passowrd"], 7)
        f = open("static/pyfiles/7.txt")
        ls = f.readlines()
        for i,j in zip(range(len(ls)),dict_) :
            dict_[j] = ls[i+1]
        dat_json = json.dump(dict_)
        
        with open("static/js/7.json", "w") as outfile:
            outfile.write(dat_json)

    return render_template("getstatus.html")



if __name__ == '__main__' : 
    app.run(debug=True)