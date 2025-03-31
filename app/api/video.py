class Video(object):

    def __init__(self, row):
        self.id: int = row[0]
        self.title: str = row[1]
        self.type: str = row[2]
        self.cover: str = row[3]
        self.directors: str = row[4]
        self.scriptwriters: str = row[5]
        self.actors: str = row[6]
        self.publish_date: str = row[7]
        self.introduce: str = row[8]
        self.tags: str = row[9]
        # self.node_names: list = row[10]
        # self.node_ids: list = row[11]
        self.max_sort: int = row[12]
        self.is_end: bool = row[13]
        # self.created_at: int = row[14]

    def toJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'cover': self.cover,
            'directors': self.directors,
            'scriptwriters': self.scriptwriters,
            'actors': self.actors,
            'publishDate': self.publish_date,
            'introduce': self.introduce,
            'tags': self.tags,
            'maxSort': self.max_sort,
            'isEnd': self.is_end,
            # 'createdAt': self.created_at,
        }