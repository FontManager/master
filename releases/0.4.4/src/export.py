"""
This module allows users to export "collections".
.
"""
# Font Manager, a font management application for the GNOME desktop
#
# Copyright 2009 Jerry Casiano
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
# Suppress errors related to gettext
# pylint: disable-msg=E0602
# Suppress messages related to missing docstrings
# pylint: disable-msg=C0111

import os
import gtk
import shutil
import subprocess
import ConfigParser

from os.path import exists, join

from common import Throbber
from config import INI, HOME, WORK_DIR


class Export:
    """
    Export a collection.
    """
    def __init__(self, collection, builder):
        self.collection = collection
        self.builder = builder
        self.archive = True
        self.sample = False
        self.outdir = join(HOME, "Desktop")
        # https://bugzilla.redhat.com/show_bug.cgi?id=551878
        # Do our staging elsewhere
        self.tmpdir = "%s/%s" % (WORK_DIR, self.collection.name)
        self.font_list = []
        self.file_list = []
        # Fonts for which filepath is ?
        self.no_info = []
        # UI elements
        self.mainbox = self.builder.get_object('main_box')
        self.options = self.builder.get_object('options_box')
        self.compress = gtk.CheckButton(_('Export as archive'))
        self.sampler = gtk.CheckButton(_('Include sample sheet'))
        self.chooser = gtk.FileChooserButton(_('Select destination'))
        self.status = gtk.Label()
        # Visual feedback
        self.throbber = Throbber(self.builder)
        # Get preferences
        config = ConfigParser.ConfigParser()
        config.read(INI)
        try:
            self.arch_type = config.get('Export Options', 'archivetype')
        except ConfigParser.NoSectionError:
            self.arch_type = 'zip'
        # Do work
        if self.build_filelist():
            self.confirm_export()
        else:
            return

    def build_filelist(self):
        for font in self.collection.fonts:
            file_path = font.filelist.itervalues()
            if file_path:
                for path in file_path:
                    # grab the real file, not a symlink
                    path = os.path.realpath(path)
                    if exists(path):
                        self.file_list.append(path)
                    # Try to catch 'broken' fonts...
                    # at this point this rarely works,
                    # it just tends to fail silently :-\
                    else:
                        self.no_info.append(font)
            else:
                self.no_info.append(font)
        if len(self.no_info) > 0:
            if self.export_anyways():
                return True
            else:
                return False
        return True

    # Fixes http://code.google.com/p/font-manager/issues/detail?id=6
    def confirm_export(self):
        dialog = gtk.Dialog(_('Export Collection'),
                            None,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OK, gtk.RESPONSE_OK))
        dialog.set_default_size(350, 190)
        self.compress.set_border_width(10)
        self.compress.connect('toggled', self.compress_toggled)
        self.compress.set_active(True)
        self.set_compress_tooltip()
        dialog.vbox.pack_start(self.compress, False, True, 0)
        self.sampler.set_border_width(10)
        self.sampler.connect('toggled', self.sampler_toggled)
        dialog.vbox.pack_start(self.sampler, False, True, 0)
        dialog.vbox.pack_start(self.status, True, True, 5)
        choose = gtk.Expander('Select a different folder')
        choose.set_expanded(False)
        choose.connect('activate', self.choose_toggled)
        self.chooser.set_current_folder(self.outdir)
        self.chooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.chooser.connect('current-folder-changed', self.change_dest)
        choose.add(self.chooser)
        dialog.vbox.pack_end(choose, False, True, 2)
        dialog.vbox.show_all()
        response = dialog.run()
        dialog.destroy()
        while gtk.events_pending():
            gtk.main_iteration()
        if not response == gtk.RESPONSE_OK:
            return
        self.sensitive(False)
        self.throbber.start()
        while gtk.events_pending():
            gtk.main_iteration()
        self.process_export()
        self.sensitive()
        self.throbber.stop()
        while gtk.events_pending():
            gtk.main_iteration()
        return

    def confirm_overwrite(self):
        dialog = gtk.Dialog(_('Destination already exists'), None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (_('Cancel'), gtk.RESPONSE_CANCEL,
                            _('Overwrite'), gtk.RESPONSE_OK),)
        dialog.set_default_size(300, 100)
        label = gtk.Label('Overwrite %s?' % \
        join(self.outdir, self.collection.name))
        dialog.vbox.pack_start(label)
        label.show()
        response = dialog.run()
        dialog.destroy()
        if response != gtk.RESPONSE_OK:
            shutil.rmtree(self.tmpdir)
            return False
        else:
            shutil.rmtree(join(self.outdir, self.collection.name))
            return True

    def do_file_copy(self):
        for path in set(self.file_list):
            shutil.copy(path, self.tmpdir)
            # Try to include AFM files for Type 1 fonts
            if path.endswith('.pfb'):
                afm_path = path.replace('.pfb', '.afm')
                if not exists(afm_path):
                    afm_path = path.replace('afm', 'AFM')
                if exists(afm_path):
                    try:
                        shutil.copy(afm_path, self.tmpdir)
                    except OSError:
                        pass
        return

    def do_pdf_setup(self):
        # Get preferences
        config = ConfigParser.ConfigParser()
        config.read(INI)
        try:
            from sampler import Config
            size = float(config.get('Export Options', 'fontsize'))
            pangram = config.getboolean('Export Options', 'pangram')
            C = Config()
            C.font_size = size
            C.include_pangram = pangram
        except ConfigParser.NoSectionError:
            C = None
        from sampler import BuildSample
        buildsample = BuildSample\
        (C, self.collection.name, self.tmpdir, join\
        (self.tmpdir, '%s.pdf' % self.collection.name), self.builder)
        if not buildsample.basic():
            return False
        else:
            return True

    def process_export(self):
        if exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        if not exists(WORK_DIR):
            os.mkdir(WORK_DIR)
        os.mkdir(self.tmpdir)
        self.do_file_copy()
        if self.sample:
            self.do_pdf_setup()
        if self.archive:
            self.create_archive()
        else:
            if exists(join(self.outdir, self.collection.name)) \
            and not self.confirm_overwrite():
                shutil.rmtree(WORK_DIR)
                os.chdir(HOME)
                return
            shutil.move(self.tmpdir, self.outdir)
        shutil.rmtree(WORK_DIR)
        os.chdir(HOME)
        return

    def compress_toggled(self, widget):
        if widget.get_active():
            self.archive = True
        else:
            self.archive = False
        self.status.set_text('')
        return

    def sampler_toggled(self, widget):
        try:
            import reportlab
            import logging
            logging.info\
            ('Using ReportLab Toolkit Version %s' % reportlab.Version)
        except ImportError:
            widget.set_active(False)
            widget.set_sensitive(False)
            self.status.set_markup\
            ('<span weight="light" size="small"><tt>' + \
            _('Install the ReportLab Toolkit to enable this feature') \
            + '</tt></span>')
        if widget.get_active():
            self.sample = True
        else:
            self.sample = False
        return

    def choose_toggled(self, widget):
        # Seems like this is backwards?
        if not widget.get_expanded():
            self.status.set_markup\
            ('<span weight="light" size="small"><tt>' + \
            _('You must have write permissions to the selected path') \
            + '</tt></span>')
            # Force an update
            while gtk.events_pending():
                gtk.main_iteration()
        else:
            self.status.set_text('')
            while gtk.events_pending():
                gtk.main_iteration()
        return

    def change_dest(self, widget):
        newdir = widget.get_filename()
        if os.access(newdir, os.W_OK):
            self.outdir = newdir
        else:
            widget.set_current_folder(join(HOME, "Desktop"))
        self.set_compress_tooltip()
        return

    def set_compress_tooltip(self):
        self.compress.set_tooltip_text\
        (_('Archive will be saved in %s format to %s') \
        % (self.arch_type, self.outdir))
        return

    def export_anyways(self):
        """
        If any filepaths were not found ask for confirmation before continuing.
        """
        dialog = gtk.Dialog(_('Missing information'), None,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    (_('Cancel'), gtk.RESPONSE_CANCEL,
                                    _('Continue'), gtk.RESPONSE_OK),)
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_size_request(450, 325)
        box = dialog.get_content_area()
        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled.set_property('shadow-type', gtk.SHADOW_ETCHED_IN)
        view = gtk.TextView()
        view.set_left_margin(5)
        view.set_right_margin(5)
        view.set_cursor_visible(False)
        view.set_editable(False)
        t_buffer = view.get_buffer()
        t_buffer.insert_at_cursor\
        (_("\nFilepaths for the following fonts could not be determined.\n"))
        t_buffer.insert_at_cursor(_("\nThese fonts will not be included :\n\n"))
        for font in set(self.no_info):
            t_buffer.insert_at_cursor("\t" + font.get_name() + "\n")
        scrolled.add(view)
        box.pack_start(scrolled, True, True, 0)
        box.show_all()
        response = dialog.run()
        dialog.destroy()
        if response == gtk.RESPONSE_OK:
            return True
        else:
            return False

    def create_archive(self):
        """
        Produces an archive from the selected collection

        Requires file-roller to be installed
        """
        os.chdir(self.outdir)
        roller = subprocess.Popen('file-roller' + ' -a "%s.%s" "%s"' % \
        (self.collection.name, self.arch_type, self.tmpdir), shell=True)
        # Wait for file-roller to finish
        while roller.poll() is None:
            continue
        shutil.rmtree(self.tmpdir)
        return

    def sensitive(self, state=True):
        self.mainbox.set_sensitive(state)
        self.options.set_sensitive(state)
        while gtk.events_pending():
            gtk.main_iteration()
        return
