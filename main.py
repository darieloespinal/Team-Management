from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import mysql.connector

app = FastAPI()

# To be modified
db_config = {
    "host": "database_host",
    "user": "database_user",
    "password": "database_password",
    "database": "database_name",
}

# To be modified
def get_team_from_db(team_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM teams WHERE team_id = '{team_id}'"
    cursor.execute(query)
    team_info = cursor.fetchone()
    cursor.close()
    connection.close()
    return team_info

def add_team_to_db(team_data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    # To be modified
    query = f"INSERT INTO teams (Name, Birthdate, StartDate, Email) VALUES ('{team_data['Name']}', '{team_data['Birthdate']}', '{team_data['StartDate']}', '{team_data['Email']}')"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Team added successfully"}

def modify_team_in_db(team_id, team_data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    # To be modified
    query = f"UPDATE teams SET Name = '{team_data['Name']}', Birthdate = '{team_data['Birthdate']}', StartDate = '{team_data['StartDate']}', Email = '{team_data['Email']}' WHERE team_id = '{team_id}'"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Team modified successfully"}

def delete_team_from_db(team_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = f"DELETE FROM teams WHERE team_id = '{team_id}'"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Team deleted successfully"}

"""
GET operation to retrieve team information by ID
"""
@app.get("/teams/{team_id}")
async def get_team(team_id: str):
    try:
        team_info = get_team_from_db(team_id)
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
@app.put("/teams/{team_id}")
async def modify_team(team_id: str, team_data: dict):
    try:
        result = modify_team_in_db(team_id, team_data)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

"""
DELETE operation to delete a team by ID
"""
@app.delete("/teams/{team_id}")
async def delete_team(team_id: str):
    try:
        result = delete_team_from_db(team_id)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)


