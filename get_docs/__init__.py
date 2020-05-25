import logging
from .PyAzStorage import az_storage
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    #name = req.params.get('name')
    db_op = ''
    if not db_op:
        try:
            logging.info('Getting body from json')
            req_body = req.get_json()
        except ValueError:
                pass
        else:
            logging.info('Sending body to az storage')
            payload = az_storage(req_body)

    if payload:
        return func.HttpResponse(f'{payload}')
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
