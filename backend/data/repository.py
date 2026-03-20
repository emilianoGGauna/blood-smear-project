from __future__ import annotations

import importlib
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..schemas.property import PropertyDetail


@dataclass(slots=True)
class PropertyRecord:
    id: int
    title: str
    location: str
    price: int
    bedrooms: int
    bathrooms: int
    square_feet: int
    tags: list[str]
    description: str
    amenities: list[str]

    def to_detail(self) -> PropertyDetail:
        return PropertyDetail(
            id=self.id,
            title=self.title,
            location=self.location,
            price=self.price,
            bedrooms=self.bedrooms,
            bathrooms=self.bathrooms,
            square_feet=self.square_feet,
            tags=self.tags,
            description=self.description,
            amenities=self.amenities,
        )


class PropertyRepository(Protocol):
    def list_properties(self) -> list[PropertyDetail]:
        ...

    def get_property_by_id(self, property_id: int) -> PropertyDetail | None:
        ...


class SQLitePropertyRepository:
    def __init__(self, db_path: str = "backend/data/properties.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS properties (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    location TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    bedrooms INTEGER NOT NULL,
                    bathrooms INTEGER NOT NULL,
                    square_feet INTEGER NOT NULL,
                    tags TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amenities TEXT NOT NULL
                )
                """
            )
            existing_count = connection.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
            if existing_count == 0:
                self._seed(connection)

    def _seed(self, connection: sqlite3.Connection) -> None:
        seed_rows = [
            (1, "Modern Loft", "Austin, TX", 325000, 2, 2, 1220, "loft,city,open-floor", "Bright urban loft near downtown amenities.", "gym,parking,pet-friendly"),
            (2, "Family Home", "Denver, CO", 540000, 4, 3, 2480, "family,suburban,garage", "Spacious home with backyard and nearby schools.", "yard,garage,storage"),
            (3, "Beach Condo", "San Diego, CA", 690000, 2, 2, 1110, "beach,condo,view", "Ocean-view condo with walkable beach access.", "pool,balcony,security"),
            (4, "Starter Townhouse", "Raleigh, NC", 285000, 3, 2, 1460, "townhouse,starter,value", "Affordable townhouse in a growing neighborhood.", "playground,hoa,parking"),
        ]
        connection.executemany(
            """
            INSERT INTO properties
            (id, title, location, price, bedrooms, bathrooms, square_feet, tags, description, amenities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            seed_rows,
        )

    def list_properties(self) -> list[PropertyDetail]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, title, location, price, bedrooms, bathrooms, square_feet, tags, description, amenities
                FROM properties
                ORDER BY id
                """
            ).fetchall()
        return [self._to_detail(row) for row in rows]

    def get_property_by_id(self, property_id: int) -> PropertyDetail | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, title, location, price, bedrooms, bathrooms, square_feet, tags, description, amenities
                FROM properties
                WHERE id = ?
                """,
                (property_id,),
            ).fetchone()
        return self._to_detail(row) if row else None

    def _to_detail(self, row: tuple) -> PropertyDetail:
        record = PropertyRecord(
            id=row[0],
            title=row[1],
            location=row[2],
            price=row[3],
            bedrooms=row[4],
            bathrooms=row[5],
            square_feet=row[6],
            tags=row[7].split(",") if row[7] else [],
            description=row[8],
            amenities=row[9].split(",") if row[9] else [],
        )
        return record.to_detail()


class PostgresPropertyRepository:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        psycopg = importlib.import_module("psycopg")
        self._connect_factory = psycopg.connect

    def list_properties(self) -> list[PropertyDetail]:
        with self._connect_factory(self.dsn) as connection:
            rows = connection.execute(
                """
                SELECT id, title, location, price, bedrooms, bathrooms, square_feet, tags, description, amenities
                FROM properties
                ORDER BY id
                """
            ).fetchall()
        return [self._row_to_detail(row) for row in rows]

    def get_property_by_id(self, property_id: int) -> PropertyDetail | None:
        with self._connect_factory(self.dsn) as connection:
            row = connection.execute(
                """
                SELECT id, title, location, price, bedrooms, bathrooms, square_feet, tags, description, amenities
                FROM properties
                WHERE id = %s
                """,
                (property_id,),
            ).fetchone()
        return self._row_to_detail(row) if row else None

    def _row_to_detail(self, row: tuple) -> PropertyDetail:
        return PropertyRecord(
            id=row[0],
            title=row[1],
            location=row[2],
            price=row[3],
            bedrooms=row[4],
            bathrooms=row[5],
            square_feet=row[6],
            tags=list(row[7]) if isinstance(row[7], list) else str(row[7]).split(","),
            description=row[8],
            amenities=list(row[9]) if isinstance(row[9], list) else str(row[9]).split(","),
        ).to_detail()
