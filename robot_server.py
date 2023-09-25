from flask import Flask, request, jsonify
import sys
import os
import subprocess
import json
import time


logfile = '/home/canbee/Desktop/ROBOT/py532lib/robot_logs.json'
nfcRead = '/home/canbee/Desktop/ROBOT/py532lib/nfcRead.py'
inputsfile = '/home/canbee/Desktop/ROBOT/py532lib/input.json'
test_data_file = '/home/canbee/Desktop/ROBOT/py532lib/testdata.json'

sys.path.append(os.path.join(os.path.abspath(__file__ + "../../../")))
sys.path.append('/home/pi/Desktop/ROBOT/py532lib/py532lib')
#print(sys.path)
#from py532lib.nfcRead.py import readnfc
#nr=readnfc
app = Flask(__name__)

# GET endpoint

@app.route('/readNfc', methods=['GET'])
def get_data():
    cmd='python3 ' + nfcRead
    comd=subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out,err =comd.communicate()
    string=out.decode('utf-8')
    print(string)
    tag=eval(string)
    # Perform any necessary operations to retrieve data
    #data_list=[nr.card_data, nr.card_len_checksum, nr.card_data_checksum, nr.card_frame_type]
    try:
        x = open(logfile,'r')
        data=json.load(x)
        x.close()
    except:
        ret_data={'warning':'data is empty'}
        x = open(logfile,'w')
        json.dump({}, x, indent=4)
        x.close()
        x = open(logfile,'r')
        data=json.load(x)
        x.close()
    data['NFC_tag']=tag
    tag = tag['card_data'].split('\\')[-5]
    #let us assume the following sequence
    tag_sequence={
            'xf0':1,
            'xf9':2,
            'x00':3,
            'x08':4,
            'x10':5,
            'x17':6,
            'xee':7,
            'xef':8,
            'xd1':9,
            'xcb':10,
            'xff':11,
            'xa7!':12,
            'xe72':13,
            'x1dr3':14,
            'x98D':15,
            'xdd':16,
            'xc0':17,
            'xaf':18,
            'xaa':19,
            'xdfy':20,
            '''xf7}''':21,
            'x8d':22,
            'x99':23,
            'x9e':24

            }
    data['NFC_tag']['Coordinate']=tag_sequence[tag]
    try:
        x = open(logfile,'w')
        json.dump(data, x, indent=4)
        x.close()
        x = open(logfile,'r')
        ret_data=json.load(x)
        x.close()
    except:
        ret_data={'warning':'error while updating logs.json'}
    return ret_data

@app.route('/logs', methods=['GET'])
def get_log():
    x = open(logfile, 'r')
    data=json.load(x)
    x.close()
    return data

# POST endpoint
@app.route('/inputs', methods=['POST'])
def post_data():
    # Retrieve data from the request body
    try:
        input_data = request.get_json()
        x = open(inputsfile, 'w')
        json.dump(input_data, x, indent=4)
        x.close()
        x = open(inputsfile, 'r')
        data = json.load(x)
        x.close()
    except:
        data={}
    # Create a response
    return data

#API to Post the testdat from web-UI
@app.route('/Senddata', methods=['POST'])
def test_data():
    # Retrieve data from the request body
    test_data = request.get_json()
    x = open(test_data_file, 'w')
    json.dump(test_data, x, indent=4)
    x.close()
    x = open(test_data_file, 'r')
    data = json.load(x)
    x.close()
    # Create a response
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
