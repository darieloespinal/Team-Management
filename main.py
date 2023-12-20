from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import mysql.connector

app = FastAPI()

# Updated database and table names
db_config = {
#    "host": "team-mgmt-402907:us-east1:sql-team-mgmt",
    "host": "34.23.76.102",
    "database": "Managers",
    "user": "doe2102",
    "password": "sql_for_mgmt",
}


def get_team_from_db(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    id = 1
    query = f"SELECT * FROM Head_Coaches WHERE id = '{id}'"
    cursor.execute(query)
    team_info = cursor.fetchone()
    cursor.close()
    connection.close()
    return team_info

def add_team_to_db(team_data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = f"INSERT INTO Head_Coaches (name, team, birthdate, startdate, enddate, email, wins, losses) " \
            f"VALUES ('{team_data['name']}', '{team_data['team']}', '{team_data['birthdate']}', " \
            f"'{team_data['startdate']}', '{team_data['enddate']}', '{team_data['email']}', " \
            f"{team_data['wins']}, {team_data['losses']})"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Team added successfully"}

def modify_team_in_db(id, team_data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = f"UPDATE Head_Coaches SET name = '{team_data['name']}', team = '{team_data['team']}', " \
            f"birthdate = '{team_data['birthdate']}', startdate = '{team_data['startdate']}', " \
            f"enddate = '{team_data['enddate']}', email = '{team_data['email']}', " \
            f"wins = {team_data['wins']}, losses = {team_data['losses']}' WHERE id = '{id}'"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Team modified successfully"}

def delete_team_from_db(id):
    id = 8
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = f"DELETE FROM Head_Coaches WHERE id = '{id}'"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Team deleted successfully"}

"""
GET operation to retrieve team information by ID
"""
@app.get("/teams/{id}")
async def get_team(id: str):
   try:
       team_info = get_team_from_db(id)
       if team_info:
           return team_info
       else:
           raise HTTPException(status_code=404, detail="Team not found")


   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


"""
POST operation to add a new team
"""
@app.post("/teams")
async def add_team(team_data: dict):
   try:
       result = add_team_to_db(team_data)
       return result


   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


"""
PUT operation to modify team information by ID
"""
@app.put("/teams/{id}")
async def modify_team(id: str, team_data: dict):
   try:
       result = modify_team_in_db(id, team_data)
       return result


   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


"""
DELETE operation to delete a team by ID
"""
@app.delete("/teams/{id}")
async def delete_team(id: str):
   try:
       result = delete_team_from_db(id)
       return result


   except Exception as e:
       raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
   #uvicorn.run(app, host="35.185.107.184", port=8000)

   try:
    connection = mysql.connector.connect(**db_config)
    print("Connected to MySQL")
   except Exception as e:
    print(f"Error: {str(e)}")

   
   connection = mysql.connector.connect(**db_config)
   cursor = connection.cursor()
   id = 1
   query = f"UPDATE Head_Coaches SET name = 'Bobby' WHERE id = '{id}'"
   cursor.execute(query)
   connection.commit()
   team_info = cursor.fetchall()
   cursor.close()
   connection.close()













   
"""
   connection = mysql.connector.connect(**db_config)
   cursor = connection.cursor()
   query = f"INSERT INTO Head_Coaches (id, name, team, birthdate, startdate, enddate, email, wins, losses) " \
        f"VALUES (8, 'wayne bennett', 'the dolphins', '1950-01-01', 1987, 'present', 'wb1987@nfl.com', 562, 323)"
   cursor.execute(query)
   connection.commit()

   id = 8
   query = f"SELECT * FROM Head_Coaches WHERE id = '{id}'"
   cursor.execute(query)
   team_info = cursor.fetchall()
   
   print(team_info)

   cursor.close()
   connection.close()
   
 """  

   
   

"""
id = 8
cursor = connection.cursor()
query = f"DELETE FROM Head_Coaches WHERE id = '{id}'"
cursor.execute(query)
query = f"SELECT COUNT(id) FROM Head_Coaches"
cursor.execute(query)
team_info = cursor.fetchall()
print(team_info)

"""





"""
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()
id = 1
query = f"SELECT * FROM Head_Coaches WHERE id = '{id}'"
cursor.execute(query)
team_info = cursor.fetchone()
cursor.close()
connection.close()
print(team_info)
"""

uvicorn.run(app, host="0.0.0.0", port=8000)




