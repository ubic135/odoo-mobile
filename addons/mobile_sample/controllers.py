# -*- coding: utf-8 -*-
##############################################################################
#
#    Diogo Carvalho Duarte
#    Copyright (C) 2004-2024 Diogo Duarte (<http://diogocduarte.github.io/>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
from datetime import datetime, timedelta
from calendar import weekday
from openerp import http
from openerp.http import request
import werkzeug.utils
import pytz
from openerp.tools.translate import _
from openerp.addons.web.controllers.main import module_boot, login_redirect
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

MODULE_BASE_PATH = '/mobile/sample/'

class SampleController(http.Controller):

    @http.route(MODULE_BASE_PATH)
    def main(self, **kwargs):
        cr, uid, context, session = request.cr, request.uid, request.context, request.session
        # this must be replaced by mobile login 
        if not session.uid:
            return login_redirect()
        return werkzeug.utils.redirect(MODULE_BASE_PATH + '/contacts/')

    @http.route(MODULE_BASE_PATH + 'contacts/', type='http', methods=['GET'], auth="user")
    def getsearchform(self, **kwargs):
        cr, uid, context, session = request.cr, request.uid, request.context, request.session
        # TODO:this must be replaced by mobile login 
        if not session.uid:
            return login_redirect()
        return http.request.render('mobile_sample.searchform', {
            'root': MODULE_BASE_PATH,
            'contacts': False
        })
        
    @http.route(MODULE_BASE_PATH + 'contacts/', type='http', methods=['POST'], auth="user")
    def postsearchresult(self, **kwargs):
        cr, uid, context, session = request.cr, request.uid, request.context, request.session
        # TODO:this must be replaced by mobile login 
        if not session.uid:
            return login_redirect()
        cr, uid = request.cr, request.uid
        partners = request.registry.get("res.partner")
        ids = partners.search(cr, uid, [('customer', '=', True),('name', 'ilike', kwargs['searchtx'])])
        obj = []
        for rec in partners.browse(cr, uid, ids):
            obj.append(rec)
        return http.request.render('mobile_sample.searchform', {
            'root': MODULE_BASE_PATH,
            'customers': obj
        })

    @http.route(MODULE_BASE_PATH + 'contacts/<int:id>', type='http', auth="user")
    def getcustomer(self, id, **kwargs):
        cr, uid, context, session = request.cr, request.uid, request.context, request.session
        # TODO:this must be replaced by mobile login 
        if not session.uid:
            return login_redirect()
        cr, uid = request.cr, request.uid
        partners = request.registry.get("res.partner")
        ids = partners.search(cr, uid, [('id', '=', id)])
        obj = partners.browse(cr, uid, ids)
        return http.request.render('mobile_sample.customer', {
            'root': MODULE_BASE_PATH,
            'customer': obj[0]
        })
