"""
This package provides the core functionality of Font Manager.

Importing this package ensures that all the folders and files the application
requires are present and valid.

The FontManager class provides convenient access to all available family
objects and collections.
"""
# Font Manager, a font management application for the GNOME desktop
#
# Copyright (C) 2009, 2010 Jerry Casiano
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
# along with this program; if not, write to:
#
#    Free Software Foundation, Inc.
#    51 Franklin Street, Fifth Floor
#    Boston, MA 02110-1301, USA.

# Disable warnings related to gettext
# pylint: disable-msg=E0602

import os
import glib
import gobject
import logging
import shutil
import UserDict
import ConfigParser
import time

from os.path import exists, join, isdir, realpath

import fonts

from constants import *
from utils.common import AvailableApps, natural_sort, autostart
from utils.xmlutils import load_directories, save_blacklist, save_directories

APPLIST = None
MANAGER = None
PREFERENCES = None
PROGRESS_CALLBACK = None


class FontManager(gobject.GObject, UserDict.UserDict):
    """
    This class is a dictionary of Family objects.

    It also contains font categories and user defined collections, it
    provides convenience methods for enabling/disabling font families,
    adding/removing font collections and modifying them.

    Emits 'update-font-select' any time font families are enabled/disabled.
    Emits 'update-font-groups' any time collections are modified.

    Keyword Arguments:

    progress_callback -- a function to call, it will be called everytime
                        a family is processed with the name of the family,
                        the total number of families to be processed and
                        the number of families processed so far.

    """
    _loading = False
    __gproperties__ =   {
                        'disabled'  :   (gobject.TYPE_STRING,
                                        'Disable family',
                                        'Disable a font family',
                                        'None', gobject.PARAM_WRITABLE),
                        'enabled'   :   (gobject.TYPE_STRING,
                                        'Enable family',
                                        'Enable a font family',
                                        'None', gobject.PARAM_WRITABLE),
                        'reject'    :   (gobject.TYPE_PYOBJECT,
                                        'Disabled families',
                                        'List of disabled families',
                                        gobject.PARAM_READABLE),
                        'accept'    :   (gobject.TYPE_PYOBJECT,
                                        'Enabled families',
                                        'List of enabled families',
                                        gobject.PARAM_READABLE)
                                        }
    __gsignals__    =   {
                        'update-font-select'    :   (gobject.SIGNAL_RUN_LAST,
                                                    gobject.TYPE_NONE,
                                                    (gobject.TYPE_PYOBJECT,)),
                        'update-font-groups'    :   (gobject.SIGNAL_RUN_LAST,
                                                    gobject.TYPE_NONE,
                                                    (gobject.TYPE_PYOBJECT,))
                                                    }
    def __init__(self, progress_callback = None, parent = None):
        self._loading = True
        super(FontManager, self).__init__()
        self.progress = progress_callback
        self.parent = parent
        self._disabled = []
        self._enabled = []
        self.categories = {}
        self.collections = {}
        self.initial_collection_order = []
        self.data = {}
        if self.parent:
            fonts.Sort(self, self.progress, self.parent)
        else:
            fonts.Sort(self, self.progress)
        self._update_selections()
        self.auto_enable_collections()
        self._loading = False
        self.connid = self.connect('update-font-groups', self._update_orphans)

    def _add_category(self, category):
        """
        Add a category object.
        """
        if isinstance(category, fonts.Collection):
            self.categories[category.name] = category
        else:
            raise TypeError('Not a valid category object')
        self.emit('update-font-groups', self.categories)
        return

    def _add_collection(self, collection):
        """
        Add a collection object.
        """
        if isinstance(collection, fonts.Collection):
            self.collections[collection.name] = collection
        else:
            raise TypeError('Not a valid collection object')
        self.emit('update-font-groups', self.collections)
        return

    def add_families_to(self, collection, *families):
        """
        Add families to an existing collection.
        """
        if isinstance(collection, str):
            collection = self.collections[collection]
        elif not isinstance(collection, fonts.Collection):
            raise TypeError('Not a valid collection object or family name')
        if isinstance(families[0], str):
            collection.add(families[0])
        elif isinstance(families[0], (tuple, list)):
            families = list(families[0])
            collection.add(families)
        self.emit('update-font-groups', self.collections)
        return

    def auto_enable_collections(self):
        """
        Automatically enable/disable collections and categories based on
        whether they contain any enabled families or not.
        """
        for collection in self.categories.itervalues():
            collection.enabled = False
            for family in collection.families:
                if family in self._enabled:
                    collection.enabled = True
                    break
        for collection in self.collections.itervalues():
            collection.enabled = False
            for family in collection.families:
                if family in self._enabled:
                    collection.enabled = True
                    break
        self.emit('update-font-groups', self.collections)
        return

    def contains(self, family):
        """
        Return True if family is aavailable.
        """
        if family in self.data.iterkeys():
            return True
        return False

    def create_category(self, name, comment = None, families = None):
        """
        Create and add a category object.

        name -- collection name

        Keyword Arguments:

        comment -- comment to display in tooltips
        families -- a family, a list or tuple of families to add
        """
        if name in self.categories.iterkeys():
            raise ValueError('Category %s already exists' % name)
        collection = fonts.Collection(name)
        collection.builtin = True
        if comment and isinstance(comment, str):
            collection.comment = comment
        if families:
            self.add_families_to(collection, families)
        self._add_category(collection)
        return

    def create_collection(self, name, comment = None, families = None):
        """
        Create and add a collection object.

        name -- collection name

        Keyword Arguments:

        comment -- comment to display in tooltips
        families -- a family, a list or tuple of families to add
        """
        if name in self.collections.iterkeys():
            raise ValueError('Collection %s already exists' % name)
        collection = fonts.Collection(name)
        if isinstance(comment, str):
            collection.comment = comment
        else:
            collection.comment = _('Created on %s' % \
                time.strftime('%A, %B %d, %Y, at %I:%M %p', time.localtime()))
        if families:
            self.add_families_to(collection, families)
        self._add_collection(collection)
        return

    def disable_collection(self, collection):
        """
        Disable collection.
        """
        if collection in self.collections:
            self.set_disabled(self.collections[collection].families)
        elif collection in self.categories:
            self.set_disabled(self.categories[collection].families)
        else:
            raise IndexError('No such collection or category')
        self.emit('update-font-groups', self.collections)
        return

    def do_get_property(self, prop):
        """
        get_property
        """
        if prop.name == 'reject':
            return self._disabled
        elif prop.name == 'accept':
            return self._enabled
        else:
            raise AttributeError('Unknown property : %s' % prop.name)

    def _do_set(self, values, state):
        """
        Actual set_property
        """
        try:
            if isinstance(values, str):
                self.data[values].enabled = state
            elif isinstance(values[0], (tuple, list)):
                for value in values[0]:
                    self.data[value].enabled = state
            elif isinstance(values, (tuple, list)):
                for value in values:
                    self.data[value].enabled = state
            else:
                raise TypeError\
                ('Expected str, tuple or list got %s instead' % type(values[0]))
        except KeyError, key:
            raise ValueError( '%s is not a valid family name' % key)
        self._update_selections()
        self.emit('update-font-select', self._disabled)
        return

    def do_set_property(self, prop, value):
        """
        set_property
        """
        if prop.name == 'enabled':
            self._do_set(value[0], True)
        elif prop.name == 'disabled':
            self._do_set(value, False)
        else:
            raise AttributeError('Unknown property : %s' % prop.name)
        return

    def enable_collection(self, collection):
        """
        Enable collection.
        """
        if collection in self.collections:
            self.set_enabled(self.collections[collection].families)
        elif collection in self.categories:
            self.set_enabled(self.categories[collection].families)
        else:
            raise IndexError('No such collection or category')
        self.emit('update-font-groups', self.collections)
        return

    def get_collection_details(self, collection):
        """
        Return collection details. Name, comment and list of families.
        """
        if collection in self.collections:
            return str(self.collections[collection].name), \
                    str(self.collections[collection].comment), \
                    self.collections[collection].families
        elif collection in self.categories:
            return str(self.categories[collection].name), \
                    str(self.categories[collection].comment), \
                    self.categories[collection].families
        else:
            raise IndexError('No such collection or category')

    def list_categories(self):
        """
        Return a sorted list of available categories.
        """
        return natural_sort([c for c in self.categories.iterkeys()])

    def list_collections(self):
        """
        Return a sorted list of available collections.
        """
        return natural_sort([c for c in self.collections.iterkeys()])

    def list_disabled(self):
        """
        Return a sorted list of disabled families.
        """
        self._update_selections()
        return natural_sort(self._disabled)

    def list_enabled(self):
        """
        Return a sorted list of enabled families.
        """
        self._update_selections()
        return natural_sort(self._enabled)

    def list_families(self):
        """
        Return a sorted list of all available families.
        """
        return natural_sort([f for f in self.data.iterkeys()])

    def list_families_in(self, collection):
        """
        Return a sorted list of families in collection.
        """
        if collection in self.collections:
            return natural_sort(self.collections[collection].families)
        elif collection in self.categories:
            return natural_sort(self.categories[collection].families)
        else:
            raise IndexError('No such collection or category')
        return

    def remove_collection(self, collection):
        """
        Remove an existing collection.
        """
        if collection in self.collections:
            del self.collections[collection]
        else:
            raise IndexError('No such collection')
        self.emit('update-font-groups', self.collections)
        return

    def remove_families(self, *families):
        """
        Remove a family, a tuple or list of families.
        """
        collections = self.list_collections() + self.list_categories()
        if isinstance(families[0], str):
            if self.contains(families[0]):
                del self.data[families[0]]
                for collection in collections:
                    if families[0] in self.list_families_in(collection):
                        self.remove_families_from(collection, families[0])
        elif isinstance(families[0], (tuple, list)):
            for family in families[0]:
                while self.contains(family):
                    del self.data[family]
                for collection in collections:
                    if family in self.list_families_in(collection):
                        self.remove_families_from(collection, family)
        else:
            raise TypeError\
            ('Expected a string, tuple or list but got %s instead' % \
            type(families[0]))
        return

    def remove_families_from(self, collection, *families):
        """
        Remove families from an existing collection.
        """
        if isinstance(collection, str):
            try:
                collection = self.collections[collection]
            except KeyError:
                collection = self.categories[collection]
        elif not isinstance(collection, fonts.Collection):
            raise TypeError('Not a valid collection object or name')
        collection.remove(families[0])
        self.emit('update-font-groups', self.collections)
        return

    def set_disabled(self, *family):
        """
        Disable a family, list or tuple of families.
        """
        self._do_set(family, False)
        return

    def set_enabled(self, *family):
        """
        Enable a family, list or tuple of families.
        """
        self._do_set(family, True)
        return

    def total_families(self):
        """
        Return a current total of families.
        """
        return len(self.categories[_('All')].families)

    def _update_orphans(self, unused_cls_instance, unused_collections):
        """
        Update orphans list.
        """
        collected = []
        for collection in self.list_collections():
            collected += self.list_families_in(collection)
        self.categories[_('Orphans')].families = \
        [f for f in self.data.iterkeys() if f not in set(collected)]
        return

    def _update_selections(self):
        """
        Update 'reject' and 'accept' properties whenever a font family is
        enabled or disabled.
        """
        del self._disabled[:]
        del self._enabled[:]
        for key, obj in self.data.iteritems():
            if obj.enabled:
                self._enabled.append(key)
            else:
                self._disabled.append(key)
        return

