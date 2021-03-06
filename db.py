import logging
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()
Session = sessionmaker()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def db_init():
	global session
	logger.info('db_init')
	engine = create_engine('sqlite:///ids.db', connect_args={'check_same_thread': False})
	Session.configure(bind=engine)
	Base.metadata.create_all(engine)
	session = Session()

def add_entry(Object):
	logger.info('db:add_entry')
	logger.info(Object)
	session.add(Object)
	try:
		session.commit()
	except exc.SQLAlchemyError as ex:
		logger.info(ex)
		session.rollback()
		logger.info('session rolled back')
		return False
	else:
		logger.info('success')
		return True

def rollback_db():
	logger.info('undo_db_change')
	sesson.rollback()
	logger.info('session rolled back')

def get_row_count(Object):
	logger.info('get_row_count')
	rows = session.query(Object).count()
	return rows

def get_first_row(Object):
	logger.info('get_first_row')
	row = session.query(Object).order_by('id').first()
	return row

def get_last_row(Object):
	logger.info('get_last_row')
	row = session.query(Object).order_by(desc('id')).first()
	return row

def get_all_rows(Object):
	rows = session.query(Object).all()
	return rows

def get_rows_with_range(Object, field, start, end):
	rows = session.query(Object).filter(field>=start, field<=end).all()
	return rows

def get_rows(Object, field, value):
	logger.info('get_rows')
	rows = session.query(Object).filter(field == value).all()
	return rows

def get_row_for_object(Object, field, value):
	logger.info('get_row_for_object')
	try:
		row = session.query(Object).filter(field == value).order_by('id').one()
		logger.info(row)
	except NoResultFound:
		logger.info('NoResultFound')
		return None
	
	return row

def get_first_row_for_object(Object, field, value):
	logger.info('get_first_row_for_object')
	row = session.query(Object).filter(field == value).order_by('id').first()
	logger.info('row: ' + row)
	return row

def get_last_row_for_object_with_value(Object, field, value):
	logger.info('get_last_row_for_object_with_value')
	row = session.query(Object).filter(field == value).order_by(desc('id')).first()
	return row

def update_arbitrary_row(Object, query_key, query_value, update_column, new_column_value):
    logger.info('update_arbitrary_row')
    row = session.query(Object).filter_by(**{query_key:query_value}).first()
    logger.info(row)

    kwargs = {update_column: new_column_value}
    for key, value in kwargs.items():
        setattr(row, key, value)

    result = session.commit()
    logger.info(result)
    return result

def delete_row(Object, field, value):
	logger.info('delete_row')
	row = session.query(Object).filter(field == value).order_by('id').first()
	if row is None:
		return False
	else:
		result = session.query(Object).filter(field == value).delete()
		session.commit()
		return result
