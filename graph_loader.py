from neo4j import GraphDatabase
import json
import os
from dotenv import load_dotenv
# -----------------------------
# CONFIG (Update credentials)
# -----------------------------
load_dotenv()
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")   # ⚠️ change this

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
# -----------------------------
# CREATE CONSTRAINT (Avoid duplicates)
# -----------------------------
def create_constraints():
    with driver.session() as session:
        session.run("""
        CREATE CONSTRAINT skill_name_unique IF NOT EXISTS
        FOR (s:Skill)
        REQUIRE s.name IS UNIQUE
        """)
    print("✅ Constraint ensured (no duplicate skills)")


# -----------------------------
# CREATE SKILL NODE
# -----------------------------
def create_skill(tx, name):
    tx.run("""
    MERGE (s:Skill {name: $name})
    """, name=name)


# -----------------------------
# CREATE RELATIONSHIP
# -----------------------------
def create_relationship(tx, source, target):
    tx.run("""
    MATCH (a:Skill {name: $source})
    MATCH (b:Skill {name: $target})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """, source=source, target=target)


# -----------------------------
# LOAD GRAPH FROM JSON
# -----------------------------
def load_graph(json_file="skills.json"):

    with open(json_file, "r") as file:
        data = json.load(file)

    with driver.session() as session:

        # Step 1: Create all nodes
        for skill in data.get("skills", []):
            session.execute_write(create_skill, skill["name"])

        print("✅ Skills (nodes) loaded")

        # Step 2: Create relationships
        for rel in data.get("relationships", []):
            session.execute_write(
                create_relationship,
                rel["from"],
                rel["to"]
            )

        print("✅ Relationships created")

    print("🚀 Graph successfully loaded!")


# -----------------------------
# OPTIONAL: CLEAR DATABASE
# -----------------------------
def clear_graph():
    confirm = input("⚠️ This will delete ALL data. Type 'YES' to continue: ")
    if confirm == "YES":
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("🧹 Graph cleared")
    else:
        print("❌ Cancelled")


# -----------------------------
# RUN SCRIPT
# -----------------------------
if __name__ == "__main__":

    print("🔧 Setting up graph...")
    create_constraints()

    load_graph("skills.json")

    print("🎉 Done! Open Neo4j Browser to visualize your graph.")