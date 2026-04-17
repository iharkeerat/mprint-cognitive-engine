from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
# -----------------------------
# CONFIG (Update credentials)
# -----------------------------
load_dotenv()
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")  # Ensure this matches your local Neo4j password

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# -----------------------------
# GET LEARNING PATH
# -----------------------------
def get_learning_path(target_skill, depth="1..3"):
    """
    Returns all possible prerequisite paths to target skill.
    Uses PREREQUISITE_OF relationship created by graph_loader.py
    """
    query = f"""
    MATCH path = (t:Skill {{name: $target}})<-[:PREREQUISITE_OF*{depth}]-(s:Skill)
    RETURN path
    """

    with driver.session() as session:
        result = session.run(query, target=target_skill)
        paths = []
        for record in result:
            path = record["path"]
            # Extract node names and reverse to show s -> t order
            skills = [node["name"] for node in path.nodes][::-1]
            paths.append(skills)
        return paths


# -----------------------------
# GET DIRECT PREREQUISITES
# -----------------------------
def get_prerequisites(skill):
    """
    Returns immediate prerequisites of a skill
    """
    query = """
    MATCH (a:Skill)-[:PREREQUISITE_OF]->(b:Skill {name: $skill})
    RETURN a.name AS prerequisite
    """
    with driver.session() as session:
        result = session.run(query, skill=skill)
        return [record["prerequisite"] for record in result]


# -----------------------------
# GET NEXT SKILLS (Forward)
# -----------------------------
def get_next_skills(skill, depth="1..2"):
    """
    Returns what can be learned after this skill
    """
    query = f"""
    MATCH (s:Skill {{name: $target}})-[:PREREQUISITE_OF*{depth}]->(t:Skill)
    RETURN DISTINCT t.name AS next_skill
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(query, target=skill)
        return [record["next_skill"] for record in result]


# -----------------------------
# CHECK IF SKILL EXISTS
# -----------------------------
def skill_exists(skill):
    query = """
    MATCH (s:Skill {name: $skill})
    RETURN s LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query, skill=skill)
        return result.single() is not None


# -----------------------------
# SMART PATH (PERSONALIZED)
# -----------------------------
def get_personalized_path(target_skill, user_type):
    """
    Adjust depth based on cognitive style
    """
    if user_type == "Activist":
        depth = "1..2"
    elif user_type == "Theorist":
        depth = "1..5"
    elif user_type == "Reflector":
        depth = "1..3"
    else:
        depth = "1..3"

    return get_learning_path(target_skill, depth)


# -----------------------------
# ADAPTIVE PATH (ACCURACY BASED)
# -----------------------------
def get_adaptive_path(topic, confidence_score, mode):
    """
    Determines depth and path complexity based on accuracy scores.
    Uses PREREQUISITE_OF to match the loader schema.
    """
    if confidence_score < 40:
        # BRIDGE PATH: Focus on foundational nodes only (Short paths)
        query = """
        MATCH (t:Skill {name: $topic})<-[:PREREQUISITE_OF*1..2]-(p)
        RETURN DISTINCT p.name as step
        """
    elif confidence_score > 80:
        # EXPERT PATH: Skip basics, look for deeper architecture nodes
        query = """
        MATCH (t:Skill {name: $topic})<-[:PREREQUISITE_OF*3..5]-(p)
        RETURN DISTINCT p.name as step
        """
    else:
        # STANDARD PATH: Full curriculum
        query = """
        MATCH (t:Skill {name: $topic})<-[:PREREQUISITE_OF*1..3]-(p)
        RETURN DISTINCT p.name as step
        """

    with driver.session() as session:
        result = session.run(query, topic=topic)
        # Return a flat list of skill names for the frontend
        return [record["step"] for record in result]


# -----------------------------
# TEST RUN
# -----------------------------
if __name__ == "__main__":
    # Ensure "Machine Learning" exists in your skills.json and has been loaded
    target = "Machine Learning"

    print("🔍 Checking skill...")
    if not skill_exists(target):
        print(f"❌ Skill '{target}' not found in graph. Run graph_loader.py first.")
    else:
        print(f"✅ Skill '{target}' exists")

        print("\n📚 All Learning Paths:")
        paths = get_learning_path(target)
        for i, p in enumerate(paths, 1):
            print(f"{i}. {' → '.join(p)}")

        print("\n📌 Direct Prerequisites:")
        print(get_prerequisites(target))

        print("\n➡️ Next Skills from 'Python':")
        # Ensure 'Python' is a node that points to something
        print(get_next_skills("Python"))

        print("\n🧠 Personalized Path (Activist):")
        print(get_personalized_path(target, "Activist"))

        print("\n⚡ Adaptive Path (Confidence 30%):")
        print(get_adaptive_path(target, 30, "FOUNDATION_BRIDGE"))