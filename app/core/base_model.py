from app.core.database import Base

"""
Imports newly created models here to deal with 
alembic functionalities and alembic revision file.
"""
from app.apis.clients.models.client import *
from app.apis.clients.models.address import *
from app.apis.clients.models.app_registry import *
from app.apis.clients.models.poc import *
from app.apis.users.models import *
from app.apis.storages.models import *
from app.apis.activities.models import *
