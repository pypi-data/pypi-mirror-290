import pandas as pd
from opensearchpy import OpenSearch

from echoss_fileformat import FileUtil, get_logger, set_logger_level

logger = get_logger("echoss_query")


class ElasticSearch:
    def __init__(self, conn_info: str or dict):
        """
        Args:
            conn_info : configration dictionary
            ex) conn_info = {
                                'elastic':
                                    {
                                        'user'  : str(user),
                                        'passwd': str(pw),
                                        'cloud_id'  : str(id),
                                        'index' : str(index)
                                    }
                            }
        """
        if isinstance(conn_info, str):
            conn_info = FileUtil.dict_load(conn_info)
        elif not isinstance(conn_info, dict):
            raise TypeError("ElasticSearch support type 'str' and 'dict'")
        required_keys = ['user', 'passwd', 'host', 'port', 'index']
        if (len(conn_info) > 0) and ('elastic' in conn_info) and all(k in conn_info['elastic'] for k in required_keys):
            self.user = conn_info['elastic']['user']
            self.passwd = conn_info['elastic']['passwd']
            self.host = conn_info['elastic']['host']
            self.port = conn_info['elastic']['port']
            self.index_name = conn_info['elastic']['index']

            self.hosts = [{
                'host': self.host,
                'port': self.port
            }]

            self.auth = (self.user, self.passwd)
        else:
            logger.debug(f"[Elastic] config info not exist")

    def __str__(self):
        return f"ElasticSearch(hosts={self.hosts}, index={self.index_name})"

    def _connect_es(self):
        """
        ElasticSearch Cloud에 접속하는 함수
        """
        self.es = OpenSearch(
            hosts=self.hosts,
            http_compress=True,
            http_auth=self.auth,
            use_ssl=True,
            verify_certs=True,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )
        return self.es

    def ping(self) -> bool:
        """
        Elastic Search에 Ping
        """
        with self._connect_es() as conn:
            return conn.ping()

    def info(self) -> dict:
        """
        Elastic Search Information
        """
        with self._connect_es() as conn:
            return conn.info()

    def exists(self, id: str or int = None) -> bool:
        """
        Args:
            index(str) : 확인 대상 index \n
            id(str) : 확인 대상 id \n
        Returns:
            boolean
        """
        with self._connect_es() as conn:
            return conn.exists(index=self.index_name, id=id)

    def search_list(self, body: dict) -> list:
        """
        Returns:
            result(list) : search result
        """
        with self._connect_es() as conn:
            result = conn.search(
                index=self.index_name,
                body=body
            )
        return result['hits']['hits']

    def search(self, body: dict) -> list:
        """
        Returns:
            result(list) : search result
        """
        with self._connect_es() as conn:
            result = conn.search(
                index=self.index_name,
                body=body
            )
        return result

    def search_field(self, field: str, value: str) -> list:
        """
        해당 index, field, value 값과 비슷한 값들을 검색해주는 함수 \n
        Args:
            field(str) : 검색 대상 field \n
            value(str) : 검색 대상 value \n
        Returns:
            result(list) : 검색 결과 리스트
        """
        with self._connect_es() as conn:
            result = conn.search(
                index=self.index_name,
                body={
                    'query': {
                        'match': {field: value}
                    }
                }
            )
        return result['hits']['hits']

    def get(self, id: str or int) -> dict:
        """
        index에서 id와 일치하는 데이터를 불러오는 함수 \n
        Args:
            id(str) : 가져올 대상 id \n
        Returns:
            result(dict) : 결과 데이터

        """
        with self._connect_es() as conn:
            return conn.get(index=self.index_name, id=id)

    def get_source(self, id: str or int) -> dict:
        """
        index에서 id와 일치하는 데이터의 소스만 불러오는 함수 \n
        Args:
            id(str) : 가져올 대상 id \n
        Returns:
            result(dict) : 결과 데이터

        """
        with self._connect_es() as conn:
            return conn.get_source(index=self.index_name, id=id)

    def create(self, id: str or int, body: dict):
        """
        index에 해당 id로 새로운 document를 생성하는 함수 \n
        (기존에 있는 index에 데이터를 추가할 때 사용) \n
        Args:
            id(str) : 생성할 id \n
        Returns:
            result(str) : 생성 결과
        """
        with self._connect_es() as conn:
            return conn.create(index=self.index_name, id=id, body=body)

    def index(self, index: str, body: dict, id: str or int = None) -> str:
        """
        index를 생성하고 해당 id로 새로운 document를 생성하는 함수 \n
        (index를 추가하고 그 내부 document까지 추가하는 방식) \n
        Args:
            index(str) : 생성할 index name \n
            id(str) : 생성할 id \n
            body(dict) : 입력할 json 내용
        Returns:
            result(str) : 생성 결과
        """
        with self._connect_es() as conn:
            if id == None:
                return conn.index(index=index, body=body)
            else:
                return conn.index(index=index, id=id, body=body)

    def update(self, id: str or int, body: dict) -> str:
        """
        기존 데이터를 id를 기준으로 body 값으로 수정하는 함수 \n
        Args:
            id(str) : 수정할 대상 id \n
        Returns:
            result(str) : 처리 결과
        """
        with self._connect_es() as conn:
            return conn.update(index=self.index_name, id=id, body=body)

    def delete(self, id: str or int) -> str:
        """
        삭제하고 싶은 데이터를 id 기준으로 삭제하는 함수 \n
        Args:
            id(str) : 삭제 대상 id \n
        Returns:
            result(str) : 처리 결과
        """
        with self._connect_es() as conn:
            return conn.delete(index=self.index_name, id=id)

    def delete_index(self, index):
        """
        인덱스를 삭제하는 명령어 신중하게 사용해야한다.\n
        Args:
            index(str) : 삭제할 index
        Returns:
            result(str) : 처리 결과
        """
        with self._connect_es() as conn:
            return conn.indices.delete(index=index)
