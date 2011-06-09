import gettext
_ = gettext.gettext

import ConfigParser

class Config():
    sql = {}
    main = {}

    def __init__(self):
        self.cfg = ConfigParser.RawConfigParser()
        self.cfg.read("ticket.cfg")

        self.backup_file = self.cfg.get("main", "backup_file")
        self.db_type = self.cfg.get("db", "type")
        self.db_host = self.cfg.get("db", "host")
        self.db_winkas = self.cfg.get("db", "winkas_db")
        self.db_ticket = self.cfg.get("db", "ticket_db")
        self.db_user = self.cfg.get("db", "user")
        self.db_pass = self.cfg.get("db", "pass")
        self.db_charset = self.cfg.get("db", "charset")
