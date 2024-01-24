import os
current_dir = os.path.dirname(os.path.abspath(__file__))

version_file = os.path.join(current_dir, '../../VERSION')
if not os.path.exists(version_file):
    version_file = os.path.join(current_dir, '../../../../VERSION')

with open(version_file, 'r') as f:
    version = f.read().strip()

__version__ = version
__authors__ = "Ad de Roo, Emiliano Gelati, Peter Burek, Johan van der Knijff, Niko Wanders"
__date__ = "23/01/2024"
__copyright__ = "Copyright 2019-2024, European Commission - Joint Research Centre"
__maintainer__ = "Stefania Grimaldi, Cinzia Mazzetti, Carlo Russo, Damien Decremer, Corentin Carton De Wiart, Valerio Lorini, Ad de Roo"
__status__ = "Operation"
__institution__ = "European Commission DG Joint Research Centre (JRC) - E1, D2 Units"
