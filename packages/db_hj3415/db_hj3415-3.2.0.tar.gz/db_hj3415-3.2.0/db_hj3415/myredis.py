"""
redis 서버를 이용해서 mongodb의 데이터를 캐시한다.
데이터의 캐시 만료는 데이터를 업데이트 시키는 모듈인 scraper_hj3415에서 담당하고
여기서 재가공해서 만들어지는 데이터는 만료기간을 설정한다.
장고에서 필요한 데이터를 보내는 기능이 주임.
"""

import redis
from db_hj3415 import mymongo
import json
from utils_hj3415 import utils


def connect_to_redis(addr: str):
    conn_str = f"Connect to Redis ..."
    print(conn_str, f"Server Addr : {addr}")
    return redis.Redis(host=addr, port=6379, db=0)


class Base:
    from db_hj3415 import cli as db_cli
    redis_client: redis.Redis = connect_to_redis(db_cli.load_redis_addr())

    def __init__(self):
        if Base.redis_client is None:
            raise ValueError("myredis.Base.redis_client has not been initialized!")

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


class Corps(Base):
    COLLECTIONS = mymongo.Corps.COLLECTIONS

    def __init__(self, code: str = '', page: str = ''):
        self.code_page = code + '.' + page
        self.code = code
        self.page = page
        # redis에서 name으로 사용하는 변수의 기본으로 문미에 문자열을 추가로 첨가해서 사용하는 역할을 함.
        super().__init__()

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        self.code_page = code + self.code_page[6:]
        # print('code_page 변경 :', self.code_page)
        self._code = code

    @property
    def page(self) -> str:
        return self._page

    @page.setter
    def page(self, page: str):
        assert page in self.COLLECTIONS, f'Invalid value : {page}({self.COLLECTIONS})'
        self.code_page = self.code_page[:7] + page
        # print('code_page 변경 :', self.code_page)
        self._page = page

    @classmethod
    def list_all_codes(cls) -> list:
        """
        redis_name = 'all_codes'
        :return:
        """
        redis_name = 'all_codes'

        try:
            cached_data = cls.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            codes = []
            for db_name in mymongo.Corps.list_db_names():
                if utils.is_6digit(db_name):
                    codes.append(db_name)
            data = sorted(codes)

            if data:
                # 데이터를 Redis에 캐싱
                cls.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - krx 리프레시할때 제거되도록 개선..
                # cls.redis_client.expire(redis_name, 3600)
            # print("list_all_codes() - Mongo에서 데이터 가져오기")
            return data
        else:
            # print("list_all_codes() - Redis 캐시에서 데이터 가져오기")
            return json.loads(cached_data)

    @classmethod
    def list_all_codes_names(cls) -> dict:
        """
        redis_name = 'all_codes_names'
        :return:
        """
        redis_name = 'all_codes_names'

        try:
            cached_data = cls.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            corps = {}
            for code in cls.list_all_codes():
                corps[code] = mymongo.Corps.get_name(code)
            data = corps

            if data:
                # 데이터를 Redis에 캐싱
                cls.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - krx 리프레시할때 제거되도록 개선..
                # cls.redis_client.expire(redis_name, 3600)
            print("list_all_codes_names() - Mongo에서 데이터 가져오기")
            return data
        else:
            print("list_all_codes_names() - Redis 캐시에서 데이터 가져오기")
            return json.loads(cached_data)

    def _list_rows(self, func: mymongo.Corps, redis_name:str):
        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = func.list_rows()
            # import pprint
            # pprint.pprint(data)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # cls.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기")
            return json.loads(cached_data)


class C101(Corps):
    def __init__(self, code: str):
        super().__init__(code, 'c101')

    def get_recent(self) -> dict:
        # code_page 앞 11글자가 코드와 c101 페이지임.
        redis_name = self.code_page[:11] + '_recent'

        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = mymongo.C101(self.code).get_recent(merge_intro=True)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c101 업데이트할때 제거되도록..
                # cls.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기")
            return json.loads(cached_data)


class C103(Corps):
    PAGES = mymongo.C103.PAGES

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q', 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y'
        """
        super().__init__(code, page)

    def list_rows(self):
        # redis_name 앞 17글자가 코드와 c103 페이지임.
        redis_name = self.code_page[:17] + '_rows'
        return super()._list_rows(mymongo.C103(self.code, self.page), redis_name)


class C104(Corps):
    PAGES = mymongo.C104.PAGES

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c104y', 'c104q
        """
        super().__init__(code, page)

    def list_rows(self):
        # redis_name 앞 12글자가 코드와 c104 페이지임.
        redis_name = self.code_page[:12] + '_rows'
        return super()._list_rows(mymongo.C104(self.code, self.page), redis_name)


class C106(Corps):
    PAGES = mymongo.C106.PAGES

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c106y', 'c106q
        """
        super().__init__(code, page)

    def list_rows(self):
        # redis_name 앞 12글자가 코드와 c104 페이지임.
        redis_name = self.code_page[:12] + '_rows'
        return super()._list_rows(mymongo.C106(self.code, self.page), redis_name)


class C108(Corps):
    def __init__(self, code: str):
        """
        :param code:
        """
        super().__init__(code, 'c108')

    def list_rows(self):
        # redis_name 앞 12글자가 코드와 c104 페이지임.
        redis_name = self.code_page[:11] + '_rows'
        return super()._list_rows(mymongo.C108(self.code), redis_name)



