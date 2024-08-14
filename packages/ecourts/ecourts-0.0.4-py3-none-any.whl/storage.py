from entities import CaseType, Court, Case,ActType, CaseType
import sqlite3
import json
from collections.abc import Iterator


class Storage:
    """
    A class that implements storage for various dataclasses
    in a local sqlite database. The database is called
    ecourts.db in the PWD unless one is specified.

    Every dataclass is converted to a JSON object stored using the
    sqlite json extension.
    """

    def __init__(self, filename="ecourts.db"):
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS case_types (value JSON)")
        self.cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_case_types ON case_types(json_extract(value, '$.code'), json_extract(value, '$.court_state_code'), json_extract(value, '$.court_court_code'))"
        )

        self.cursor.execute("CREATE TABLE IF NOT EXISTS act_types (value JSON)")
        self.cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_act_types ON act_types(json_extract(value, '$.code'), json_extract(value, '$.court_state_code'), json_extract(value, '$.court_court_code'))"
        )
        self.cursor.execute("CREATE TABLE IF NOT EXISTS courts (value JSON)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS cases (state_code, court_code, value JSON)")
        self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_cases_cnr ON cases(json_extract(value, '$.cnr_number'))")
        self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_cases_caseno ON cases(json_extract(value, '$.case_type'), json_extract(value, '$.registration_number'))")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_cases_category ON cases(json_extract(value, '$.category'))")
        self.conn.commit()

    def addCaseTypes(self, records: list[CaseType]):
        for record in records:
            self.cursor.execute(
                "INSERT OR IGNORE INTO case_types VALUES (?)",
                (json.dumps(dict(record)),),
            )
        self.conn.commit()

    def getCaseTypes(self):
        r = self.conn.execute("SELECT * FROM case_types")
        for record in r:
            j = json.loads(record["value"])
            court = Court(
                state_code=j["court_state_code"], court_code=j["court_court_code"]
            )
            yield CaseType(code=j["code"], description=j["description"], court=court)


    def addActTypes(self, records: list[ActType]):
        for record in records:
            self.cursor.execute(
                "INSERT OR IGNORE INTO act_types VALUES (?)",
                (json.dumps(dict(record)),),
            )
        self.conn.commit()

    def getActTypes(self) -> Iterator[ActType]:
        r = self.conn.execute("SELECT * FROM act_types")
        for record in r:
            j = json.loads(record["value"])
            court = Court(
                state_code=j["court_state_code"], court_code=j["court_court_code"]
            )
            yield ActType(code=j["code"], description=j["description"], court=court)

    def addCourts(self, records: list[Court]):
        for record in records:
            self.cursor.execute(
                "INSERT OR IGNORE INTO courts VALUES (?)", (json.dumps(dict(record)),)
            )
        self.conn.commit()

    #TODO: Move storage to under ecourts.storage so we get court information from there
    def addCases(self, court: Court, records: list[Case]):
        for record in records:
            self.cursor.execute(
                "INSERT OR IGNORE INTO cases VALUES (?, ?, ?)", (court.state_code, court.court_code or "1", json.dumps(record.json(), default=str))
            )
        self.conn.commit()
