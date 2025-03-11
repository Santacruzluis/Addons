# -*- coding: utf-8 -*-
# from odoo import http


# class CustomAccountFormat(http.Controller):
#     @http.route('/custom_account_format/custom_account_format', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_account_format/custom_account_format/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_account_format.listing', {
#             'root': '/custom_account_format/custom_account_format',
#             'objects': http.request.env['custom_account_format.custom_account_format'].search([]),
#         })

#     @http.route('/custom_account_format/custom_account_format/objects/<model("custom_account_format.custom_account_format"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_account_format.object', {
#             'object': obj
#         })

