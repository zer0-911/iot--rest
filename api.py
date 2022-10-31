from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd
import sqlConnector


app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)


class ESP(Resource):
    def get(self):
        data = sqlConnector.getTodayData()
        data = pd.DataFrame(data, columns=["ID", "Date", "Temp"])
        data["Date"] = data["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('temperature', type=float,
                            required=True, location='args')
        args = parser.parse_args()
        new_data = pd.DataFrame({
            'temperature': [args['temperature']],
        })
        sqlConnector.postData(float(args['temperature']))
        return {'data': new_data.to_dict('records')}, 201


# Add URL endpoints
api.add_resource(ESP, '/esp')

if __name__ == '__main__':
    app.run()
