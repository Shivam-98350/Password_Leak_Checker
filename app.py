from flask import Flask, render_template, request, jsonify
import requests
import hashlib

app = Flask(__name__)

# Configure the app to serve static files (e.g., videos)
app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    try:
        password = request.json.get('password', '')
        count = pwned_api_check(password)

        return jsonify({'count': count})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'count': -1, 'message': 'Error checking password.'}), 500


# to request out api data
def request_api_data(query_char):
    url='https://api.pwnedpasswords.com/range/'+query_char
    res=requests.get(url)
    if res.status_code !=200:
        raise RuntimeError(f'Error fetching:{res.status_code},check the api and try again')
    return res

# count the number of leak passwords
def get_password_leaks_count(hashes,hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h==hash_to_check:
            return count
    return 0
        
# generate the hash code and get the leak count with the help of above function
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail=sha1password[:5],sha1password[5:]
    response=request_api_data(first5_char)
    print(response)
    return get_password_leaks_count(response,tail)


if __name__ == '__main__':
    app.run(debug=True)
