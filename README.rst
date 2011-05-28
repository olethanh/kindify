Kindify
=======

Kindify is a script to transform a single web page to a mobi ebook, while keeping the images displayed in the page.

It download the page via WGET, pass it through decruft (a python port of readability) to extract the main content, then finally pass it to mobigen.


Requirements
------------
   * decruft (dcramer version)
   * mobigen or kindlegen
   * wget

Configuration
-------------
Set the DESTDIR in the source code to the dir you want your generated ebook to be created

Usage
-----
kindify <url>

Author
------
Olivier Lê Thanh Duong <olivier@lethanh.be>
based on an idea from Laurent Peutch

Licence
-------
This code is licensed under the Do What The Fuck You Want To Public License (WTFPL) version 2.0
