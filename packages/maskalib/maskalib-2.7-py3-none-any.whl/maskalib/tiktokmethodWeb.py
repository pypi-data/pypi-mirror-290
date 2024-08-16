from flask import Flask, request, render_template_string, jsonify
import hashlib
import json
from time import time
from random import randint, choice
import requests
from copy import deepcopy
from urllib.parse import quote
import os
from colorama import Fore, init  
import tkinter as tk
from tkinter import messagebox
import random

invisible_chars = [
    '\u200B',  # Zero-width space
    '\u200C',  # Zero-width non-joiner
    '\u200D',  # Zero-width joiner
    '\u2060',  # Word joiner
    '\u2061',  # Function application
    '\u2062',  # Invisible times
    '\u2063',  # Invisible separator
    '\uFEFF',  # Zero-width no-break space
    '\u034F',  # Combining grapheme joiner
]


def make_username_unique(username):
    num_invisibles = random.randint(3, 10)

    unique_suffix = ''.join(random.choice(invisible_chars) for _ in range(num_invisibles))

    if random.choice([True, False]):
        unique_suffix = unique_suffix[:len(unique_suffix)//2] + ''.join(random.choice(invisible_chars) for _ in range(num_invisibles))
    
    insertion_point = random.randint(0, len(username))
    unique_username = username[:insertion_point] + unique_suffix + username[insertion_point:]
    
    return unique_username

def hex_string(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return tmp_string

def RBIT(num):
    result = ''
    tmp_string = bin(num)[2:]
    while len(tmp_string) < 8:
        tmp_string = '0' + tmp_string
    for i in range(0, 8):
        result = result + tmp_string[7 - i]
    return int(result, 2)

def file_data(path):
    with open(path, 'rb') as f:
        result = f.read()
    return result

def reverse(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return int(tmp_string[1:] + tmp_string[:1], 16)


class XG:
    def __init__(self, debug):
        self.length = 0x14
        self.debug = debug
        self.hex_CE0 = [0x05, 0x00, 0x50, choice(range(0, 0xFF)), 0x47, 0x1e, 0x00, choice(range(0, 0xFF)) & 0xf0]

    def addr_BA8(self):
        tmp = ''
        hex_BA8 = []
        for i in range(0x0, 0x100):
            hex_BA8.append(i)
        for i in range(0, 0x100):
            if i == 0:
                A = 0
            elif tmp:
                A = tmp
            else:
                A = hex_BA8[i - 1]
            B = self.hex_CE0[i % 0x8]
            if A == 0x05:
                if i != 1:
                    if tmp != 0x05:
                        A = 0
            C = A + i + B
            while C >= 0x100:
                C = C - 0x100
            if C < i:
                tmp = C
            else:
                tmp = ''
            D = hex_BA8[C]
            hex_BA8[i] = D
        return hex_BA8

    def initial(self, debug, hex_BA8):
        tmp_add = []
        tmp_hex = deepcopy(hex_BA8)
        for i in range(self.length):
            A = debug[i]
            if not tmp_add:
                B = 0
            else:
                B = tmp_add[-1]
            C = hex_BA8[i + 1] + B
            while C >= 0x100:
                C = C - 0x100
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = D + D
            while E >= 0x100:
                E = E - 0x100
            F = tmp_hex[E]
            G = A ^ F
            debug[i] = G
        return debug

    def calculate(self, debug):
        for i in range(self.length):
            A = debug[i]
            B = reverse(A)
            C = debug[(i + 1) % self.length]
            D = B ^ C
            E = RBIT(D)
            F = E ^ self.length
            G = ~F
            while G < 0:
                G += 0x100000000
            H = int(hex(G)[-2:], 16)
            debug[i] = H
        return debug

    def main(self):
        result = ''
        for item in self.calculate(self.initial(self.debug, self.addr_BA8())):
            result = result + hex_string(item)

        return '8404{}{}{}{}{}'.format(hex_string(self.hex_CE0[7]), hex_string(self.hex_CE0[3]),
                                       hex_string(self.hex_CE0[1]), hex_string(self.hex_CE0[6]), result)


def X_Gorgon(param, data, cookie):
    gorgon = []
    ttime = time()
    Khronos = hex(int(ttime))[2:]
    url_md5 = hashlib.md5(bytearray(param, 'utf-8')).hexdigest()
    for i in range(0, 4):
        gorgon.append(int(url_md5[2 * i: 2 * i + 2], 16))
    if data:
        if isinstance(data, str):
            data = data.encode(encoding='utf-8')
        data_md5 = hashlib.md5(data).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(data_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    if cookie:
        cookie_md5 = hashlib.md5(bytearray(cookie, 'utf-8')).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(cookie_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    gorgon = gorgon + [0x1, 0x1, 0x2, 0x4]
    for i in range(0, 4):
        gorgon.append(int(Khronos[2 * i: 2 * i + 2], 16))
    return {'X-Gorgon': XG(gorgon).main(), 'X-Khronos': str(int(ttime))}


def get_stub(data):
    if isinstance(data, dict):
        data = json.dumps(data)

    if isinstance(data, str):
        data = data.encode(encoding='utf-8')
    if data is None or data == "" or len(data) == 0:
        return "00000000000000000000000000000000"

    m = hashlib.md5()
    m.update(data)
    res = m.hexdigest()
    res = res.upper()
    return res

def check_is_changed(last_username, session_id, device_id, iid):
    """Check if the username has been changed in the TikTok profile."""
    return get_profile(session_id, device_id, iid) != last_username


def change_username(session_id, device_id, iid, last_username, new_username):
    """Attempt to change a TikTok username."""
    data = f"aid=364225&unique_id={quote(new_username)}"
    parm = f"aid=364225&residence=&device_id={device_id}&version_name=1.1.0&os_version=17.4.1&iid={iid}&app_name=tiktok_snail&locale=en&ac=4G&sys_region=SA&version_code=1.1.0&channel=App%20Store&op_region=SA&os_api=18&device_brand=iPad&idfv=16045E07-1ED5-4350-9318-77A1469C0B89&device_platform=iPad&device_type=iPad13,4&carrier_region1=&tz_name=Asia/Riyadh&account_region=&tz_offset=10800"
    headers = {
        "Host": "api.tiktokv.com",
        "Connection": "keep-alive",
        "sdk-version": "2",
        "x-tt-token": "00000000000000000000000000000000",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "com.zhiliaoapp.musically/202100 (Linux; U; Android 8; en_US; samsung; SM-G930T; samsung; sm; en_US; tt-ok/1.1.0.0)",
        "Cookie": f"sessionid={session_id}",
        "Accept-Encoding": "gzip, deflate",
    }
    url = f"https://api.tiktokv.com/aweme/v1/commit/user/?{parm}"

    X_Gon = X_Gorgon(parm, data, f'sessionid={session_id}')
    response = requests.post(url, data=data, headers={**headers, **X_Gon})
    if check_is_changed(last_username, session_id, device_id, iid):
        return "Your name got Changed! gg!"
    else:
        return f"Didn't work, error code: {response.json()}"

init(autoreset=True)

def get_profile(session_id, device_id, iid):
    """Retrieve the current TikTok username for a given session, device, and iid."""
    try:
        data = None
        parm = (
            f"device_id={device_id}&iid={iid}&id=kaa&version_code=34.0.0&language=en"
            "&app_name=lite&app_version=34.0.0&carrier_region=SA&tz_offset=10800&mcc_mnc=42001"
            "&locale=en&sys_region=SA&aid=473824&screen_width=1284&os_api=18&ac=WIFI&os_version=17.3"
            "&app_language=en&tz_name=Asia/Riyadh&carrier_region1=SA&build_number=340002&device_platform=iphone"
            "&device_type=iPhone13,4"
        )
        url = f"https://api16.tiktokv.com/aweme/v1/user/profile/self/?{parm}"
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={session_id}",
            "sdk-version": "2",
            "user-agent": "com.zhiliaoapp.musically/432424234 (Linux; U; Android 5; en; fewfwdw; Build/PI;tt-ok/3.12.13.1)",
        }
        response = requests.get(url, headers=headers, cookies={"sessionid": session_id})
        return response.json()
    except Exception as e:
        return "None"
    
app = Flask(__name__)

# Mock data for demonstration purposes
users_data = {

}

def Discordmethod(username):
    method1 = random.randint(1, 3)
    numberrandom = str(random.randint(1,100))
    if method1 == 1:
        newusername = f"{username}                                                 {numberrandom}"
    elif method1 == 2:
        newusername = f"{username}                                                {numberrandom}"
    elif method1 == 3:
        newusername = f"{username}                                                  {numberrandom}"
    return newusername

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Profile</title>
    <style>
        body {
            background-color: #0D0D0D;
        }
        p {
            color: #FFFFFF;
    -webkit-text-stroke-width: 0.5px;
    -webkit-text-stroke-color: var(--Primary-Color, #FFF);
    font-family: serif;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
    font-size: 2vw;
        }
        h1 {
            color: #FFFFFF;
        }
                 
        .profile-pic {
            border-radius: 50%;
            width: 150px;
            height: 150px;
        }
        .edit-profile {
            margin-top: 20px;
        }
                                  form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 350px;
  padding: 20px;
  border-radius: 20px;
  position: relative;
  background-color: #1a1a1a;
  color: #fff;
  border: 1px solid #333;
}
.input1 {
  background-color: #333;
  color: #fff;
  width: 96%;
  padding: 20px 05px 05px 05px;
  outline: 0;
  border: 1px solid rgba(105, 105, 105, 0.397);
  border-radius: 10px;
}


.input1 {
  font-size: medium;
}

.button1 {
  border: none;
  outline: none;
  padding: 10px;
  border-radius: 10px;
  color: #fff;
  font-size: 16px;
  transform: .3s ease;
  background-color: #00bfff;
}

.button1:hover {
  background-color: #00bfff96;
}

@keyframes pulse {
  from {
    transform: scale(0.9);
    opacity: 1;
  }

  to {
    transform: scale(1.8);
    opacity: 0;
  }
}
    </style>
</head>
<body>
    <form id="session-form">
        <input class="input1" type="text" id="session-id" name="session_id" placeholder="Enter Session ID" required>
        <button class="button1" type="button" onclick="getUserProfile()">Submit</button>
    </form>
    <div id="profile-container" style="display: none;">
        <p><strong>SessionID:</strong> <span id="profile-session-id"></span></p>
        <p><strong>Username:</strong> <span id="profile-username"></span></p>
        <p><strong>DisplayName:</strong> <span id="profile-displayname"></span></p>
        <img id="profile-pic" alt="Profile Picture" class="profile-pic">
        <div class="edit-profile">
            <h2>Edit Profile</h2>
            <input type="text" id="profile-input" placeholder="Enter text">
            <button onclick="sendInput('Button 1')">Normal Changer (normal name)</button>
            <button onclick="sendInput('Button 2')">Maska Method (get any name but can take more times)</button>
            <button onclick="sendInput('Button 3')">Discord method (watch a tuto on ytb: MaskaOffi)</button>
            <p id="response-output"></p>
        </div>
        <p><strong>Followers:</strong> <span id="profile-followers"></span></p>
        <p><strong>Following:</strong> <span id="profile-following"></span></p>
        <p><strong>Friends:</strong> <span id="profile-friends"></span></p>
        <p><strong>Email:</strong> <span id="profile-email"></span></p>
        <p><strong>Share URL:</strong> <a id="profile-shareurl" href="" target="_blank"></a></p>
    </div>
    <script>
        function getUserProfile() {
            const sessionId = document.getElementById('session-id').value;
            fetch(`/api/user/${sessionId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        document.getElementById('profile-session-id').textContent = sessionId;
                        document.getElementById('profile-username').textContent = data.Username;
                        document.getElementById('profile-displayname').textContent = data.DisplayName;
                        document.getElementById('profile-pic').src = data.ProfilePicture;
                        document.getElementById('profile-followers').textContent = data.Followers;
                        document.getElementById('profile-following').textContent = data.Following;
                        document.getElementById('profile-friends').textContent = data.Friends;
                        document.getElementById('profile-email').textContent = data.email;
                        document.getElementById('profile-shareurl').href = data.ShareUrl;
                        document.getElementById('profile-shareurl').textContent = data.ShareUrl;
                        document.getElementById('profile-container').style.display = 'block';
                    }
                })
                .catch(error => alert('Error fetching user profile'));
        }

        function sendInput(buttonName) {
            const text = document.getElementById('profile-input').value;
            const sessionID = document.getElementById('profile-session-id').textContent;
            const user = document.getElementById('profile-username').textContent;
            fetch(`/api/print_input`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ button: buttonName, input: text, session_id: sessionID, user: user })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('response-output').textContent = data.message;
            })
            .catch(error => alert('Error sending input'));
        }
    </script>
</body>
</html>
''')

@app.route('/api/user/<session_id>', methods=['GET'])
def api_user(session_id):
    device_id = str(randint(777777788, 999999999999))
    iid = str(randint(777777788, 999999999999))
    infos = get_profile(session_id, device_id, iid)
    users_data = {
            f"{session_id}": {
                "Username": infos["user"]["unique_id"],
                "DisplayName": infos["user"]["nickname"],
                "ProfilePicture": infos["user"]["avatar_larger"]["url_list"][0],
                "Followers": infos["user"]["follower_count"],
                "Following": infos["user"]["following_count"],
                "Friends": infos["user"]["friend_count"],
                "email": infos["user"]["email"],
                "ShareUrl": infos["user"]["share_info"]["share_url"],

            }
        }
    user_data1 = users_data.get(session_id)
    if user_data1:
        return jsonify(user_data1)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/print_input', methods=['POST'])
def print_input():
    data = request.json
    button_name = data.get('button')
    input_text = data.get('input')
    session_id = (data.get('session_id'))
    user = data.get('user')
    print(f"{button_name}: {input_text}")
    device_id = str(randint(777777788, 999999999999))
    iid = str(randint(777777788, 999999999999))
    new_username = input_text
    MaskaUsername = make_username_unique(new_username)
    Discordmethod1 = Discordmethod(new_username)
    if button_name == "Button 1":
        print(user)
        print(session_id)
        result = change_username(session_id, device_id, iid, user, new_username)
    elif button_name == "Button 2":
        result = change_username(session_id, device_id, iid, user, MaskaUsername)
    elif button_name == "Button 3":
        result = change_username(session_id, device_id, iid, user, Discordmethod1)
    return jsonify({"message": f"{result}"})

if __name__ == '__main__':
    app.run(debug=True)