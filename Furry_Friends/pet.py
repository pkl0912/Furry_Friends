from flask import request, jsonify, session, Blueprint, url_for, redirect
from werkzeug.utils import secure_filename
import os
from sqlalchemy import and_
import boto3
import json


from connect_db import db
from models import User, Animal
from config import AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_REGION, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, ALLOWED_EXTENSIONS


bp = Blueprint("pet", __name__, url_prefix="/pet")


# s3 클라이언트 생성
def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name=AWS_S3_BUCKET_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        return s3

    except Exception as e:
        print(e)
        print('ERROR_S3_CONNECTION_FAILED') 


def query_to_dict(objs):
    try:
        lst = [obj.__dict__ for obj in objs]
        for obj in lst:
            del obj['_sa_instance_state']
        return lst
    except TypeError: # non-iterable
        if objs == None:
            return []
        objs = objs.__dict__
        del objs['_sa_instance_state']
        lst = [objs]
        return lst


def upload_file_to_s3(file):
    filename = secure_filename(file.filename)
    s3.upload_fileobj(
            file,
            AWS_S3_BUCKET_NAME,
            file.filename
    )

    return file.filename


s3 = s3_connection()


@bp.route('/management', methods=['GET'])
def management():

    if 'login' in session:

        # 해당 아이디로 등록한 동물 전부
        animal_list = Animal.query.filter(Animal.user_id==session['login']).all()
        animal_list = query_to_dict(animal_list)

        # 등록한 동물이 없음
        if animal_list == []:
            return "no animal registered"
        
        # 등록한 동물이 있음
        else:
            return jsonify(animal_list)

    else:
        "unauthorized"


@bp.route('/profile', methods=["GET"])
def profile():
    # 로그인 o
    if 'login' in session:

        # 유저에게 등록된 동물들 id에 헤더로 받은 동물 id가 포함되어 있는지 확인
        # 있으면 헤더로 받은 동물 세션에 저장, 동물 정보 json 반환
        animals = Animal.query.filter_by(user_id = session['login']).all()
        animal_id = int(request.headers['animal_id'])

        ids = [animal.animal_id for animal in animals]

        if animal_id in ids:
            session['curr_animal'] = animal_id
            curr_animal = Animal.query.get(animal_id)
            curr_animal = query_to_dict(curr_animal)

            return jsonify(curr_animal)

        else:
            return "wrong request"

    # 로그인 x
    else:
        return "not logged in"


    #     # 관리할 동물 header와 일치 시
    #     if session['curr_animal'] == animal_id:
    #         animal = Animal.query.filter_by(animal_id = session['curr_animal']).first()
    #         animal = query_to_dict(animal)
    #         return jsonify(animal)
        
    #     # 관리할 동물 교체 시
    #     else:
    #         session['curr_animal'] = animal_id
    #         animal = Animal.query.filter_by(animal_id = session['curr_animal']).first()
    #         animal = query_to_dict(animal)
    #         return jsonify(animal)

    # # 세션에 관리할 동물 x
    # else:
    #     try:
    #     # header로 animal_id 받으면 프로필
    #         session['curr_animal'] = animal_id
    #         animal = query_to_dict(Animal.query.filter_by(animal_id = session['curr_animal']).first())
    #         return jsonify(animal)

    #     except:   
    #         # header로 온 게 없으면 동물 관리 화면
    #         animal_list = query_to_dict(Animal.query.filter_by(user_id = session['login']).all())

    #         return jsonify(animal_list)


@bp.route('/update', methods=["GET","PUT"])
def info_update():

    # 수정할 동물 id header로 받음
    animal_id = request.headers['animal_id']

    # 세션과 일치 시
    if session['curr_animal'] == animal_id:

        # 동물 정보 수정 페이지 접근
        if request.method == "GET":
            animal = Animal.query.filter_by(animal_id = session['curr_animal']).first()

            animal = query_to_dict(animal)
            return jsonify(animal)  

        # 수정 정보 전달 시
        # 수정사항 한번에 전송받음
        else: # PUT
            animal = Animal.query.filter_by(animal_id = session['curr_animal']).first()

            # 새로 이미지 업로드
            try:
                f = request.files['file']

                changes = request.form
                changes = json.loads(changes['data'])

                animal.animal_name = changes['animal_name']
                animal.bday = changes['bday']
                animal.sex = changes['sex']
                animal.neutered = changes['neutered']
                animal.weight = changes['weight']

                # 기존의 이미지 s3에서 삭제
                try:
                    s3.delete_object(
                        Bucket = AWS_S3_BUCKET_NAME,
                        Key = (animal.image).split('/')[-1]
                    )

                # 기존에 이미지가 없었던 경우 -- pass
                except: 
                    pass

                extension = f.filename.split('.')[-1]
                if extension in ALLOWED_EXTENSIONS:
                    extension = '.' + extension

                    newname = session['login'] + '_' + animal.animal_name + extension
                    img_url = f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_S3_BUCKET_REGION}.amazonaws.com/{newname}"
                    f.filename = newname

                    upload_file_to_s3(f)

                    animal.image = img_url

                # 업로드된 파일이 이미지 파일이 아님
                else:
                    return "wrong file extension"

            # 이미지 업로드 x
            # 이미지 삭제 시에는?
            except:
                changes = request.get_json()

                animal.animal_name = changes['animal_name']
                animal.bday = changes['bday']
                animal.sex = changes['sex']
                animal.neutered = changes['neutered']
                animal.weight = changes['weight']

            db.session.commit()

            return "successfully updated"
    else:
        return "unauthorized"


@bp.route('/delete', methods=["DELETE"])
def pet_delete():
    
    # 삭제할 동물 id header로 받음
    animal_id = request.headers['animal_id']

    # 세션에 동물과 일치 시
    if session['curr_animal'] == animal_id:
        try:
            animal = Animal.query.filter_by(animal_id = session['curr_animal']).first()

            # 프로필 이미지 s3에서 삭제
            try:
                s3.delete_object(
                    Bucket = AWS_S3_BUCKET_NAME,
                    Key = (animal.image).split('/')[-1]
                )

            # 기존에 이미지가 없었던 경우 -- pass
            except: 
                pass

            # db에서 animal 삭제
            db.session.delete(animal)
            db.session.commit()
            return "successfully removed"

        except:
            return "removal failed"
    
    else:
        return "unauthorized"
