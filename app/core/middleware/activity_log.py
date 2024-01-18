import os
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import settings


class ActivityLogMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # get request data
        current_date_time = datetime.now()
        formatted_date = current_date_time.strftime("%Y-%m-%d")
        formatted_time = current_date_time.strftime("%H:%M")

        log_info = "Level:INFO" \
            + " Date:" + formatted_date \
            + " Time:" + formatted_time \
            + " URL:" + request.url.path \
            + " Method:" + request.method \
            + " Domain:" + request.headers.get("host", '') \
            + " IP-Address:" + request.client.host \
            + " UserType:" + request.headers.get('user-type', '') \
            + " RequesterId:" + request.headers.get('user-id', '')

        response = await call_next(request)

        # get response data
        end_time = datetime.now()
        response_time = (end_time - current_date_time).total_seconds()
        log_info += " ResponseTime:" + \
            str(response_time) + " Status:" + str(response.status_code) + '\n'

        # write log data
        log_path, filename = self.get_log_path()
        self.write_log(log_info=log_info, log_path=log_path, filename=filename)

        return response

    def get_log_path(self):
        current_date = datetime.now()
        month_string = current_date.strftime("%B")
        year = current_date.year
        log_filename = f"{month_string}_{year}_activity_log.txt"
        log_path = os.path.join(settings.ROOT_STORAGE_DIR, 'ActivityLog')
        return log_path, log_filename

    def write_log(self, log_info=None, log_path=None, filename=None):

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        with open(os.path.join(log_path, filename), 'a') as logfile:
            # write format
            logfile.write(log_info)
