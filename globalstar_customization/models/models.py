# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PartnerGlobal(models.Model):
    _inherit = 'res.partner'

    contact_person_id = fields.Many2one(comodel_name="res.users", default=lambda self: self.env.user)
    c_r = fields.Char(string="C.R #")
    nickname = fields.Char()
    invoice_percentage = fields.Float()


class AccountMoveGlobal(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        super(AccountMoveGlobal, self).action_post()
        debit_disc = self.env['account.account'].search_read([('customer_discount', '=', 'debit')], fields=['id'],
                                                             limit=1)
        credit_disc = self.env['account.account'].search_read([('customer_discount', '=', 'credit')], fields=['id'],
                                                              limit=1)
        if debit_disc and credit_disc:
            for rec in self:
                if rec.move_type == 'out_invoice':
                    if rec.partner_id:
                        if rec.partner_id.invoice_percentage > 0:
                            disc = rec.partner_id.invoice_percentage * rec.amount_total / 100
                            self.env['account.move.line'].create([{
                                'name': _('Customer Discount'),
                                'move_id': rec.id,
                                'account_id': debit_disc[0]['id'],
                                'debit': disc,
                                'credit': 0,
                                'is_partner_disc': True,
                            },
                                {
                                    'name': _('Customer Discount'),
                                    'move_id': rec.id,
                                    'account_id': credit_disc[0]['id'],
                                    'debit': 0,
                                    'credit': disc,
                                    'is_partner_disc': True,
                                }]
                            )

    def button_draft(self):
        super(AccountMoveGlobal, self).button_draft()
        for rec in self:
            if rec.move_type == 'out_invoice':
                rec.line_ids.filtered(lambda l: l.is_partner_disc).unlink()


class AccountMoveLineGlobal(models.Model):
    _inherit = 'account.move.line'

    is_partner_disc = fields.Boolean()


class AccountAccountGlobal(models.Model):
    _inherit = 'account.account'

    customer_discount = fields.Selection(selection=[('debit', 'Debit'), ('credit', 'Credit')])
