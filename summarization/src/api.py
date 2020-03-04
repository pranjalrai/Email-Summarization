try:
  from flask import Flask, request
  from flask_restful import Resource, Api
  from flasgger import Swagger
  from flasgger.utils import swag_from
  from flask_restful_swagger import swagger
  from mail_auth import *
  import time

except Exception as e:
  print('modules missing: {}'.format(e))

app = Flask(__name__)
api = Api(app)


api = swagger.docs(Api(app), apiVersion=0.1, api_spec_url='/docs')


class EmailSummarization(Resource):

  @swagger.model
  @swagger.operation(notes='some notes')
  def get(self):
    return {
      'Response': 200
    }

  @swagger.model
  @swagger.operation(notes='some notes')
  def delete(self):
    return {
      'Error': 'This facility is not live yet',
    }

  @swagger.model
  @swagger.operation(notes='some notes')
  def post(self, mail_id, password, no_of_mails):
    get_mail_details(mail_id, password, no_of_mails)  # give the password: app specific password in this case
    return {
      # mail_id: mail_id,
      # password: password
      'Response': 200,
      'Message': 'Success, Csv File Created with the details of the mails of mail id {}'.format(mail_id)
    }


api.add_resource(EmailSummarization, '/email-sum/<string:mail_id>/<string:password>/<int:no_of_mails>')


if __name__ == "__main__":
  app.run(debug=True)
