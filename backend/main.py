from copyreg import constructor
import json
import os
import time
from flask_httpauth import HTTPBasicAuth
import jwt
from flask import Flask, jsonify, make_response, request, g
from flask_restful import Resource, Api, reqparse
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin

auth = HTTPBasicAuth()

app = Flask(__name__)
CORS(app, supports_credentials=True)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
print(SECRET_KEY)
app.config['CORS_HEADERS'] = 'Content-type'
app.config['SECRET_KEY'] = SECRET_KEY
api = Api(app)
parser = reqparse.RequestParser()
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="gamenight"
)
cursor = mydb.cursor()

def _build_cors_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

## objekti ki jih vrnejo api - dodane igre, dogodki, skupine, profil
class DodaneIgre(Resource):
    @auth.login_required
    @cross_origin(origin='*')
    def options(self):
        return _build_cors_response()
    def get(self, uporabnisko_ime):
            cursor = mydb.cursor()
            print(uporabnisko_ime)
            cursor.execute("""SELECT * FROM igre WHERE uporabnisko_ime = %s""", [uporabnisko_ime])
            rows = cursor.fetchall()
            r = [dict((cursor.description[i][0], value)
                    for i, value in enumerate(row)) for row in rows]
            print(r)
            cursor.close()
            return json.dumps(r) 



    def post(self,uporabnisko_ime):
            parser = reqparse.RequestParser()  # initialize
            parser.add_argument('ime_igre', required=True)  # add args
            parser.add_argument('min_stevilo_igralcev', required=True)
            parser.add_argument('max_stevilo_igralcev', required=True)
            parser.add_argument('tezavnost', required=True)
            parser.add_argument('dolzina_igre', required=True)
            parser.add_argument('ocena', required=True)
            parser.add_argument('slika_url', required=True)

            request.get_json(force=True)
            args = parser.parse_args()  # parse arguments to dictionary
            print(args)

            dodaj_igro_sql = """INSERT INTO igre(ime_igre, min_stevilo_igralcev, max_stevilo_igralcev, tezavnost,
             dolzina_igre,ocena,slika_url,uporabnisko_ime) 
                                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(dodaj_igro_sql,
                           [args['ime_igre'], args['min_stevilo_igralcev'], args['max_stevilo_igralcev'],
                            args['tezavnost'], args['dolzina_igre'], args['ocena'],args['slika_url'], uporabnisko_ime])
            response = jsonify(message='Igra dodana', id=cursor.lastrowid)
            mydb.commit()
            # response.data = cursor.lastrowid
            response.status_code = 200
            return _corsify_actual_response(response)
       

    def put(self):
        try:
            parser = reqparse.RequestParser()  # initialize

            parser.add_argument('ime_igre', required=True)  # add args
            parser.add_argument('min_stevilo_igralcev', required=True)
            parser.add_argument('max_stevilo_igralcev', required=True)
            parser.add_argument('tezavnost', required=True)
            parser.add_argument('dolzina_igre', required=True)
            parser.add_argument('ocena', required=True)
            parser.add_argument('uporabnisko_ime', required=True)

            request.get_json(force=True)
            args = parser.parse_args()  # parse arguments to dictionary
            print(args)

            posodobi_igro_sql = """UPDATE igre SET min_stevilo_igralcev = %s, max_stevilo_igralcev = %s, tezavnost = %s,
             dolzina_igre= %s,ocena= %s WHERE uporabnisko_ime = %s AND ime_igre = %s"""
            cursor.execute(posodobi_igro_sql,
                           [args['min_stevilo_igralcev'], args['max_stevilo_igralcev'],
                            args['tezavnost'], args['dolzina_igre'], args['ocena'], args['uporabnisko_ime'], args['ime_igre']])
            response = jsonify(message='Igra dodana', id=cursor.lastrowid)
            mydb.commit()
            # response.data = cursor.lastrowid
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
            response = jsonify('Ni dodana igra')
            response.status_code = 400


class DodanaIgra(Resource):
    @auth.login_required
    @cross_origin(origin='*')
    def options(self):
        return _build_cors_response()
    def get(self, id_igre):
        cursor = mydb.cursor()
        try:
            cursor.execute("""select * from igre WHERE ID_igre = %s""", [id_igre])
            rows = cursor.fetchall()
            r = [dict((cursor.description[i][0], value)
                    for i, value in enumerate(row)) for row in rows]
            return json.dumps(r) 
        except Exception as e:
            print(e)


class Uporabniki(Resource):
    # ni še dodano za geslo
    @cross_origin(origin='*')
    def options(self):
        return _build_cors_response()
    def get(self):
        try:
            cursor.execute("""select uporabnisko_ime from uporabnik""")
            rows = cursor.fetchall()
            r = [dict((cursor.description[i][0], value)
                    for i, value in enumerate(row)) for row in rows]
            return json.dumps(r) 
        except Exception as e:
            print(e)


class Uporabnik(Resource):
    # ni še dodano za geslo
    @cross_origin(origin='*')
    def options(self):
        return _build_cors_response()
    def get(self, uporabnisko_ime):
        cursor = mydb.cursor()
        try:
            cursor.execute("""select * from uporabnik WHERE uporabnisko_ime = %s""", [uporabnisko_ime])
            rows = cursor.fetchall()
            r = [dict((cursor.description[i][0], value)
                    for i, value in enumerate(row)) for row in rows]
            cursor.close()
            return json.dumps(r) 
        except Exception as e:
            print(e)

    def post(self):
        request.get_json(force=True)

        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('uporabnisko_ime', required=True)  # add args
        parser.add_argument('geslo', required=True)
        parser.add_argument('ime', required=True)
        parser.add_argument('priimek', required=True)
        parser.add_argument('email', required=True)

        args = parser.parse_args()  # parse arguments to dictionary
        print(args)

        dodaj_uporabnika_sql = """INSERT INTO uporabnik(uporabnisko_ime, geslo, ime, priimek, email) 
                                VALUES(%s, %s, %s, %s, %s)"""
        print(args['geslo'])
        geslo = generate_password_hash(args['geslo'])
        print(geslo)
        cursor.execute(dodaj_uporabnika_sql,
                       [args['uporabnisko_ime'], geslo, args['ime'], args['priimek'],
                        args['email']])
        response = jsonify(message='Uporabnik dodan', id=cursor.lastrowid)
        mydb.commit()
        cursor.close()
        # response.data = cursor.lastrowid
        response.status_code = 200
        return _corsify_actual_response(response)


# skupine ki jih je dodal uporabnik
class Skupine(Resource):
    
    @auth.login_required
    @cross_origin(origin='*')
    def options(self):
        return _build_cors_response()
    def get(self):
        try:
            cursor.execute("""select * from skupine""")
            rows = cursor.fetchall()
            cursor.close()
            return jsonify(rows)
        except Exception as e:
            print(e)

    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('uporabnisko_ime', required=True)  # add args
        parser.add_argument('ime_skupine', required=True)
        parser.add_argument('clani', required=True)

        request.get_json(force=True)
        args = parser.parse_args()  # parse arguments to dictionary
        print(args)

        dodaj_skupino_sql = """INSERT INTO skupine(uporabnisko_ime, ime_skupine, clani) 
                                VALUES(%s, %s, %s)"""
        cursor.execute(dodaj_skupino_sql,
                       [args['uporabnisko_ime'], args['ime_skupine'], args['clani']])
        response = jsonify(message='Skupina dodana', id=cursor.lastrowid)
        mydb.commit()
        # response.data = cursor.lastrowid
        response.status_code = 200
        return response


class Skupina(Resource):
    @auth.login_required
    @cross_origin(origin='*')
    def options(self):
        return _build_cors_response()
    def get(self, uporabnisko_ime, id_skupine):
        try:
            print(type(id_skupine))
            cursor.execute("""select * from skupine WHERE uporabnisko_ime = %s AND id_skupine = %s""", [uporabnisko_ime,
                                                                                                        id_skupine])
            rows = cursor.fetchall()
            cursor.close()
            return jsonify(rows)
        except Exception as e:
            print(e)


# dogodki, ki jih je dodal uporabnik
class Dogodki(Resource):
    @auth.login_required
    @cross_origin(origin='*')
    def options(self):
        return _build_cors_response()
    def get(self, uporabnisko_ime):
        cursor = mydb.cursor()
        try:
            print(type(uporabnisko_ime))
            cursor.execute("""SELECT * FROM dogodek WHERE uporabnisko_ime = %s""", [uporabnisko_ime])
            rows = cursor.fetchall()
            r = [dict((cursor.description[i][0], value)
                    for i, value in enumerate(row)) for row in rows]
            cursor.close()
            return json.dumps(r) 
        except Exception as e:
            print(e)

    def post(self, uporabnisko_ime):

            parser = reqparse.RequestParser()  # initialize

            parser.add_argument('ime_skupine', required=True)
            parser.add_argument('datum', required=True)
            parser.add_argument('odigrana_igra', required=True)
            parser.add_argument('zmagovalec', required=True)

            request.get_json(force=True)
            args = parser.parse_args()  # parse arguments to dictionary
            print(args)

            dodaj_dogodek_sql = """INSERT INTO dogodek(ime_skupine, datum,odigrana_igra, zmagovalec,uporabnisko_ime) 
                                        VALUES(%s, %s, %s,%s, %s)"""
            cursor.execute(dodaj_dogodek_sql,
                           [args['ime_skupine'], args['datum'], args['odigrana_igra'],args['zmagovalec'], uporabnisko_ime])
            response = jsonify(message='Dogodek dodan', id=cursor.lastrowid)
            mydb.commit()
            # response.data = cursor.lastrowid
            response.status_code = 200
            return _corsify_actual_response(response)
    

    def delete(self, uporabnisko_ime):
        try:
            parser = reqparse.RequestParser()  # initialize
            parser.add_argument('id_dogodka', required=True)
            request.get_json(force=True)
            args = parser.parse_args()
            # treba izbrisati še odigrane igre kjer je id_dogodka
            cursor.execute("""delete from dogodek WHERE uporabnisko_ime = %s AND id_dogodka = %s""", [uporabnisko_ime,
                                                                                                      args[
                                                                                                          "id_dogodka"]])
            cursor.execute("""delete from odigrana_igra WHERE uporabnisko_ime = %s AND id_dogodka = %s""",
                           [uporabnisko_ime, args["id_dogodka"]])

            response = jsonify(message='Dogodek izbrisan', id=cursor.lastrowid)
            response.status_code = 200
            mydb.commit()
            return response
        except Exception as e:
            print(e)


class Dogodek(Resource):
    @auth.login_required
    @cross_origin(origin='*')
    def options(self):
        return _build_cors_response()
    def get(self, uporabnisko_ime, id_dogodka):
        cursor = mydb.cursor()
        try:

            cursor.execute("""select * from dogodek WHERE uporabnisko_ime = %s AND id_dogodka = %s""", [uporabnisko_ime,
                                                                                                        id_dogodka])
            rows = cursor.fetchall()
            r = [dict((cursor.description[i][0], value)
                    for i, value in enumerate(row)) for row in rows]
            cursor.close()
            return json.dumps(r) 
        except Exception as e:
            print(e)


class OdigraneIgreIgralec(Resource):
    @auth.login_required
    @cross_origin(origin='*')
    def get(self, uporabnisko_ime, igralec):
        try:

            cursor.execute("""select * from odigrana_igra WHERE uporabnisko_ime = %s AND igralec = %s """,
                           [uporabnisko_ime, igralec
                            ])
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)


class OdigraneIgre(Resource):
    @auth.login_required
    @cross_origin(origin='*')
    def get(self, uporabnisko_ime):
        cursor = mydb.cursor()
        try:
            cursor.execute("""select * from odigrana_igra WHERE uporabnisko_ime = %s """, [uporabnisko_ime])
            rows = cursor.fetchall()
            r = [dict((cursor.description[i][0], value) \
                    for i, value in enumerate(row)) for row in rows]
            return json.dumps(r) 
        except Exception as e:
            print(e)

    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('id_dogodka', required=True)
        parser.add_argument('uporabnisko_ime', required=True)  # add args
        parser.add_argument('igra', required=True)
        parser.add_argument('tocke', required=True)
        parser.add_argument('igralec', required=True)

        request.get_json(force=True)
        args = parser.parse_args()  # parse arguments to dictionary
        print(args)

        dodaj_odigrano_igro_sql = """INSERT INTO odigrana_igra(id_dogodka, uporabnisko_ime,igra, tocke, igralec) 
                                VALUES(%s, %s, %s, %s, %s)"""
        cursor.execute(dodaj_odigrano_igro_sql,
                       [args['id_dogodka'], args['uporabnisko_ime'], args['igra'], args['tocke'], args['igralec']])
        response = jsonify(message='Odigrana igra dodana', id=cursor.lastrowid)
        mydb.commit()
        # response.data = cursor.lastrowid
        response.status_code = 200
        return response

### Avtentikacija
class User:
    username = ""
    password_hash = ""
    def __init__(self, username1, hashPass):  
        self.username = username1
        self.password_hash = hashPass

    @cross_origin(origin='*')   
    def hash_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        print("!!!!!!!!!!!!")
        print(password)
        print(self.password_hash)
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        print("generating token")
        return jwt.encode(
            {'uporabnisko_ime': self.username, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            cursor = mydb.cursor()
            data = jwt.decode(token, options={"verify_signature": False},
                              algorithm='HS256')
            cursor.execute("""SELECT * FROM uporabnik WHERE uporabnisko_ime = %s""", [data['uporabnisko_ime']])
            user = cursor.fetchone()
            cursor.close()
        except:
            return
        return user


@auth.verify_password
def verify_password(username_or_token, password = None):
    # first try token
    print(".............")
    user = User.verify_auth_token(username_or_token)
    print(user)
    if not user:
        cursor = mydb.cursor()
        prijavi_uporabnika_sql = """SELECT * FROM uporabnik WHERE uporabnisko_ime = %s"""
        cursor.execute(prijavi_uporabnika_sql, [username_or_token])
        user1 = cursor.fetchone()
        if user1 == None:
            return print("user does not exist")
        user = User(user1[0], user1[1])
        
        print(username_or_token)
        print(password)
        print(".............")
        print(user.verify_password(password))
        if not user.verify_password(password):
            print("PASSWORD FALSE")
            return False
    cursor.close()
    g.user = user if user else  print("User does not exist")
    return True


class Login(Resource):
    @auth.login_required
    @cross_origin(supports_credentials=True, origins='*')
    def get(self):
        token = User.generate_auth_token(g.user, 600)
        return jsonify({'token': token, 'duration': 600})


api.add_resource(Uporabniki, '/api/uporabniki', endpoint='uporabniki')
api.add_resource(Uporabnik, '/api/uporabnik/<string:uporabnisko_ime>', endpoint='uporabnik')
api.add_resource(Skupine, '/api/skupine', endpoint='skupine')
api.add_resource(Skupina, '/api/skupine/<string:uporabnisko_ime>/<int:id_skupine>', endpoint='skupina')
api.add_resource(Dogodek, '/api/dogodki/<string:uporabnisko_ime>/<int:id_dogodka>', endpoint='dogodek')
api.add_resource(Dogodki, '/api/dogodki/<string:uporabnisko_ime>', endpoint='dogodki')
api.add_resource(DodaneIgre, '/api/igre/<string:uporabnisko_ime>', endpoint='igre')
api.add_resource(DodanaIgra, '/api/igre/<int:id_igre>', endpoint='igra')
api.add_resource(OdigraneIgreIgralec, '/api/odigraneigre/<string:uporabnisko_ime>/<string:igralec>',
                 endpoint='odigrana_igra')
api.add_resource(OdigraneIgre, '/api/odigraneigre/<string:uporabnisko_ime>', endpoint='odigrane_igre')
api.add_resource(Login, '/api/login', endpoint='login')
api.add_resource(Uporabnik, '/api/registracija', endpoint='registracija')

if __name__ == "__main__":
    app.run(debug=True)
