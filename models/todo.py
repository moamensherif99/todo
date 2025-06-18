from odoo import models,fields,api
from odoo.exceptions import ValidationError

class ToDo(models.Model):
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'todo'

    name = fields.Char(string="Task Name")
    active = fields.Boolean(default=True)
    assign_to_id = fields.Many2one('res.partner')
    description = fields.Char()
    due_date = fields.Date()
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed')
    ])
    estimated_time = fields.Float()
    todo_line_ids = fields.One2many('todo.line','todo_id')
    is_late = fields.Boolean()
    ref = fields.Char(default='New', readonly=1)

    def status_new(self):
        for rec in self:
            rec.status = 'new'

    def status_in_progress(self):
        for rec in self:
            rec.status = 'in_progress'

    def status_completed(self):
        for rec in self:
            rec.status = 'completed'

    def status_closed(self):
        for rec in self:
            rec.status = 'closed'

    @api.constrains('estimated_time', 'todo_line_ids.working_time')
    def _check_working_time(self):
        for rec in self:
            total_spent = sum(rec.todo_line_ids.mapped('working_time'))

            if rec.estimated_time > 0 and total_spent > rec.estimated_time:
                raise ValidationError(
                    f"The total time spent ({total_spent} hours) cannot exceed the "
                    f"estimated time ({rec.estimated_time} hours) for this task."
                )

    def check_due_date(self):
        print('GGGGGGGGggg')
        for rec in self.search([]):
            if rec.due_date and rec.due_date < fields.date.today():
                if rec.status in ['new', 'in_progress']:
                    rec.is_late = True
                else:
                    rec.is_late = False

    @api.model
    def create(self, vals):
        res = super(ToDo, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('todo_seq')
        return res

class ToDOLine(models.Model):
    _name = 'todo.line'
    _description = 'todo line'

    todo_id = fields.Many2one('todo.task')
    date = fields.Date()
    description = fields.Char()
    working_time = fields.Float()
