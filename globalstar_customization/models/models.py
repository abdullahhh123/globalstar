# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PartnerGlobal(models.Model):
    _inherit = 'res.partner'

    contact_person_id = fields.Many2one(comodel_name="res.users", default=lambda self: self.env.user)
    c_r = fields.Char(string="C.R #")
    nickname = fields.Char()
    invoice_percentage = fields.Float()


class AccountPaymentGlobal(models.Model):
    _inherit = 'account.payment'

    allow_journal_ids = fields.Many2many('account.journal', compute='_compute_allow_journal_ids',
                                         relation="journal_payments_rel")

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_allow_journal_ids(self):
        for m in self:
            domain = [('type', 'in', ('bank', 'cash'))]
            if self.env.user.account_journal_ids:
                domain.append(('id', 'in', self.env.user.account_journal_ids.ids))
            m.allow_journal_ids = self.env['account.journal'].search(domain)


class AccountMoveGlobal(models.Model):
    _inherit = 'account.move'

    discount_move_id = fields.Many2one(comodel_name="account.move")

    @api.model
    def _search_default_journal(self, journal_types):
        company_id = self._context.get('default_company_id', self.env.company.id)
        domain = [('company_id', '=', company_id), ('type', 'in', journal_types)]
        if self.env.user.account_journal_ids:
            domain.append(('id', 'in', self.env.user.account_journal_ids.ids))

        journal = None
        if self._context.get('default_currency_id'):
            currency_domain = domain + [('currency_id', '=', self._context['default_currency_id'])]
            journal = self.env['account.journal'].search(currency_domain, limit=1)

        if not journal:
            journal = self.env['account.journal'].search(domain, limit=1)

        if not journal:
            company = self.env['res.company'].browse(company_id)

            error_msg = _(
                "No journal could be found in company %(company_name)s for any of those types: %(journal_types)s",
                company_name=company.display_name,
                journal_types=', '.join(journal_types),
            )
            raise UserError(error_msg)

        return journal

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for m in self:
            journal_type = m.invoice_filter_type_domain or 'general'
            company_id = m.company_id.id or self.env.company.id
            domain = [('company_id', '=', company_id), ('type', '=', journal_type)]
            if self.env.user.account_journal_ids:
                domain.append(('id', 'in', self.env.user.account_journal_ids.ids))
            m.suitable_journal_ids = self.env['account.journal'].search(domain)


class AccountMoveLineGlobal(models.Model):
    _inherit = 'account.move.line'

    is_partner_disc = fields.Boolean()


class AccountAccountGlobal(models.Model):
    _inherit = 'account.account'

    customer_discount = fields.Selection(selection=[('debit', 'Debit'), ('credit', 'Credit')])


class ResUsersGlobal(models.Model):
    _inherit = 'res.users'

    stock_warehouse_ids = fields.Many2many(comodel_name="stock.warehouse", relation="warehouse_user_rel")
    account_journal_ids = fields.Many2many(comodel_name="account.journal", relation="journal_user_rel")

    @api.constrains('stock_warehouse_ids')
    def onchange_stock_warehouse(self):
        self.clear_caches()


class AccountJournalGlobal(models.Model):
    _inherit = 'account.journal'

    specific_users_ids = fields.Many2many(comodel_name="res.users", relation="journal_user_rel", string="Users")
    partner_discount = fields.Boolean()
