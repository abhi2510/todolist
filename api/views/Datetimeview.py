from datetime import datetime
import pytz


def get_current_time():
	now_date = datetime.now(pytz.timezone('UTC'))
	now_date = now_date.astimezone(pytz.timezone('Asia/Kolkata'))
	now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
	now_date = datetime.strptime(now_date,'%Y-%m-%d %H:%M:%S')
	return now_date