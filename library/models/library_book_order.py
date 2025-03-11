# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class LibraryBookOrder(models.Model):
    _name = 'library.book.order'
    _description = _('LibraryBookOrder')

    name = fields.Char(_('Name'))
