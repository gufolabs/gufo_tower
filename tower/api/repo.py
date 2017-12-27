# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Mercurial repo hosting
# ----------------------------------------------------------------------
# Copyright (C) 2007-2015 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import logging

# Third-party modules
import mercurial.ui
import tornado.web
import tornado.wsgi
from mercurial.hgweb.hgwebdir_mod import hgwebdir

logger = logging.getLogger(__name__)


class RepoHandler(tornado.web.FallbackHandler):
    def initialize(self):
        ui = mercurial.ui.ui()
        ui.setconfig('ui', 'report_untrusted', 'off', 'hgwebdir')
        ui.setconfig('ui', 'nontty', 'true', 'hgwebdir')
        ui.setconfig("web", "baseurl", "/hg", "hgwebdir")
        ui.setconfig("web", "style", "gitweb", "hgwebdir")
        ui.setconfig("web", "logourl", "http://nocproject.org/", "hgwebdir")
        # @todo: Set proper paths, use prefix
        fallback = tornado.wsgi.WSGIContainer(
            hgwebdir([("/", "var/tower/repo/*")], ui)
        )
        super(RepoHandler, self).initialize(fallback)

    def prepare(self):
        # Rewrite /hg -> /
        self.request.path = self.request.path[3:]
        super(RepoHandler, self).prepare()
