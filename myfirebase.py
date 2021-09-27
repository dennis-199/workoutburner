import requests
import json
from kivy.app import App

class MyFirebase():
    wak = "AIzaSyBOO8TOW6eHzLiXXOH6nr_tRQmtkI5NtTM" #my web api key
    def sign_up(self, email, password):
        app = App.get_running_app()
        #send email and password to databse
        #firebase return a localid, authToken, refresh token
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
        signup_data = {"email": email, "password": password, "returnSecureToken": True}
        signup_request = requests.post(signup_url, data=signup_data)
        print(signup_request.ok)
        print(signup_request.content.decode())
        sign_up_data = json.loads(signup_request.content.decode())
        if signup_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']

            # save refresh token to a file
            with open("refresh_token.txt", "w") as f:
                f.write(refresh_token)
            # save local id to a variable in main app class
            # save id token to a variable in an app class
            app.local_id= localId
            app.id_token = idToken



            #create new key in database from local id
            #get my friend id
            #default avatar
            #friens list
            #booking / workouts
            my_data = '{"avatar": "man.png", "fiends": "", "workouts": ""}'
            post_request=requests.patch("https://public-transport-3f985-default-rtdb.firebaseio.com/" + localId + ".json?auth=" + idToken,
                                        data=my_data)
            print(post_request.ok)
            print(json.loads(post_request.content.decode()))

            app.change_screen("home_screen")

        if signup_request.ok == False:
            error_data= json.loads(signup_request.content.decode())
            error_message = error_data["error"]['message']
            app.root.ids['login_screen'].ids['login_message'].text = error_message


        pass

    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": %s}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_payload)
        print("REFRESH OK ?", refresh_req.ok)
        print(refresh_req.json())
        id_token = refresh_req.json()['id_token']
        local_id =refresh_req.json()['user_id']

        return id_token, local_id
