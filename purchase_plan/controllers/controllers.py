# -*- coding: utf-8 -*-
# from odoo import http


# class PurchasePlan(http.Controller):
#     @http.route('/purchase_plan/purchase_plan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_plan/purchase_plan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_plan.listing', {
#             'root': '/purchase_plan/purchase_plan',
#             'objects': http.request.env['purchase_plan.purchase_plan'].search([]),
#         })

#     @http.route('/purchase_plan/purchase_plan/objects/<model("purchase_plan.purchase_plan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_plan.object', {
#             'object': obj
#         })