gobject.type_register(FontManager)


class Preferences(gobject.GObject):
    """
    Load/Save user preferences

    Emits 'update-font-dirs' anytime user font directories are added or removed.
    """
    __gsignals__    =   {
                        'update-font-dirs'  :   (gobject.SIGNAL_RUN_LAST,
                                                    gobject.TYPE_NONE,
                                                    ()),
                        'update-tray-icon'  :   (gobject.SIGNAL_RUN_LAST,
                                                    gobject.TYPE_NONE,
                                                    (gobject.TYPE_BOOLEAN,))
                                                    }
    _sections = ('Categories', 'Collections', 'Export Options', 'Font Folder',
                    'General', 'Interface')
    _section_map = {
                    'Categories'        :   ['orphans'],
                    'Collections'       :   ['tooltips', 'focusondrop'],
                    'Export Options'    :   ['archivetype', 'fontsize',
                                                                'pangram'],
                    'Font Folder'       :   ['folder'],
                    'General'           :   ['autostart', 'minimizeonclose',
                                                            'minimizeonstart'],
                    'Interface'         :   ['collectiontotals', 'familytotals',
                                            'hpane', 'vpane', 'windowsize',
                                            'maximized', 'previewsize',
                                            'bgcolor', 'fgcolor', 'browsemode']
                    }
    _defaults = {
                    'config_file'       :   APP_CONFIG,
                    'archivetype'       :   'zip',
                    'autostart'         :   False,
                    'folder'            :   USER_FONT_DIR,
                    'fontsize'          :   20.0,
                    'pangram'           :   False,
                    'minimizeonclose'   :   False,
                    'orphans'           :   False,
                    'minimizeonstart'   :   False,
                    'tooltips'          :   True,
                    'focusondrop'       :   True,
                    'collectiontotals'  :   False,
                    'familytotals'      :   False,
                    'experimental'      :   False,
                    'hpane'             :   0,
                    'vpane'             :   0,
                    'windowsize'        :   '0:0',
                    'maximized'         :   False,
                    'previewsize'       :   11.0,
                    'bgcolor'           :   '#FFF',
                    'fgcolor'           :   '#000',
                    'browsemode'        :   False
                    }
    fontdirs = []
    def __init__(self):
        gobject.GObject.__init__(self)
        self.config = ConfigParser.ConfigParser()
        self._load_defaults()
        if exists(self.config_file):
            self.config.read(self.config_file)
            self._load_user_prefs()
        directories = load_directories()
        if directories:
            for directory in directories:
                self.fontdirs.append(directory)

    def add_user_font_dir(self, directory):
        """
        Add a user directory to include in FontConfig search path.
        """
        if directory:
            if isdir(directory) and (directory not in self.fontdirs):
                self.fontdirs.append(directory)
            save_directories(self.fontdirs)
            self.emit('update-font-dirs')
        return

    def on_autostart(self, startme = True):
        """
        Install or remove .desktop file autostart directory.
        """
        setattr(self, 'autostart', startme)
        autostart(startme)
        return

    def list_user_font_dirs(self):
        """
        Return a list of user configured font directories.
        """
        return set(self.fontdirs)

    def _load_user_prefs(self):
        """
        Load any saved preferences.
        """
        try:
            config = self.config
            for section, options in self._section_map.iteritems():
                for option in options:
                    if isinstance(self._defaults[option], bool):
                        setattr(self, option, 
                                            config.getboolean(section, option))
                    elif isinstance(self._defaults[option], int):
                        setattr(self, option, config.getint(section, option))
                    elif isinstance(self._defaults[option], float):
                        setattr(self, option, config.getfloat(section, option))
                    else:
                        setattr(self, option, config.get(section, option))
            if self.collectiontotals or self.familytotals:
                setattr(self, 'experimental', True)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError,
        ConfigParser.MissingSectionHeaderError, ConfigParser.ParsingError):
            os.unlink(self.config_file)
            self._load_defaults()
        return

    def _load_defaults(self):
        """
        Load default preferences.
        """
        for attribute, default in self._defaults.iteritems():
            setattr(self, attribute, default)
        return

    def minimize_to_tray(self, minimize = True):
        setattr(self, 'minimizeonclose', minimize)
        self.emit('update-tray-icon', minimize)
        return

    def remove_user_font_dir(self, directory):
        """
        Remove a directory from the list of user configured font directories.
        """
        while directory in self.fontdirs:
            self.fontdirs.remove(directory)
        save_directories(self.fontdirs)
        self.emit('update-font-dirs')
        return

    def save(self):
        """
        Save current preferences to disk
        """
        config = self.config
        for section in config.sections():
            config.remove_section(section)
        for section in self._sections:
            if not config.has_section(section):
                config.add_section(section)
        for section in self._sections:
            for option in self._section_map[section]:
                config.set(section, option, str(getattr(self, option)))
        with open(self.config_file, 'wb') as configfile:
            self.config.write(configfile)
        save_directories(self.fontdirs)
        return

