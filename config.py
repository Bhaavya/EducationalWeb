class Config (object):
    """
    Initializes Table object
    """

    def __init__(self):
        # initialize table name, schema and load data
        self.env = "dev"
        self.base_url = "http://localhost:8097/"
        self.target_url = "http://localhost:8097/"
        self.pdf_url = "http://localhost:8889"
        self.local_url= "http://localhost:8097/"
        self.app_host = 'localhost'
        self.app_port = 8097
        self.is_local_srv = False
