from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from product_api_service import models
from product_api_service.database.session import create_local_session

confirmMailbp=Blueprint("confirmMail",__name__,url_prefix="/user")


@confirmMailbp.route("/confirmMail/<codeMail>", methods=["POST", "GET"])
def confirmaMail(codeMail):
    if codeMail:
        try:
            with create_local_session() as db_session:
                queryVerifyEmail = select(models.User).where(
                    models.User.email_code == codeMail)
                usuario = db_session.execute(queryVerifyEmail).scalar_one_or_none()
                print(usuario)
                if usuario is None:
                    return {
                        "msg": "No se puede confirmar ese mail"
                }, 404
                else:
                    usuario.email_confirmed = 1
                    db_session.commit()
                    return {
                        "msg": "Correo confirmado exitosamente"
                    }, 200
        except SQLAlchemyError as e:
            print(e)
            return jsonify({"error":"Error en la base de datos"}),500
        except Exception as e:
            print(e)
            return jsonify({"error":"Error interno en el servidor"}),500