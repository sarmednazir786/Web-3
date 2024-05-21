import yaml
import base64
from werkzeug.utils import secure_filename
from distutils.log import debug 
from fileinput import filename 
from flask import *
import re
import json
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def start_again():
 return render_template('index.html')

@app.route("/home", methods=["GET"])
def start():
 return render_template('index.html')

@app.route('/success/subscribed')
def success():
 return render_template('subscribed.html', sites=sanitized_value)
#	return 'Hello %s' % sanitized_value
	
@app.route('/login', methods=['POST', 'GET'])

def login():
 if request.method == 'POST':
  global value
  global sanitized_value
  value = request.form['nm']
  sanitized_value = value.replace('<script>', '').replace('</script>', '')
  return redirect(url_for('success'))
 else:
  user = request.args.get('nm')
  return redirect (url_for('success'))
			
@app.route('/file-upload')
def file():
  return render_template('file_upload.html')

app.config['upload_folder'] = ''  
ALLOWED_EXTENSIONS = {'yaml', 'json', 'txt'}

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

uploaded_files = []

@app.route('/upload', methods=['POST'])
def upload_file():
  if request.method == 'POST': 
    f = request.files['file'] 
    if f and allowed_file(f.filename):
      f.save(f.filename)
      uploaded_files.append(f.filename)
      return render_template('file_upload_success.html') 
    return render_template('file_upload_failed.html')

@app.route('/uploaded-files', methods=['GET'])
def show_uploaded_files():
  if request.method == 'GET':
    file_links = [(file, url_for('uploaded_file', filename=file)) for file in uploaded_files]
    return render_template('uploaded_files.html', file_links=file_links)

@app.route('/uploaded-files/<filename>')
def uploaded_file(filename):
      file_path = f'{filename}'
      if request.method == 'GET':
        statement = ""
        with open(file_path, "r") as file:
          for line in file.readlines():
            statement += line
        with open(filename, "r") as in_fh:
          config = in_fh.read()
          config_dict = dict()
          valid_b64 = True
          valid_json = True
          valid_yaml = True
          
          if re.match("^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$", config):
            base64_bytes = config.encode("ascii") 

            stri_bytes = base64.b64decode(base64_bytes)
            stri_fnl = stri_bytes.decode("ascii")

            try:
              config_dict = json.loads(stri_fnl)
            except:
              print ("Error trying to load the config file in JSON format")
              valid_json = False

            try:
              config_dict = yaml.load(stri_fnl)
            except:
              print ("Error trying to load the config file in YAML format")
              valid_yaml = False

            print ("Base64 encoded")

          else:
            valid_b64 = False
            print ("Not encoded in Base64")

          try:
            config_dict = json.loads(config)
          except:
            print ("Error trying to load the config file in JSON format")
            valid_json = False

          try:
            config_dict = yaml.safe_load(config)
          except:
            print ("Error trying to load the config file in YAML format")
            valid_yaml = False
          

      return render_template('view_raw_content.html', content=statement, isjson=valid_json, isyaml=valid_yaml, isb64=valid_b64)
  
@app.route('/view/', methods=['GET'])
def select_file():
  return render_template('view_file.html')

@app.route('/view/<filename>', methods=['GET'])
def view_file(filename):
      file_path = f'{filename}'
      if request.method == 'GET':
        statement = ""
        with open(file_path, "r") as file:
          for line in file.readlines():
            statement += line
        with open(filename, "r") as in_fh:
          config = in_fh.read()
          config_dict = dict()
          valid_json = True
          valid_yaml = True

          try:
            config_dict = json.loads(config)
          except:
            print ("Error trying to load the config file in JSON format")
            valid_json = False

          try:
            config_dict = yaml.load(config)
          except:
            print ("Error trying to load the config file in YAML format")
            valid_yaml = False
          
          print ("JSON: " + str(valid_json))
          print ("YAML: " + str(valid_yaml))

      return render_template('view_raw_content.html', content=statement, isjson=valid_json, isyaml=valid_yaml)


      
      # return yaml.load(statement)

  # if 'file' in request.files:
  #   file = request.files['file']
  #   if file and allowed_file(file.filename):
  #     filename = secure_filename(file.filename)
  #     return 'File uploaded successfully'
  # for line in request.files.get('file'):
  #   print(line)    
  # return 'No file found'

@app.route("/robots.txt", methods=["GET"])
def robots_txt():
    return send_from_directory('static', 'robots.txt')

@app.route("/vulnerability", methods=["GET"])
def vulnerability():
    data = json.loads(str(request.args.to_dict()).replace("'", '"'))
    data = data.get("url") if data.get("url") else "http://0.0.0.0:8083/robots.txt"
    if data == "http://127.0.0.1:8083/":
      dirname = f"{os.getcwd()}/templates/"
      filename = os.path.basename("git.zip")
      return send_from_directory(dirname, filename)
    try:
        return requests.get(data).text
    except:
        return "http://0.0.0.0:8083/robots.txt"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8083)
