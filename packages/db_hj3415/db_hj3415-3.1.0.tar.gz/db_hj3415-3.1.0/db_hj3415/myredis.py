import redis
from db_hj3415 import mymongo
import json


def connect_to_redis(addr: str):
    conn_str = f"Connect to Redis ..."
    print(conn_str, f"Server Addr : {addr}")
    return redis.Redis(host=addr, port=6379, db=0)


class Base:
    from db_hj3415 import cli as db_cli
    redis_client: redis.Redis = connect_to_redis(db_cli.load_redis_addr())

    def __init__(self, name: str = ''):
        self.redis_name = name

    @classmethod
    def delete(cls, redis_name: str):
        """
        redis_name 에 해당하는 키/값을 삭제하며 원래 없으면 아무일 없음
        :param redis_name:
        :return:
        """
        # print(Redis.list_redis_names())
        cls.redis_client.delete(redis_name)
        # print(Redis.list_redis_names())

    @classmethod
    def delete_all_with_pattern(cls, pattern: str):
        """
        pattern에 해당하는 모든 키를 찾아서 삭제한다.
        :param pattern: ex) 005930.c101* - 005930.c101로 시작되는 모든키 삭제
        :return:
        """
        # print(Redis.list_redis_names())
        # SCAN 명령어를 사용하여 패턴에 맞는 키를 찾고 삭제
        cursor = '0'
        while cursor != 0:
            cursor, keys = cls.redis_client.scan(cursor=cursor, match=pattern, count=1000)
            if keys:
                cls.redis_client.delete(*keys)
        # print(Redis.list_redis_names())

    @classmethod
    def list_redis_names(cls) -> list:
        return cls.redis_client.keys('*')


class Corps(mymongo.Corps, Base):
    def __init__(self, code: str = '', page: str = ''):
        if mymongo.Base.mongo_client is None:
            raise ValueError("mymongo.Base.mongo_client has not been initialized!")
        if Base.redis_client is None:
            raise ValueError("myredis.Base.mongo_client has not been initialized!")
        mymongo.Corps.__init__(self, code, page)
        redis_name = code + '.' + page
        Base.__init__(self, redis_name)

    @classmethod
    def list_all_codes(cls) -> list:
        redis_name = 'all_codes'

        try:
            cached_data = cls.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = mymongo.Corps.list_all_codes()
            if data:
                # 데이터를 Redis에 캐싱
                cls.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨
                cls.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기")
            return json.loads(cached_data)


class C101(mymongo.C101, Base):
    def __init__(self, code: str):
        if mymongo.Base.mongo_client is None:
            raise ValueError("mymongo.Base.mongo_client has not been initialized!")
        if Base.redis_client is None:
            raise ValueError("myredis.Base.mongo_client has not been initialized!")
        mymongo.C101.__init__(self, code)
        Base.__init__(self)
        self.set_redis_name()

    def set_redis_name(self, *args):
        """
        redis의 저장 이름값을 설정하며 기본 코드명.c101에 접미사를 추가할수 있다.
        :param args: 접미사 추가시 코드명.c101_접미사
        :return:
        """
        self.redis_name = self.code + '.' + 'c101'
        for arg in args:
            self.redis_name += '_' + arg

    def get_recent(self, merge_intro=False) -> dict:
        if merge_intro:
            self.set_redis_name('recent', 'merged')
        else:
            self.set_redis_name('recent')

        try:
            cached_data = self.redis_client.get(self.redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = super().get_recent(merge_intro=merge_intro)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(self.redis_name, json.dumps(data))
                # 10분후 키가 자동으로 제거됨
                self.redis_client.expire(self.redis_name, 600)
            print("Mongo에서 데이터 가져오기")
            return data
        else:
            # print("Redis 캐시에서 데이터 가져오기")
            return json.loads(cached_data)






