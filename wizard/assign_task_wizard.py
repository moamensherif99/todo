from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssignTask(models.TransientModel):
    _name = 'assign.task'
    _description = 'Assign Task Wizard'

    todo_ids = fields.Many2many('todo.task', default=lambda self: self.env.context.get('active_ids'))
    assign_to_id = fields.Many2one('res.partner')

    def action_assign_tasks(self):
        for rec in self:
            if any(task.status in ['completed', 'closed'] for task in rec.todo_ids):
                raise ValidationError(
                    "You cannot assign tasks that are already completed or closed."
                )
            else:
                rec.todo_ids.write({'assign_to_id': rec.assign_to_id.id})
