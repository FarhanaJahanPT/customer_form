from odoo import models, fields


class Customer_Form(models.Model):

    _name = 'customer.form'



class SaleOrder(models.Model):

    _inherit = "res.partner"

    sale_count = fields.Integer(compute='compute_count')
    customer_form = fields.Many2one('sale.order.line')


    def get_product(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'product',
            'view_mode': 'tree,form',
            'res_model': 'product.product',
            'domain': [('product_tmpl_id.name','=',self.customer_form.product_id.id)],
            'context': [('create', '=', False)],
        }

    def compute_count(self):
        for record in self:
            record.sale_count = self.env['product.product'].search_count([('product_tmpl_id.name','=',self.customer_form.product_id.id)])


class Product(models.Model):

    _inherit =  'product.product'

    total_sale = fields.Integer(string='Total Sale Count',compute='_compute_sale_order',store=True)

    def _compute_sale_order(self):
        for record in self:
            record.sale_count = self.env['sale.order'].search_count([('order_line.product_id', '=', self.ids)])



