from viavi.fibermark.db_utils.connect import create_session

TEST_DB_URI = "steintranetrd.ds.jdsu.net"
TEST_DB_login = "fibermarkuser"
TEST_DB_password = "users123"
TEST_DB_name = "FiberMarkDatabaseTest"

test_db_engine, test_db_session = create_session(
    f"mysql+pymysql://{TEST_DB_login}:{TEST_DB_password}@{TEST_DB_URI}/{TEST_DB_name}?charset=utf8mb4"
)
