LensReview.Photography - Do Your Homework First
===========================================================

System Requirements
--------------------------
There are a few system packages that must be installed in order to install the
necessary python modules.  There is a bash shell script that can be run to
install the necessary system requirements on CentOS 6 via yum, and Mac OSX if
you are using homebrew.


Requirements Python 2.7.6
--------------------------
The required pip modules for Python 2.7.6 are the ones listed in the
requirements.txt.

Trying to code with Python 3 in mind, so some of the modules are different.
The Python3 requirements (not currently working) are in requirements/requirements3.txt.

code-block:: python

pip install -r requirements/requirements3.txt


**emphasis (bold/strong)**

*italics*

Simple link: http://ajc.technology
Fancier link: 'AJC Technology' _

.. _AJC Technology: http://ajc.technology

Subsection Header
-----------------

#) An enumerated list item

#) Second Item

* First bullet

* Second Bullet

  * indented bullet

  * Note carriage return and indents

Listeral code block::

  def like():
    print("I like Weed")

  for i in range(10):
    like()

Python colored code block (requires pygments):

code-block:: python