gobject.type_register(Preferences)


def get_applist():
    """
    Return an instance of AvailableApps.
    """
    global APPLIST
    if APPLIST:
        return APPLIST
    else:
        APPLIST = AvailableApps()
        return APPLIST

def get_manager(parent = None):
    """
    Return an instance of FontManager.
    """
    global MANAGER
    if MANAGER:
        return MANAGER
    else:
        if parent:
            MANAGER = FontManager(PROGRESS_CALLBACK, parent)
        else:
            MANAGER = FontManager(PROGRESS_CALLBACK)
        MANAGER.connect('update-font-select', _save_rejects)
        return MANAGER

def get_preferences():
    """
    Return an instance of Preferences.
    """
    global PREFERENCES
    if PREFERENCES:
        return PREFERENCES
    else:
        PREFERENCES = Preferences()
        return PREFERENCES

def _save_rejects(unused_cls_instance, families):
    """
    Save disabled families to file.
    """
    save_blacklist(families)
    return

def _setup_logging():
    """
    Ensure log exists and set logging options
    """
    try:
        with open(APP_LOG, 'w') as log:
            log.write('\n')
        # to send messages somewhere useful
        logging.basicConfig(filename=APP_LOG,
                            format=\
                        '%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%b %d %Y %H:%M:%S',
                            level=logging.DEBUG,filemode='w')
        # send them to the console too
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter\
        ('%(levelname)-8s:  %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
    except:
        print \
    "FontManagerError : failed to find/create log file, logging disabled"

def _migrate():
    """
    Migrate old files to new more XDG-like structure.
    """
    fm_dir                  =   os.path.join(HOME, '.FontManager')
    conf_dir                =   os.path.join(fm_dir, 'config')
    groups_dir              =   os.path.join(fm_dir, 'collections')
    install_directory       =   os.path.join(fm_dir, 'Library')
    ini                     =   os.path.join(conf_dir, 'FontManager.ini')
    fm_group_conf           =   os.path.join(groups_dir, 'groups.xml')
    fm_block_conf           =   os.path.join(conf_dir, 'rejects.conf')
    dirs_conf               =   os.path.join(conf_dir, 'dirs.conf')
    render_conf             =   os.path.join(conf_dir, 'render.conf')

    update = {
                install_directory   :   DATA_DIR,
                ini                 :   APP_CONFIG,
                fm_group_conf       :   USER_FONT_COLLECTIONS,
                fm_block_conf       :   USER_FONT_CONFIG_SELECT,
                dirs_conf           :   USER_FONT_CONFIG_DIRS,
                render_conf         :   USER_FONT_CONFIG_RENDER
                }

    for old, new in update.iteritems():
        if exists(old):
            if old == install_directory:
                shutil.rmtree(USER_LIBRARY_DIR)
                if exists(join(install_directory, 'fontlog')):
                    os.unlink(join(install_directory, 'fontlog'))
            shutil.move(old, new)
    shutil.rmtree(fm_dir, ignore_errors=True)

# Make sure we have everything we need to run properly
_setup_logging()
for folder in CACHE_DIR, CONFIG_DIR, APP_CONFIG_DIR, AUTOSTART_DIR, DATA_DIR, \
                        USER_FONT_CONFIG_DIR, USER_FONT_DIR, USER_LIBRARY_DIR:
    if not exists(folder):
        os.makedirs(folder, 0755)
        if folder == USER_FONT_DIR:
            from utils.common import install_readme
            install_readme()
# Migrate old files to new more XDG-like structure if needed
if exists(join(HOME, '.FontManager')):
    _migrate()
# Make sure our library symlink exists and points to the right place
if os.path.islink(USER_LIBRARY_SYMLINK):
    if realpath(USER_LIBRARY_SYMLINK) != USER_LIBRARY_DIR:
        os.unlink(USER_LIBRARY_SYMLINK)
if not exists(USER_LIBRARY_SYMLINK):
    os.symlink(USER_LIBRARY_DIR, join(USER_FONT_DIR, 'Library'))
# Overwrite user configuration file on startup.
if exists(USER_FONT_CONFIG):
    os.unlink(USER_FONT_CONFIG)
with open(USER_FONT_CONFIG, 'wb') as conf:
    conf.write(VALID_USER_FONT_CONFIG)
# Yeah, that last action is probably bad form, but a warning about that
# possibility has been in the release notes for a while, now that it's
# the default there's even a message about it in the file itself so... :-p

__version__ = '0.5.5'