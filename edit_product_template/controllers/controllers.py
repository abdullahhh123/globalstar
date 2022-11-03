# -*- coding: utf-8 -*-
# from odoo import http


# class EditProductTemplate(http.Controller):
#     @http.route('/edit_product_template/edit_product_template', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_product_template/edit_product_template/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_product_template.listing', {
#             'root': '/edit_product_template/edit_product_template',
#             'objects': http.request.env['edit_product_template.edit_product_template'].search([]),
#         })

#     @http.route('/edit_product_template/edit_product_template/objects/<model("edit_product_template.edit_product_template"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_product_template.object', {
#             'object': obj
#         })
