#!/usr/bin/env python
import re
import os
import math
import shutil

from jinja2 import FileSystemLoader, Template
from jinja2.environment import Environment
from PIL import Image

from data import articles, photo_data

def main():
    env = Environment()
    env.loader = FileSystemLoader('.')

    html_dir = "compiled_html/"

    if not os.path.exists(html_dir):
        os.makedirs(html_dir)

    copy_dir(html_dir, 'assets')

    # Comment this line out to make the script run way faster
    # process_images(html_dir)

    with open(html_dir + 'index.html', 'w+') as out_file:
        contents = env.get_template('index.html').render().encode('utf-8')
        out_file.write(contents)

    translations = {ord(u'\u00a0'): u' ',
                    ord(u'\u2018'): u"&lsquo;",
                    ord(u'\u2019'): u"&rsquo;",
                    ord(u'\u201c'): u'&ldquo;',
                    ord(u'\u201d'): u'&rdquo;',
                    ord(u'\uc3a9'): u'&eacute;',
                    ord(u'\u2013'): u'&ndash;',
                    ord(u'\u2014'): u'&mdash;',
                    ord(u'\u00ca'): u'&ecirc;'}

    photos = []
    for img in photo_data:
        photos.append({
            'path': img[0].decode('utf-8').translate(translations),
            'caption': img[1].decode('utf-8').translate(translations),
            'contributors': img[2].decode('utf-8').translate(translations),
        })
    photos_left = photos[:int(len(photos)/2)-2]
    photos_right = photos[int(len(photos)/2)-2:]

    path = '%s%s' % (html_dir, 'article/year-in-photos/')
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    with open(path + 'index.html', 'w+') as out_file:
        contents = env.get_template('photos.html').render(photos_left=photos_left, photos_right=photos_right).encode('utf-8')
        out_file.write(contents)

    good_articles = []
    for art in articles:
        good_articles.append({
            'title': art[0].decode('utf-8').translate(translations),
            'slug': art[1],
            'subtitle': art[2].decode('utf-8').translate(translations),
            'contributor_line': art[3].decode('utf-8').translate(translations),
            'text': art[4].decode('utf-8').translate(translations)
        })

    for article in good_articles:
        print('COMPILING {0}'.format(article['title']))
        path = '%s%s%s%s' % (html_dir, 'article/', article['slug'], '/')

        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

        context = {'article': article}

        with open(path + 'index.html', 'w+') as out_file:
            contents = env.get_template('article.html').render(context).encode('utf-8')
            out_file.write(contents)
        print 'DONE'

    # for hood in hoods:
    #     for house in hood.houses:
    #         print 'COMPILING {0}...'.format(house),
    #         path = html_dir + house.name.lower() + '/'

    #         if os.path.exists(path):
    #             shutil.rmtree(path)
    #         os.makedirs(path)

    #         context = {'house': house}
    #         with open(path + 'index.html', 'w+') as out_file:
    #             contents = env.get_template('jinja2/individual.html.jinja2').render(context).encode('utf-8')
    #             out_file.write(contents)
    #         print 'DONE'

    print 'FINISHED!'

def copy_dir(html_dir, dname):
    print 'COPYING {0} to {1}...'.format(dname, html_dir + dname),
    if os.path.exists(html_dir + dname):
        shutil.rmtree(html_dir + dname)
    shutil.copytree(dname, html_dir + dname)
    print 'DONE'


def process_images(html_dir):
    if os.path.exists(html_dir + 'img'):
        shutil.rmtree(html_dir + 'img')
    os.makedirs(html_dir + 'img')
    shutil.copy2('img/logo.svg', '{0}img/logo.svg'.format(html_dir))
    shutil.copy2('img/arrow.png', '{0}img/arrow.png'.format(html_dir))

    i = Image.open('img/wide.jpg')
    height = int((float(1600) / i.size[0]) * i.size[1])
    i = i.resize((1600, height), Image.ANTIALIAS)
    i.save('{0}img/wide.jpg'.format(html_dir))

    for hood in hoods:
        for house in hood.houses:
            os.makedirs('{0}img/{1}'.format(html_dir, house.name.lower()))

            i = Image.open('img/{0}/box.jpg'.format(house.name.lower()))
            i = i.resize((600, 600), Image.ANTIALIAS)
            i.save('{0}img/{1}/box.jpg'.format(html_dir, house.name.lower()))

            if hood.published:
                os.makedirs('{0}img/{1}/thumbs'.format(html_dir, house.name.lower()))
                os.makedirs('{0}img/{1}/thumbs_full'.format(html_dir, house.name.lower()))

                i = Image.open('img/{0}/wide.jpg'.format(house.name.lower()))
                height = int((float(1600) / i.size[0]) * i.size[1])
                i = i.resize((1600, height), Image.ANTIALIAS)
                i.save('{0}img/{1}/wide.jpg'.format(html_dir, house.name.lower()))

                imgs = [f for f in 
                        os.listdir('img/{0}/thumbs'.format(house.name.lower()))
                        if f[-4:].lower() == '.jpg']

                for f in imgs:
                    f_full = 'img/{0}/thumbs/{1}'.format(house.name.lower(), f)
                    print 'PROCESSING {0}...'.format(f_full),
                    i = Image.open(f_full).resize((530, 530), Image.ANTIALIAS)
                    i.save('{0}img/{1}/thumbs/{2}'.format(html_dir, house.name.lower(), f))
                    print 'DONE'


                imgs_full = [f for f in 
                        os.listdir('img/{0}/thumbs'.format(house.name.lower()))
                        if f[-4:].lower() == '.jpg']

                for f in imgs_full:
                    f_full = 'img/{0}/thumbs_full/{1}'.format(house.name.lower(), f)
                    print 'PROCESSING {0}...'.format(f_full),
                    i = Image.open(f_full)
                    height = int((float(800) / i.size[0]) * i.size[1])
                    i = i.resize((800, height), Image.ANTIALIAS)
                    i.save('{0}img/{1}/thumbs_full/{2}'.format(html_dir, 
                            house.name.lower(), f))
                    print 'DONE'

if __name__ == '__main__':
    main()
