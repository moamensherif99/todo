import json
import math
from idlelib.rpc import response_queue
from urllib.parse import parse_qs

from PIL.ImageChops import offset
from odoo import http
from odoo.http import request
from xlwt import Borders


def valid_response(data, status, pagination_info=None):
    response_body = {
        'message': 'success',
        'data': data,
    }
    if pagination_info:
        response_body['pagination_info'] = pagination_info
    return request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {
        'error': error,
    }
    return request.make_json_response(response_body, status=status)


class ToDoApi(http.Controller):
    @http.route("/v1/todo", type='http', auth='none', methods=['POST'], csrf=False)
    def post_todo(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        res = request.env['todo.task'].sudo().create(vals)
        if res:
            return valid_response(
                {
                    'message': 'ToDo Task Created Successfully'
                }, status=200
            )

    @http.route("/v1/todo/<int:todo_id>", type='http', auth='none', methods=['PUT'], csrf=False)
    def put_todo(self, todo_id):
        try:
            todo_id = request.env['todo.task'].sudo().search([('id', '=', todo_id)])
            if not todo_id:
                return invalid_response(
                    {
                        'error': 'ToDo not found',
                    }, status=400
                )
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            todo_id.write(vals)
            return valid_response(
                {
                    'message': 'ToDo Task Updated Successfully',
                    'id': todo_id.id,
                    'name': todo_id.name,
                }, status=200
            )
        except Exception as erorr:
            return invalid_response(
                {
                    'error': 'Error updating ToDo',
                }, status=400
            )

    @http.route("/v1/todo/<int:todo_id>", type='http', auth='none', methods=['GET'], csrf=False)
    def get_todo(self, todo_id):
        try:
            todo_id = request.env['todo.task'].sudo().search([('id', '=', todo_id)])
            if not todo_id:
                return request.make_json_response(
                    {
                        'error': 'ToDo Task not found',
                    }, status=400)
            return valid_response(
                {
                    'id': todo_id.id,
                    'name': todo_id.name,
                    'ref': todo_id.ref,
                    'description': todo_id.description,
                    'assign_to_id': todo_id.assign_to_id,
                    'due_date': todo_id.due_date,
                    'status': todo_id.status,
                    'estimated_time': todo_id.estimated_time,
                }, status=200
            )
        except Exception as erorr:
            print(erorr)
            return invalid_response(
                {
                    'error': 'Error Updating Todo Task',
                }, status=400
            )

    @http.route("/v1/todo/<int:todo_id>", type='http', auth='none', methods=['DELETE'], csrf=False)
    def delete_todo(self, todo_id):
        try:
            todo_id = request.env['todo.task'].sudo().search([('id', '=', todo_id)])
            if not todo_id:
                return invalid_response(
                    {
                        'error': 'todo not found',
                    }, status=400)
            todo_id.unlink()
            return valid_response(
                {
                    'message': 'todo deleted successfully',
                }, status=200
            )

        except Exception as erorr:
            print(erorr)
            return invalid_response(
                {
                    'error': 'Error updating todo',
                }, status=400
            )

    @http.route("/v1/todos", type='http', auth='none', methods=['GET'], csrf=False)
    def get_todo_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            todo_domain = []
            page = offset = None
            limit = 10  # Default limit
            if params:
                if params.get('limit'):
                    limit = int((params.get('limit')[0]))
                if params.get('page'):
                    page = int((params.get('page')[0]))

            if page:
                offset = (page * limit) - limit
            if params.get('state'):
                todo_domain += [('state', '=', params.get('state')[0])]
            todo_ids = request.env['todo.task'].sudo().search(todo_domain, offset=offset, limit=limit)
            todo_ccount = request.env['todo.task'].sudo().search_count(todo_domain)
            if not todo_ids:
                return invalid_response(
                    {
                        'error': 'todo not found',
                    }, status=400)
            return valid_response([
                {
                    'id': todo_id.id,
                    'name': todo_id.name,
                    'ref': todo_id.ref,
                    'description': todo_id.description,
                    'assign_to_id': todo_id.assign_to_id,
                    'due_date': todo_id.due_date,
                    'status': todo_id.status,
                    'estimated_time': todo_id.estimated_time,
                } for todo_id in todo_ids],
                status=200,
                pagination_info={
                    'page': page if page else 1,
                    'limit': limit,
                    'pages': math.ceil(todo_ccount / limit) if limit else 1,
                    'count': todo_ccount
                },

            )
        except Exception as erorr:
            print(erorr)
            return invalid_response(
                {
                    'error': 'Error updating todo',
                }, status=400
            )