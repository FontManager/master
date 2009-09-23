"""
.
"""
# Font Manager, a font management application for the GNOME desktop
#
# Copyright (C) 2009 Jerry Casiano
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to: Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

import os

PACKAGE     = _('Font Manager')
VERSION     = 'Uninstalled'
PACKAGE_DIR = os.getcwd()
LOCALEDIR   = PACKAGE_DIR

HOME                    =   os.getenv('HOME')
USER                    =   os.getenv('LOGNAME')
USER_FONT_DIR           =   os.path.join(HOME, '.fonts')

HOME                    =   os.getenv('HOME')
USER                    =   os.getenv('LOGNAME')
USER_FONT_CONF          =   os.path.join(HOME, '.fonts.conf')
USER_FONT_CONF_INVALID  =   os.path.join(HOME, 'original.fonts.conf')
FM_DIR                  =   os.path.join(HOME, '.FontManager')

VER                     =   os.path.join(FM_DIR, '0.4')
CONF_DIR                =   os.path.join(FM_DIR, 'config')
GROUPS_DIR              =   os.path.join(FM_DIR, 'collections')
DB_DIR                  =   os.path.join(FM_DIR, 'db')
LOG_DIR                 =   os.path.join(FM_DIR, 'logs')
TMP_DIR                 =   os.path.join(FM_DIR, 'temp')
INSTALL_DIRECTORY       =   os.path.join(FM_DIR, 'Library')
FM_CONF                 =   os.path.join(FM_DIR, 'FontManager.conf')

INI                     =   os.path.join(CONF_DIR, 'FontManager.ini')
FM_BLOCK_CONF           =   os.path.join(CONF_DIR, 'rejects.conf')
DIRS_CONF               =   os.path.join(CONF_DIR, 'dirs.conf')
RENDER_CONF             =   os.path.join(CONF_DIR, 'render.conf')
DIRS_CONF_BACKUP        =   DIRS_CONF + '.bak'
FM_BLOCK_CONF_TMP       =   FM_BLOCK_CONF + '.tmp'

FM_GROUP_CONF           =   os.path.join(GROUPS_DIR, 'groups.xml')
FM_GROUP_CONF_BACKUP    =   FM_GROUP_CONF + '.bak'

LOG_FILE                =   os.path.join(LOG_DIR, 'session.log')
LOG_FILE_BACKUP         =   os.path.join(LOG_DIR, 'previous-session.log')

OLD_FM_BLOCK_CONF       =   os.path.join(FM_DIR, 'FontManager.conf')
OLD_FM_GROUP_CONF       =   os.path.join(FM_DIR, 'groups.xml')
OLD_LOG_FILE            =   os.path.join(FM_DIR, 'session.log')
OLD_LOG_FILE_BACKUP     =   os.path.join(FM_DIR, 'previous-session.log')

