import requests
from flask import Flask, request, jsonify

app=Flask(__name__)

@app.route('/byname', methods=['POST'])
def classify_galaxy():
    # Retrieve the name from the request
    name = request.form.get('name')
    name='Andromeda'
    name=name.lower()
    name1=name[0].upper()+name[1:]
    # Perform your logic to search in the JSON and return the response
    info='sources.txt'
    files=[]
    photo=[]
    with open (info,'r',encoding='utf=8') as f:
        jsoninfo=f.readlines()
    for info in jsoninfo:
        try:
            if '.json' in info:
                files.append(requests.get(info.partition('\n')[0]).content)
            elif 'small' in info:
                photo.append(info)
        except Exception as e:
            print(e)
    i=0
    for file in files:
        if name in file:
            photo_url=photo[i]
            galaxy_data=file
        i+=1
     
    # Return the response as JSON
    return jsonify({"photo": photo_url, "data": galaxy_data})