from __future__ import unicode_literals
import multiprocessing

"""
  For more info on configuring gunicorn, check out this link
  http://docs.gunicorn.org/en/develop/configure.html
"""

bind = "127.0.0.1:8002"
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = "error"
proc_name = "lensreview_photography"
