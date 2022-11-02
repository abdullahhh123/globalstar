# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerGlobal(models.Model):
    _inherit = 'res.partner'

    contact_person_id = fields.Many2one(comodel_name="res.users", default=lambda self: self.env.user)
    c_r = fields.Char(string="C.R #")
    nickname = fields.Char()
