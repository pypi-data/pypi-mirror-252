import os

# Get values from environment variables if available, otherwise use defaults
DB_URI = os.getenv('DB_URI', 'steintranetrd.ds.jdsu.net')
DB_login = os.getenv('DB_login', 'fibermarkuser')
DB_password = os.getenv('DB_password', 'users123')
DB_name = os.getenv('DB_name', 'FiberMarkDatabase')