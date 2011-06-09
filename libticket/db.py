from qtreactor import qt4reactor
qt4reactor.install()
from twisted.internet import reactor
from twisted.enterprise import adbapi

class Db:
    def __init__(self, dbtype, host, user, pwd, winkas, ticket):

        self.dbtype = dbtype
        self.host = host
        self.port = -1
        self.user = user
        self.pwd = pwd
        self.winkas = winkas
        self.ticket = ticket
        self.timeout = 3

        self.event_id = None

        self.connect_db()
        reactor.runReturn()

    def stop(self):
        reactor.stop()
        reactor.crash()

    def connect_db(self):
        self.winkas_db = adbapi.ConnectionPool('MySQLdb', host=self.host, user=self.user, passwd=self.pwd, db=self.winkas, connect_timeout=self.timeout)
        self.ticket_db = adbapi.ConnectionPool('MySQLdb', host=self.host, user=self.user, passwd=self.pwd, db=self.ticket, connect_timeout=self.timeout)

    def get_members(self, callback, error_handler):
        query = "SELECT Felt20 as cardno, Felt11 AS studyno, CONCAT(Felt01, ' ', Felt08) AS name, 0, 0 FROM medlemp WHERE Felt12 = 'Y' ORDER BY name"
        q = self.winkas_db.runQuery(query, ())
        q.addCallbacks(callback, error_handler)

    def get_events(self, callback, error_handler):
        query = "SELECT `Kode`, `Bontekst` FROM `tbcvarer` ORDER BY `Bontekst` ASC"
        q = self.winkas_db.runQuery(query, ())
        q.addCallbacks(callback, error_handler)

    def set_event(self, event):
        self.event_id = event

    def get_event_info(self, callback, error_handler):
        if not self.event_id:
            return None

        event = self.event_id
        query = "SELECT Antal AS tickets, SFAK AS sold FROM lagbehv, tbcvarer " \
                + "WHERE lagbehv.FUnique = tbcvarer.VareUnique " \
                + "AND tbcvarer.Kode = '{0}' ".format(event) \
                + "LIMIT 1"
        q = self.winkas_db.runQuery(query, ())
        q.addCallbacks(callback, error_handler)

    def get_event_used(self, callback, error_handler):
        if not self.event_id:
            return None

        event = self.event_id
        query = "SELECT COUNT(*) FROM used WHERE eventno = '{0}'".format(event)
        q = self.ticket_db.runQuery(query, ())
        q.addCallbacks(callback, error_handler)

    def get_member_used(self, callback, error_handler, cardno=None, studyno=None):
        if not self.event_id:
            return None

        cardno = adbapi.safe(str(cardno))
        event = adbapi.safe(str(self.event_id))

        if cardno:
            column = 'cardno'
            value = cardno
        elif studyno:
            column = 'studyno'
            value = studyno
        else:
            return

        query = "SELECT 1 FROM used WHERE `{0}` = '{1}' AND `eventno` = '{2}'".format(column, value, event)
        q = self.ticket_db.runQuery(query, ())
        q.addCallbacks(callback, error_handler)

    def get_member_tickets(self, callback, error_handler, cardno=None, studyno=None):
        if not self.event_id:
            return None

        cardno = adbapi.safe(str(cardno))
        event = adbapi.safe(str(self.event_id))

        if cardno:
            column = 'Felt20'
            value = cardno
        elif studyno:
            column = 'Felt11'
            value = studyno
        else:
            return

        query = "SELECT " \
                + "sfl.FUnique AS ticket_id, " \
                + "sfl.VareNr AS eventno, " \
                + "medlemp.felt20 AS cardno " \
                + "FROM sfl, sfh, medlemp " \
                + "WHERE sfh.Debitor = medlemp.felt00 " \
                + "AND sfl.SFHUnique = sfh.FUnique " \
                + "AND medlemp.{0} = '{1}' ".format(column, value) \
                + "AND sfl.VareNr = '{0}' ".format(event)
        q = self.winkas_db.runQuery(query, ())
        q.addCallbacks(callback, error_handler)

    def get_time(self, callback, error_handler):
        q = self.ticket_db.runQuery("SELECT NOW()")
        q.addCallback(callback, error_handler)
