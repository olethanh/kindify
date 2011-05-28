#!/usr/bin/python
# This code is distributed under the WTFPL
#  (c) Olivier Le Thanh Duong <olivier@lethanh.be>

from decruft import Document
import os
from sys import argv
import sys
import shutil
from subprocess import call

# Modify this to set the dir in which generated ebooks end up.
DESTDIR = os.path.expanduser("~/mobi-articles/")

# we remove gravatar domain because it long file name break havo with ebook-convert
WGET_CMD = "wget -nv -P %(dir)s --no-directories --no-host-directories --page-requisites --convert-links --adjust-extension --span-hosts --exclude-domains gravatar.com %(url)s"


def page(doc, url):
    #the summary method of decruft only contain a portion of the html page but no title header
    # this return a "proper" html page with a title so we can feed it to mobygen

    page = u"""
<html>
    <head>
        <title>%(title)s </title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <h1>%(title)s </h1>
        Original URL :<a href="%(url)s">%(url)s</a><br />
        <article>
            %(body)s
        </article>
    </body>
</html>
""" %  { 'title' : doc.title(), 'body' : doc.summary(), 'url': url }
    return page


if __name__ == '__main__':
    # create tempory dir
    tmpdir = os.tmpnam()
    os.mkdir(tmpdir)

    url = argv[1]
    # determine the filename wget used
    start, sep, end =  url.rpartition('/')
    if end == '':
        # if wget get a dir instead of a filename (if the last component of the path is /) it use index.html
        filename = 'index.html'
    else:
        # wget automaticallty add a .html if there wasn't one (courtesy of --adjust-extension)
        if end.endswith('.html'):
            filename = end
        else :
            filename = end + '.html'

    # determinate the name for the mobi file:
    if end == '':
        # if we had a dir, reseparate it to get the dir name
        start, sep, end =  start.rpartition('/')
        outname = end
    else:
        if end.endswith('.html'):
            start, sep, end =end.rpartition('.')
            outname = start
        else:
            outname = end
    outname += '.mobi'

    # download everything
    cmd = WGET_CMD % { 'dir': tmpdir, 'url': url }
    r = call(cmd, shell=True)
    if r != 0 and r !=8 and r!=3: #wget seems to return 8 if it can't retrieve all the files, happens with wikipedia
        # 3: Ignore if we can't download some links because the filename is too long, they are usually not very interesting
        sys.exit('Could not retrieve file with command %s  \n got return values : %s' % (cmd, r))

    # decruft the document, write it to cleaned.html
    f= file(os.path.join(tmpdir, filename))
    doc = Document(f.read(), debug=False)
    cleaned_page = page(doc, url).encode('utf-8','ignore')
    cleaned_filename = os.path.join(tmpdir, 'cleaned.html')
    out = file(cleaned_filename, 'w')
    out.write(cleaned_page)
    out.close()

    # convert it
    cmd = "mobigen %s -o %s" % (cleaned_filename, outname)
    print cmd
    #TODO : check for errors
    os.system(cmd)

    join = os.path.join
    shutil.move(join(tmpdir,outname), join(DESTDIR, outname))
    print join(DESTDIR, outname)
