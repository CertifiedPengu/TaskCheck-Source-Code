from distutils.core import setup
import zipfile
import py2exe, sys, os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

sys.argv.append('py2exe')

setup(options = {'py2exe': {'bundle_files': 1, 'compressed': True}}, data_files = [('icon', [os.getcwd() + '\pencil.ico'])], windows = [{"script":"TaskCheck.py","icon_resources":[(1,os.getcwd() + "\pencil.ico")]}], zipfile = None)