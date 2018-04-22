# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Tower web daemon
# ----------------------------------------------------------------------
# Copyright (C) 2016 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

import hashlib
import logging
# Python modules
import os

# Third-party modules
import tornado.template

try:
    import jsmin
except ImportError:
    jsmin = None
# Tower modules
from tower.models.settings import Settings

logger = logging.getLogger("ui")


class UIHandler(tornado.web.RequestHandler):
    hash = None
    CACHE_ROOT = "var/tower/cache"

    def initialize(self, path, *args, **kwargs):
        self.root = path

    def get(self):
        name = Settings.get_installation_name() or "Unconfigured installation"
        return self.render(
            os.path.join(self.root, "index.html"),
            installation_name=name,
            mergecache=self.mergecache,
            hashed=self.hashed
        )

    def mergecache(self, jslist):
        if self.hash is None:
            logger.debug("Calculating JS hash")
            r = []
            for f in jslist:
                path = os.path.join(self.root, f)
                if os.path.isfile(path):
                    with open(path) as f:
                        r += [f.read()]
            js = "\n".join(r)
            if jsmin:
                ssize = len(js)
                js = jsmin.jsmin(js)
                logger.info("Minifying JS: %s -> %s", ssize, len(js))
            self.hash = hashlib.sha256(js.encode(encoding='utf-8')).hexdigest()[:8]
            cache_path = os.path.join(self.CACHE_ROOT, "%s.js" % self.hash)
            if not os.path.isfile(cache_path):
                logger.info("Writing cached JS to %s", cache_path)
                with open(cache_path, "w") as f:
                    f.write(js)
        return "<script src=\"/ui/cache/%s.js\" type=\"text/javascript\"></script>" % self.hash

    def hashed(self, path):
        """
        Convert path to path?hash version
        :param path:
        :return:
        """
        fp = path
        if fp.startswith("/ui/"):
            fp = fp[4:]
        fp = os.path.join(self.root, fp)
        with open(fp, 'r') as f:
            hash = hashlib.sha256(f.read().encode(encoding='utf-8')).hexdigest()[:8]
        return "%s?%s" % (path, hash)
