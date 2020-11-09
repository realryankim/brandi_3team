import pymysql

from exceptions    import NotFoundError

class SellerDao:
    def insert_seller(self, seller_info, db_connection):
        """
        회원가입시 sellers테이블에 넣어줄 데이터
        Args:
            seller_info = {
                account_name        : 셀러 아이디,
                password            : 패스워드,
                name_english        : 영문 셀러명,
                name_korean         : 셀러명,
                cs_contact          : 고객센터 전화번호 ,
                seller_attribute_id : 셀러 속성 PK(쇼핑몰 마켓  로드샵  디자이너브랜드  제너럴브랜드  내셔널브랜드  뷰티),
                phone_number        : 담당자 전화번호
            }
            db_connection : 데이터베이스 객체
        
        Returns:
            seller_id : 생성된 셀러의 id

        Authors:
            jisunn0130@gmail.com(최지선)
            
        History:
            2020.10.28(최지선) : 초기 생성
        """

        with db_connection.cursor() as cursor:
            insert_account_query = """
            INSERT INTO accounts (
                account_type_id,
                account_name,
                password
            ) VALUES (
                2,
                %(sellerId)s,
                %(sellerPassword)s
            )
            """
            #account table 에 새로운 seller 저장
            cursor.execute(insert_account_query, seller_info)
            account_id = cursor.lastrowid

            if not account_id:
                raise NotFoundError("S000")

            seller_info['account_id'] = account_id
           
            insert_seller_query = """
            INSERT INTO sellers (
                account_id,
                seller_attribute_id,
                name_korean,
                name_english,
                cs_contact
            ) VALUES (
                %(account_id)s,
                %(sellerRadio)s,
                %(sellerName)s,
                %(sellerEnName)s,
                %(sellerTel)s
            )
            """
            #seller table 에 새로운 seller 의 정보 저장
            cursor.execute(insert_seller_query, seller_info)

            #새로 생성된 seller_id 
            seller_id = cursor.lastrowid

            #쿼리 실패했을 경우 에러 반환
            if not seller_id:
                raise NotFoundError("S000")
            
            #seller_info 에 seller_id 속성 부여 및 값 할당
            seller_info['seller_id'] = seller_id

            insert_contact_query = """
            INSERT INTO contacts (
                phone_number,
                seller_id
            ) VALUES (
                %(sellerPhone)s,
                %(seller_id)s
            )
            """
            #contact table 에 새로운 seller 의 정보 저장
            contact_info = cursor.execute(insert_contact_query, seller_info)

            #쿼리 실패했을 경우 에러 반환
            if not contact_info:
                raise NotFoundError("S000")
            return seller_id
    
    def get_account(self, seller_info, db_connection):
        """
        account table 에 중복된 아이디가 존재하는 지 확인 & 로그인 할 때 계정정보 불러오는 쿼리
        Args:
            seller_info = {
                account_name : 셀러 아이디
            }
            db_connection : 데이터베이스 객체
        
        Returns:
            existing_account : 저장된 셀러 계정정보 (id, 계정아이디, 비밀번호, 계정타입)

        Authors:
            jisunn0130@gmail.com(최지선)
            
        History:
            2020.10.28(최지선) : 초기 생성
        """
        with db_connection.cursor() as cursor:
            get_account_query = """
            SELECT id, account_name, password, account_type_id
            FROM accounts
            WHERE account_name=%(sellerId)s
            """
            cursor.execute(get_account_query, seller_info)
            return cursor.fetchone()
    
    def get_seller_id(self, db_connection, account_id):
        """
        로그인 데코레이터에서 토큰에 담긴 account_id 로 셀러 정보를 가져오는 쿼리
        Args:
            account_id : 셀러 계정 id
            db_connection : 데이터베이스 객체
        
        Returns:
            seller_id : 셀러 정보 id

        Authors:
            jisunn0130@gmail.com(최지선)
            
        History:
            2020.10.28(최지선) : 초기 생성
        """
        with db_connection.cursor() as cursor:
            get_seller_id_query = """
            SELECT sellers.id, sellers.is_delete
            FROM sellers
            LEFT JOIN accounts
            ON sellers.account_id = accounts.id
            WHERE account_id = %(account_id)s
            """
            cursor.execute(get_seller_id_query, account_id)
            return cursor.fetchone()
            
    def get_seller_data(self, seller_id, db_connection):
        print("seller_id >>>>", seller_id)
        return "seller_dao"