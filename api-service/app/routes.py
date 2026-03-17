from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from app.db_dal import MysqlDal
from app.db_connection import MysqlManager
import matplotlib.pyplot as plt
import numpy as np
import io

# ------------------------------------------------------------
# UTILS
# ------------------------------------------------------------
def get_mysql_manager(request: Request):
    """
    Return app instance
    """
    return request.app.state.mysql_manager

def extract_lat_and_lon(coords: dict):
    """
    Simplfy MySQL query result to tuple of lists for matplotlib presentation
    """
    lat = [coord['reported_lat'] for coord in coords]
    lon = [coord['reported_lon'] for coord in coords]
    return lat, lon

# ------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------

router =  APIRouter()

# 1
@router.get('/target/get-quality-targets')
def get_quality_targets(mysql_manager: MysqlManager = Depends(get_mysql_manager)):
    return MysqlDal.get_quality_targets(mysql_manager.get_cnx())

# 2
@router.get('/target/get-signal-type-count')
def get_signal_type_count(mysql_manager: MysqlManager = Depends(get_mysql_manager)):
    return MysqlDal.get_signal_type_count(mysql_manager.get_cnx())

# 3
@router.get('/target/get-new-targets')
def get_new_targets(mysql_manager: MysqlManager = Depends(get_mysql_manager)):
    return MysqlDal.get_new_targets(mysql_manager.get_cnx())

# 4
@router.get('/target/get-dangerous-targets')
def get_dangerous_targets(mysql_manager: MysqlManager = Depends(get_mysql_manager)):
    return MysqlDal.get_dangerous_targets(mysql_manager.get_cnx())

# 5
@router.get('/target/get-target-route/{entity_id}')
def get_target_route(entity_id: str, mysql_manager: MysqlManager = Depends(get_mysql_manager)):
    target_coords = MysqlDal.get_target_coords(entity_id, mysql_manager.get_cnx())
    lat_list, lon_list = extract_lat_and_lon(target_coords)

    xpoints = np.array(lon_list)
    ypoints = np.array(lat_list)
    plt.plot(xpoints, ypoints)

    plt.scatter(lon_list[0], lat_list[0], color='g')
    plt.scatter(lon_list[-1], lat_list[-1], color='r')

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
