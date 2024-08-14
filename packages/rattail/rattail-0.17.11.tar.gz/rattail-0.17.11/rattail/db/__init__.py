# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Database Stuff
"""

import os
import sys
import logging

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None
else:
    from sqlalchemy import orm

from rattail.config import ConfigExtension as BaseExtension


log = logging.getLogger(__name__)


if sqlalchemy:

    class SessionBase(orm.Session):
        """
        Custom SQLAlchemy session class, which adds some convenience methods
        related to the SQLAlchemy-Continuum integration.
        """

        def __init__(self, rattail_config=None, rattail_record_changes=None, continuum_user=None, **kwargs):
            """
            Custom constructor, to allow specifying the Continuum user at session
            creation.  If ``continuum_user`` is specified, its value will be passed
            to :meth:`set_continuum_user()`.
            """
            super().__init__(**kwargs)
            self.rattail_config = rattail_config

            # maybe record changes
            if rattail_record_changes is None:
                rattail_record_changes = getattr(self.bind, 'rattail_record_changes', False)
            if rattail_record_changes:
                from rattail.db.changes import record_changes
                record_changes(self, config=self.rattail_config)
            else:
                self.rattail_record_changes = False

            if continuum_user is None:
                self.continuum_user = None
            else:
                self.set_continuum_user(continuum_user)

            # maybe log the current db pool status
            if getattr(self.bind, 'rattail_log_pool_status', False):
                log.debug(self.bind.pool.status())

        def set_continuum_user(self, user_info):
            """
            Set the effective Continuum user for the session.

            :param user_info: May be a :class:`model.User` instance, or the
              ``uuid`` or ``username`` for one.
            """
            if self.rattail_config:
                app = self.rattail_config.get_app()
                model = app.model
            else:
                from rattail.db import model

            if isinstance(user_info, model.User):
                user = self.merge(user_info)
            else:
                user = self.get(model.User, user_info)
                if not user:
                    try:
                        user = self.query(model.User).filter_by(username=user_info).one()
                    except orm.exc.NoResultFound:
                        user = None
            self.continuum_user = user


    Session = orm.sessionmaker(class_=SessionBase, rattail_config=None, expire_on_commit=False)


else: # no sqlalchemy
    Session = None


class ConfigExtension(BaseExtension):
    """
    Config extension for the ``rattail.db`` subpackage.  This extension is
    responsible for loading the available Rattail database engine(s), and
    configuring the :class:`Session` class with the default engine.  This
    extension expects to find something like the following in your config file:

    .. code-block:: ini

       [rattail.db]
       keys = default, host, other
       default.url = postgresql://localhost/rattail
       host.url = postgresql://host-server/rattail
       other.url = postgresql://other-server/rattail

    The result of this extension's processing is that the config object will
    get two new attributes:

    .. attribute:: rattail.config.RattailConfig.rattail_engines

       Dict of available Rattail database engines.  Keys of the dict are the
       same as found in the config file; values are the database engines.  Note
       that it is possible for this to be an empty dict.

    .. attribute:: rattail.config.RattailConfig.rattail_engine

       Default database engine; same as ``rattail_engines['default']``.  Note
       that it is possible for this value to be ``None``.
    """
    key = 'rattail.db'

    def configure(self, config):

        if Session:
            from rattail.db.config import configure_session
            from wuttjamaican.db import get_engines

            # Add Rattail database connection info to config.
            config.rattail_engines = get_engines(config, 'rattail.db')
            config.rattail_engine = config.rattail_engines.get('default')
            Session.configure(bind=config.rattail_engine, rattail_config=config)

            # TODO: This should be removed, it sets 'record changes' globally.
            configure_session(config, Session)

            # rattail export-csv
            config.setdefault('rattail.importing', 'to_csv.from_rattail.export.default_handler',
                              'rattail.importing.exporters:FromRattailToCSV')
            config.setdefault('rattail.importing', 'to_csv.from_rattail.export.default_cmd',
                              'rattail export-csv')
            config.setdefault('rattail.importing', 'to_csv.from_rattail.export.legacy_handler_setting',
                              'rattail.exporting, csv.handler')

            # rattail export-rattail
            config.setdefault('rattail.importing', 'to_rattail.from_rattail.export.default_handler',
                              'rattail.importing.rattail:FromRattailToRattailExport')
            config.setdefault('rattail.importing', 'to_rattail.from_rattail.export.default_cmd',
                              'rattail export-rattail')
            config.setdefault('rattail.importing', 'to_rattail.from_rattail.export.legacy_handler_setting',
                              'rattail.exporting, rattail.handler')

            # rattail import-csv
            config.setdefault('rattail.importing', 'to_rattail.from_csv.import.default_handler',
                              'rattail.importing.csv:FromCSVToRattail')
            config.setdefault('rattail.importing', 'to_rattail.from_csv.import.default_cmd',
                              'rattail import-csv')
            config.setdefault('rattail.importing', 'to_rattail.from_csv.import.legacy_handler_setting',
                              'rattail.importing, csv.handler')

            # rattail import-ifps
            config.setdefault('rattail.importing', 'to_rattail.from_ifps.import.default_handler',
                              'rattail.importing.ifps:FromIFPSToRattail')
            config.setdefault('rattail.importing', 'to_rattail.from_ifps.import.default_cmd',
                              'rattail import-ifps')
            config.setdefault('rattail.importing', 'to_rattail.from_ifps.import.legacy_handler_setting',
                              'rattail.importing, ifps.handler')

            # rattail import-rattail
            config.setdefault('rattail.importing', 'to_rattail.from_rattail.import.default_handler',
                              'rattail.importing.rattail:FromRattailToRattailImport')
            config.setdefault('rattail.importing', 'to_rattail.from_rattail.import.default_cmd',
                              'rattail import-rattail')
            config.setdefault('rattail.importing', 'to_rattail.from_rattail.import.legacy_handler_setting',
                              'rattail.importing, rattail.handler')

            # rattail import-rattail-bulk
            config.setdefault('rattail.importing', 'to_rattail.from_rattail_bulk.import.default_handler',
                              'rattail.importing.rattail_bulk:BulkFromRattailToRattail')
            config.setdefault('rattail.importing', 'to_rattail.from_rattail_bulk.import.default_cmd',
                              'rattail import-rattail-bulk')
            config.setdefault('rattail.importing', 'to_rattail.from_rattail_bulk.import.legacy_handler_setting',
                              'rattail.importing, rattail_bulk.handler')

            # rattail import-sample
            config.setdefault('rattail.importing', 'to_rattail.from_sample.import.default_handler',
                              'rattail.importing.sample:FromSampleToRattail')
            config.setdefault('rattail.importing', 'to_rattail.from_sample.import.default_cmd',
                              'rattail import-sample')
            config.setdefault('rattail.importing', 'to_rattail.from_sample.import.legacy_handler_setting',
                              'rattail.importing, sample.handler')

            # rattail import-versions
            config.setdefault('rattail.importing', 'to_rattail_versions.from_rattail.import.default_handler',
                              'rattail.importing.versions:FromRattailToRattailVersions')
            config.setdefault('rattail.importing', 'to_rattail_versions.from_rattail.import.default_cmd',
                              'rattail import-versions')
            config.setdefault('rattail.importing', 'to_rattail_versions.from_rattail.import.legacy_handler_setting',
                              'rattail.importing, versions.handler')

            # trainwreck export-trainwreck
            config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.export.default_handler',
                              'rattail.trainwreck.importing.trainwreck:FromTrainwreckToTrainwreckExport')
            config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.export.default_cmd',
                              'trainwreck export-trainwreck')
            config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.export.legacy_handler_setting',
                              'trainwreck.exporting, trainwreck.handler')

            # trainwreck import-self
            config.setdefault('rattail.importing', 'to_trainwreck.from_self.import.default_cmd',
                              'trainwreck import-self')

            # trainwreck import-trainwreck
            config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.import.default_handler',
                              'rattail.trainwreck.importing.trainwreck:FromTrainwreckToTrainwreckImport')
            config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.import.default_cmd',
                              'trainwreck import-trainwreck')
            config.setdefault('rattail.importing', 'to_trainwreck.from_trainwreck.import.legacy_handler_setting',
                              'trainwreck.importing, trainwreck.handler')

            # nb. cannot fetch DB settings during init
            appdir = config.appdir(require=False, usedb=False)
            if not appdir:
                appdir = os.path.join(sys.prefix, 'app')

            poser = config.get('rattail', 'poser', usedb=False,
                               default=os.path.join(appdir, 'poser'))

            # add poser to path if it exists
            if os.path.isdir(poser) and poser not in sys.path:
                sys.path.append(poser)
