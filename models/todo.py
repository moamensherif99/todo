from odoo import models,fields

class ToDo(models.Model):
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'todo'

    name = fields.Char(string="Task Name")
    assign_to_id = fields.Many2one('res.partner')
    description = fields.Char()
    due_date = fields.Date()
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ])

    def status_new(self):
        for rec in self:
            rec.status = 'new'

    def status_in_progress(self):
        for rec in self:
            rec.status = 'in_progress'

    def status_completed(self):
        for rec in self:
            rec.status = 'completed'