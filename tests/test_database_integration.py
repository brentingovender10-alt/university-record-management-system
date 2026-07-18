"""Integration checks for the Streamlit/database schema adapter."""

from __future__ import annotations

import ast
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from urms import database, queries  # noqa: E402


class BackendCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = database.build_backend_schema_connection()

    def tearDown(self) -> None:
        self.conn.close()

    def test_frontend_relations_are_available_on_backend_schema(self):
        relations = [
            "STUDENT",
            "LECTURER",
            "COURSE",
            "DEPARTMENT",
            "PROGRAM",
            "RESEARCH_PROJECT",
            "NON_ACADEMIC_STAFF_UI",
            "LECTURER_EXPERTISE_UI",
            "PROJECT_FUNDING_UI",
        ]

        for relation in relations:
            with self.subTest(relation=relation):
                self.conn.execute(f"SELECT COUNT(*) FROM {relation}").fetchone()

    def test_backend_dummy_data_is_visible_through_frontend_views(self):
        expected_counts = {
            "STUDENT": 7,
            "LECTURER": 5,
            "COURSE": 7,
            "DEPARTMENT": 3,
        }

        for relation, minimum_count in expected_counts.items():
            with self.subTest(relation=relation):
                count = self.conn.execute(f"SELECT COUNT(*) FROM {relation}").fetchone()[0]
                self.assertGreaterEqual(count, minimum_count)

    def test_backend_views_install_on_read_only_database_file(self):
        with tempfile.TemporaryDirectory() as folder:
            db_path = Path(folder) / "university.db"
            writer = sqlite3.connect(db_path)
            try:
                writer.executescript(database._BACKEND_SCHEMA_PATH.read_text(encoding="utf-8"))
                writer.commit()
            finally:
                writer.close()

            reader = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            try:
                database.install_backend_compatibility_views(reader)
                reader.execute("SELECT COUNT(*) FROM STUDENT").fetchone()
                reader.execute("SELECT COUNT(*) FROM NON_ACADEMIC_STAFF_UI").fetchone()
            finally:
                reader.close()

    def test_query_builder_specs_execute_on_backend_schema(self):
        for spec in queries.QUERIES:
            with self.subTest(query=spec["name"]):
                for param in spec.get("params", []):
                    if "options_sql" in param:
                        self.conn.execute(param["options_sql"]).fetchall()

                values = {}
                for param in spec.get("params", []):
                    if param.get("optional"):
                        values[param["key"]] = None
                    elif param["kind"] == "number":
                        values[param["key"]] = param.get("default", 0)
                    elif param["kind"] == "date":
                        values[param["key"]] = param.get("default", "2000-01-01")
                    elif "options" in param:
                        values[param["key"]] = param.get("default", param["options"][0])
                    else:
                        values[param["key"]] = ""

                self.conn.execute(spec["sql"], spec["bind"](values)).fetchall()

    def test_page_queries_execute_on_backend_schema(self):
        executed = 0
        for path in [PROJECT_ROOT / "src" / "Dashboard.py", *sorted((PROJECT_ROOT / "src" / "pages").glob("*.py"))]:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not node.args:
                    continue
                if not self._is_database_query_call(node):
                    continue

                sql = self._literal_string(node.args[0])
                if sql is None:
                    continue

                params = tuple(None for _ in range(sql.count("?")))
                with self.subTest(path=path.name, line=node.lineno):
                    self.conn.execute(sql, params).fetchall()
                executed += 1

        self.assertGreaterEqual(executed, 30)

    def test_frontend_sql_relations_exist_on_backend_schema(self):
        relations = set()
        for sql in self._frontend_sql_strings():
            relations.update(re.findall(r"\b(?:FROM|JOIN)\s+([A-Z][A-Z0-9_]*)\b", sql))

        self.assertGreaterEqual(len(relations), 20)
        for relation in sorted(relations):
            with self.subTest(relation=relation):
                exists = self.conn.execute(
                    """
                    SELECT 1
                    FROM sqlite_master
                    WHERE name = ? AND type IN ('table', 'view')
                    UNION ALL
                    SELECT 1
                    FROM sqlite_temp_master
                    WHERE name = ? AND type IN ('table', 'view')
                    LIMIT 1
                    """,
                    (relation, relation),
                ).fetchone()
                self.assertIsNotNone(exists)

    @staticmethod
    def _is_database_query_call(node: ast.Call) -> bool:
        return isinstance(node.func, ast.Attribute) and node.func.attr in {"run_query", "scalar"}

    @classmethod
    def _frontend_sql_strings(cls) -> list[str]:
        sql_strings = [spec["sql"] for spec in queries.QUERIES]
        for spec in queries.QUERIES:
            sql_strings.extend(
                param["options_sql"] for param in spec.get("params", []) if "options_sql" in param
            )

        for path in [PROJECT_ROOT / "src" / "Dashboard.py", *sorted((PROJECT_ROOT / "src" / "pages").glob("*.py"))]:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not node.args:
                    continue
                if not cls._is_database_query_call(node):
                    continue
                sql = cls._literal_string(node.args[0])
                if sql is not None:
                    sql_strings.append(sql)
        return sql_strings

    @classmethod
    def _literal_string(cls, node: ast.AST) -> str | None:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left = cls._literal_string(node.left)
            right = cls._literal_string(node.right)
            if left is not None and right is not None:
                return left + right
        return None


if __name__ == "__main__":
    unittest.main()
