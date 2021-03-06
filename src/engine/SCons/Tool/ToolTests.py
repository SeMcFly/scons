#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import sys
import unittest

import TestUnit

import SCons.Errors
import SCons.Tool

class ToolTestCase(unittest.TestCase):
    def test_Tool(self):
        """Test the Tool() function"""
        class Environment(object):
            def __init__(self):
                self.dict = {}
            def Detect(self, progs):
                if not SCons.Util.is_List(progs):
                    progs = [ progs ]
                return progs[0]
            def Append(self, **kw):
                self.dict.update(kw)
            def __getitem__(self, key):
                return self.dict[key]
            def __setitem__(self, key, val):
                self.dict[key] = val
            def __contains__(self, key):
                return self.dict.__contains__(key)
            def has_key(self, key):
                return key in self.dict
            def subst(self, string, *args, **kwargs):
                return string
        env = Environment()
        env['BUILDERS'] = {}
        env['ENV'] = {}
        env['PLATFORM'] = 'test'
        t = SCons.Tool.Tool('g++')
        t(env)
        assert (env['CXX'] == 'c++' or env['CXX'] == 'g++'), env['CXX']
        assert env['INCPREFIX'] == '-I', env['INCPREFIX']
        assert env['TOOLS'] == ['g++'], env['TOOLS']

        try:
            SCons.Tool.Tool()
        except TypeError:
            pass
        else:   # TODO pylint E0704: bare raise not inside except
            raise

        try:
            p = SCons.Tool.Tool('_does_not_exist_')
        except SCons.Errors.SConsEnvironmentError:
            pass
        else:   # TODO pylint E0704: bare raise not inside except
            raise


if __name__ == "__main__":
    suite = unittest.makeSuite(ToolTestCase, 'test_')
    TestUnit.run(suite)

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
