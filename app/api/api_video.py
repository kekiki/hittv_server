from datetime import datetime
import random
from loguru import logger
from flask import json, request
from mysql.connector import connector
from api.video import Video
from api.response import response
import api.constants as constants

@logger.catch()
def main():
    action = request.args.get(constants.KEY)
    logger.info(f'receive request [{action}]')

    if action == constants.HOME_LIST:
        data_list = __home_list__()
        return response(code=0, data=data_list, msg="OK")
    
    if action == constants.CATEGORY:
        data = __category__()
        return response(code=0, data=data, msg="OK")
    
    if action == constants.CATEGORY_LIST:
        type = request.args.get('type')
        story = request.args.get('story')
        year = request.args.get('year')
        status = request.args.get('status')
        size = request.args.get('size')
        page = request.args.get('page')
        data = __category_list__(type, story, year, status, int(page), int(size))
        return response(code=0, data=data, msg="OK")
    
    if action == constants.SEARCH_LIST:
        keyword = request.args.get('keyword')
        size = request.args.get('size')
        page = request.args.get('page')
        data_list = __search_list__(keyword, int(page), int(size))
        return response(code=0, data=data_list, msg="OK")
    
    if action == constants.SEARCH_HOT_LIST:
        data_list = __search_hot_list__()
        return response(code=0, data=data_list, msg="OK")
    
    if action == constants.VIDEO_NODE_LIST:
        id = request.args.get('id')
        data = __fetch_video_node_list__(int(id))
        return response(code=0, data=data, msg="OK")
    
    if action == constants.VIDEO_PLAY_INFO:
        id = request.args.get('id')
        node = request.args.get('node')
        sort = request.args.get('sort')
        data = __fetch_video_play_info__(int(id), node, int(sort))
        return response(code=0, data=data, msg="OK")

    return response(code=-1, msg="Invalid action")

### 首页

def __home_list__():
    new_video_list = __fetch_newest_video_list__(limit=12)
    new_tv_list = __fetch_newest_video_list__(type='电视剧', limit=12)
    new_film_list = __fetch_newest_video_list__(type='电影', limit=12)
    new_anime_list = __fetch_newest_video_list__(type='动漫', limit=12)

    return [
        __home_list_item_dict__(
            style=constants.STYLE_VIDEO_GRID_1,
            title='正在热播',
            moreTitle='更多热播',
            list=new_video_list,
        ),
        __home_list_item_dict__(
            style=constants.STYLE_VIDEO_GRID_1,
            title='热播电视剧',
            moreTitle='更多电视剧',
            list=new_tv_list,
        ),
        __home_list_item_dict__(
            style=constants.STYLE_VIDEO_GRID_1,
            title='热播电影',
            moreTitle='更多电影',
            list=new_film_list,
        ),
        __home_list_item_dict__(
            style=constants.STYLE_VIDEO_GRID_1,
            title='热播动漫',
            moreTitle='更多动漫',
            list=new_anime_list,
        ),
    ]

def __home_list_item_dict__(style, title, moreTitle, list):
    return {
        'style': style,
        'title': title,
        'moreTitle': moreTitle,
        'list': list,
        }

def __fetch_newest_video_list__(type = None, limit: int = 6) -> list:
    video_list = []
    if type is None:
        result = connector.query(f'SELECT * FROM `tv` ORDER BY `created_at` DESC LIMIT {limit};')
    else:
        result = connector.query(f"SELECT * FROM `tv` WHERE `type` = '{type}' ORDER BY `created_at` DESC LIMIT {limit};")
    for row in result:
        video = Video(row)
        video_list.append(video.toJson())
    return video_list

### 分类

def __category__():
    year_list = ['全部',]
    year = datetime.now().year
    for i in range(10):
        year_list.append(str(year-i))
    year_list.append('更早')

    return {
        'typeList': ['全部', '电视剧', '电影', '动漫'],
        'storyList': ['全部', '动作', '犯罪', '剧情', '爱情', '古装', '历史', '恐怖', '商战', '战争', '喜剧', '家庭', '奇幻', '情景'],
        'yearList': year_list,
        'statusList': ['全部', '连载', '完结'],
    }

def __category_list__(type: str, story: str, year: str, status: str, page: int = 0, size: int = 20):
    video_list = []
    sql_type= f"WHERE `type` = '{type}'" if type != '全部' else f"WHERE `type` != '{type}'"
    sql_story = f"AND `tags` LIKE '%{story}%'" if story != '全部' else ""
    sql_year = ""
    if year == '更早':
        sql_year = f"AND `publish_date` < {datetime.now().year - 10}"
    else:
        sql_year = f"AND `publish_date` = '{year}'" if year != '全部' else ""
    sql_status = f"AND `is_end` = {int(status == '完结')}" if status != '全部' else ""

    result = connector.query(
        f'''
        SELECT * FROM `tv` {sql_type} {sql_story} {sql_year} {sql_status}
        ORDER BY `created_at` DESC LIMIT {page*size},{size};
        ''')
    if result:
        for row in result:
            video = Video(row)
            video_list.append(video.toJson())
    return video_list

### 搜索

def __search_hot_list__() -> list[str]:
    data_list = []
    result = connector.query(f'SELECT * FROM `tv` ORDER BY `created_at` DESC LIMIT 20;')
    for row in result:
        video = Video(row)
        if not video.title in data_list:
                data_list.append(video.title)
    random.shuffle(data_list)
    return data_list

def __search_list__(keyword: str, page: int = 0, size: int = 20) -> list[str]:
    video_list = []
    result = connector.query(
        f'''
        SELECT * FROM `tv` WHERE `title` LIKE '%{keyword}%' 
        OR `directors` LIKE '%{keyword}%' 
        OR `scriptwriters` LIKE '%{keyword}%' 
        OR `actors` LIKE '%{keyword}%' 
        OR `tags` LIKE '%{keyword}%' 
        ORDER BY `created_at` DESC LIMIT {page*size},{size};
        ''')
    if result:
        for row in result:
            video = Video(row)
            video_list.append(video.toJson())
    return video_list

## 播放信息
def __fetch_video_node_list__(id: int) -> list:
    node_list = []
    result = connector.query(f"SELECT `node`,max(sort) FROM `tv_{id}` GROUP BY `node`;")
    for row in result:
        node_list.append({
            'node': row[0],
            'maxSort': row[1],
        })
    return node_list

def __fetch_video_play_info__(id: int, node: str, sort: int = 1) -> dict:
    result = connector.query(f"SELECT `url` FROM `tv_{id}` WHERE `node` = '{node}' AND `sort` = {sort};")
    return {
        'node': node,
        'sort': sort,
        'url': result[0][0],
        'position': 0,
    }
    