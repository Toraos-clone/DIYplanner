import sqlite3

DB_NAME = "projects.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    # creates the project table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL UNIQUE
                   )
                   """)
    
    # creates the tools table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tools (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   project_id INTEGER,
                   name TEXT NOT NULL,
                   FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
                   )
                """)
    
    # supplies table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS supplies(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   project_id INTEGER,
                   name TEXT NOT NULL,
                   quantity TEXT,
                   FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
                   )
                   """)
    
    conn.commit()
    conn.close()
    
    
def add_project(name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (name) VALUES (?)", (name,))
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return project_id
    
    
def add_tool(project_id, tool_name):
     conn = sqlite3.connect("projects.db")
     cursor = conn.cursor()
     cursor.execute("INSERT INTO tools (project_id, name) VALUES (?, ?)", (project_id, tool_name))
     tool_id = cursor.lastrowid
     conn.commit()
     conn.close()
     return tool_id

def add_supply(project_id, name, quantity):
     conn = sqlite3.connect("projects.db")
     cursor = conn.cursor()
     cursor.execute("INSERT INTO supplies (project_id, name, quantity) VALUES (?, ?, ?)", 
                   (project_id, name, quantity))
     supply_id = cursor.lastrowid
     conn.commit()
     conn.close()

def get_all_projects():
     conn = sqlite3.connect("projects.db")
     cursor = conn.cursor()
     cursor.execute("SELECT id, name FROM projects")
     projects = cursor.fetchall()
     conn.close()
     return projects

def get_tools_for_project(project_id):
    conn = sqlite3.connect("projects.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM tools WHERE project_id = ?", (project_id,))
    tools = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    conn.close()
    return tools


def get_supplies_for_project(project_id):
    conn = sqlite3.connect("projects.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity FROM supplies WHERE project_id = ?", (project_id,))
    supplies = [{"id": row[0], "name": row[1], "quantity": row[2]} for row in cursor.fetchall()]
    conn.close()
    return supplies



def update_tool(tool_id, new_name):
    conn = sqlite3.connect("projects.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tools SET name = ? WHERE id = ?", (new_name, tool_id))
    conn.commit()
    conn.close()

def delete_tool_by_id(tool_id):
    conn = sqlite3.connect("projects.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tools WHERE id = ?", (tool_id,))
    conn.commit()
    conn.close()

def update_supply(supply_id, name, quantity):
    conn = sqlite3.connect("projects.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE supplies SET name = ?, quantity = ? WHERE id = ?", (name, quantity, supply_id))
    conn.commit()
    conn.close()

def delete_supply_by_id(supply_id):
    conn = sqlite3.connect("projects.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM supplies WHERE id = ?", (supply_id,))
    conn.commit()
    conn.close()





