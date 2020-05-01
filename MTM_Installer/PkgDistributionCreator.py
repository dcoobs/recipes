#!/usr/local/autopkg/python
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Modified version of Chris Gerke's PkgDistributionCreator script
# https://github.com/autopkg/cgerke-recipes/blob/master/SharedProcessors/PkgDistributionCreator.py
# This will take six specified pkgs (in this case, designed for individual Munki tools installers and MTM onboarding pkg)
# and then reconsolidate all the pkgs into a single distribution pkg

import os.path
import subprocess
import shutil
import xml.etree.ElementTree

from glob import glob
from autopkglib import Processor, ProcessorError

__all__ = ["PkgDistributionCreator"]

class PkgDistributionCreator(Processor):
    description = ("Bundles together munki pkg installers with MTM onboarding pkg. ")
    input_variables = {
        "source_file1": {
            "required": True,
            "description": ("Path to a source file (MyCoolPkg1.pkg) "),
        },
        "source_file2": {
            "required": True,
            "description": ("Path to a source file (MyCoolPkg2.pkg) "),
        },
        "source_file3": {
            "required": True,
            "description": ("Path to a source file (MyCoolPkg3.pkg) "),
        },
        "source_file4": {
            "required": True,
            "description": ("Path to a source file (MyCoolPkg4.pkg) "),
        },
        "source_file5": {
            "required": True,
            "description": ("Path to a source file (MyCoolPkg5.pkg) "),
        },
         "source_file6": {
            "required": True,
            "description": ("Path to a source file (MyCoolPkg6.pkg) "),
        },
         "source_file7": {
            "required": True,
            "description": ("Path to a source file (MyCoolPkg6.pkg) "),
        },
        "distribution_file": {
            "required": True,
            "description": ("Destination path of distribution file. "),
        },
        "package_dir": {
            "required": True,
            "description": ("Directory containing source pkgs. "),
        },
        "version": {
            "required": True,
            "description": ("Version of final pkg "),
        },
        "output_file": {
            "required": True,
            "description": ("Name of output file. "),
        },
    }
    output_variables = {
    }

    __doc__ = description
    source_path = None

    def pkgConvert(self):
        if os.path.exists('/usr/bin/productbuild'):
            try:
                self.output("Found binary %s" % '/usr/bin/productbuild')
            except OSError as e:
                raise ProcessorError(
                    "Can't find binary %s: %s" % ('/usr/bin/productbuild', e.strerror))
        try:
            pbcmd = ["/usr/bin/productbuild",
                      "--synthesize",
                      "--package", self.env['source_file1'],
                      "--package", self.env['source_file2'],
                      "--package", self.env['source_file3'],
                      "--package", self.env['source_file4'],
                      "--package", self.env['source_file5'],
                      "--package", self.env['source_file6'],
                      "--package", self.env['source_file7'],
                      self.env['distribution_file']]
            p = subprocess.Popen(pbcmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            (out, err) = p.communicate()
        except OSError as e:
            raise ProcessorError("Creation of distribution file failed with error code %d: %s"
                % (e.errno, e.strerror))
        if p.returncode != 0:
            raise ProcessorError("Creation of distribution file %s failed: %s"
                % (self.env['output_file'], err))
        distfile = self.env['distribution_file']
        origtree = xml.etree.ElementTree.parse(distfile)
        new_tag = xml.etree.ElementTree.SubElement(origtree.getroot(), 'title')
        new_tag.text = 'Univ. of Illinois Munki Onboarding'
        origtree.write(distfile)
        try:
            pbcmd = ["/usr/bin/productbuild",
                      "--distribution", self.env['distribution_file'],
                      "--package-path", self.env['package_dir'],
                      "--version", self.env['version'],
                      self.env['output_file']]
            p = subprocess.Popen(pbcmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            (out, err) = p.communicate()
        except OSError as e:
            raise ProcessorError("cmmac execution failed with error code %d: %s"
                % (e.errno, e.strerror))
        if p.returncode != 0:
            raise ProcessorError("cmmac conversion of %s failed: %s"
                % (self.env['output_file'], err))        
        
    def main(self):
        if os.path.exists(self.env['source_file1']):
            try:
                self.output("Found %s" % self.env['source_file1'])
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['source_file1'], e.strerror))
        if os.path.exists(self.env['source_file2']):
            try:
                self.output("Found %s" % self.env['source_file2'])
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['source_file2'], e.strerror))
        if os.path.exists(self.env['source_file3']):
            try:
                self.output("Found %s" % self.env['source_file3'])
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['source_file3'], e.strerror))
        if os.path.exists(self.env['source_file4']):
            try:
                self.output("Found %s" % self.env['source_file4'])
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['source_file4'], e.strerror))
        if os.path.exists(self.env['source_file5']):
            try:
                self.output("Found %s" % self.env['source_file5'])
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['source_file5'], e.strerror))
        if os.path.exists(self.env['source_file6']):
            try:
                self.output("Found %s" % self.env['source_file6'])
                self.pkgConvert()
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['source_file6'], e.strerror))
        if os.path.exists(self.env['source_file7']):
            try:
                self.output("Found %s" % self.env['source_file7'])
                self.pkgConvert()
            except OSError as e:
                raise ProcessorError(
                    "Can't find %s" % (self.env['source_file7'], e.strerror))
                
if __name__ == '__main__':
    processor = PkgDistributionCreator()
    processor.execute_shell()
