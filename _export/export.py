#!/usr/bin/env python

import sys
import subprocess
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+oursql://root@localhost/legiinternet')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Page(Base):
    __tablename__ = 'pages'

    uid = Column(Integer, primary_key=True)
    title = Column(String)


class Content(Base):
    __tablename__ = 'tt_content'

    uid = Column(Integer, primary_key=True)
    bodytext = Column(String)


class UrlCache(Base):
    __tablename__ = 'tx_realurl_urlencodecache'

    url_hash = Column(String, primary_key=True)
    page_id = Column(Integer)
    content = Column(String)


session = Session()


def get_data(url):
    page_id = (
        session.query(UrlCache.page_id)
        .filter_by(content=url)
        .scalar()
    )
    title = session.query(Page).get(page_id).title
    bodytext = session.query(Content).get(page_id).bodytext
    return (title, bodytext)


def export(url):
    (title, bodytext) = get_data(url)
    folder = url.rsplit('/', 1)[0]
    assert '..' not in folder
    subprocess.check_call(['mkdir', '-p', folder])
    with open(url, 'wb') as f:
        f.write('---\n')
        f.write('title: ' + json.dumps(title) + '\n')
        f.write('---\n')
        f.write(bodytext.encode('utf-8'))


export(sys.argv[1])
