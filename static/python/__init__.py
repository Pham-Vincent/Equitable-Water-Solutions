"""
Exposes all modules and their publicly used functions allowing for granular imports or 
importing all at once.

Examples:
>>> # Import all modules
>>> from static.python import *
>>>
>>> # Import specific parts of a module
>>> from static.python import aboutusFunction, contactusFunction
"""

from .About import aboutusFunction, contactusFunction
from .Database import DatabaseConn
from .FeatureExtraction import interpolation, AverageDailySalinity, MonthlyAverages
from .Graph import Maryland_Tidal_Graph, Virginia_Tidal_Graph, MultiDepthGraphing
from .LocationPinning import retrieve_sessionid, add_pin_to_database, overridecheck, returnPinned
from .login import (
    verify_email,
    send_verification_email,
    registerFunction,
    loginFunction,
    checkLogin
)

__all__ = [
    # About.py exports
    'aboutusFunction',
    'contactusFunction',
    
    # Database.py exports
    'DatabaseConn',
    
    # FeatureExtraction.py exports
    'interpolation',
    'AverageDailySalinity',
    'MonthlyAverages',
    
    # Graph.py exports
    'Maryland_Tidal_Graph',
    'Virginia_Tidal_Graph',
    'MultiDepthGraphing',
    
    # LocationPinning.py exports
    'retrieve_sessionid',
    'add_pin_to_database',
    'overridecheck',
    'returnPinned',
    
    # login.py exports
    'verify_email',
    'send_verification_email',
    'registerFunction',
    'loginFunction',
    'checkLogin'
] 