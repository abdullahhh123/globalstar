# -*- coding: utf-8 -*-
# from odoo import http


# class ConsigmentProduct(http.Controller):
#     @http.route('/consigment_product/consigment_product', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/consigment_product/consigment_product/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('consigment_product.listing', {
#             'root': '/consigment_product/consigment_product',
#             'objects': http.request.env['consigment_product.consigment_product'].search([]),
#         })

#     @http.route('/consigment_product/consigment_product/objects/<model("consigment_product.consigment_product"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('consigment_product.object', {
#             'object': obj
#         })
