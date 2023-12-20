# Import libraries here
from fastapi import FastAPI, HTTPException, Response, Query, Request
from fastapi.responses import HTMLResponse
import uvicorn
import mysql.connector
from coaches import CoachModel, CoachResource  # Importing CoachModel and CoachResource from coaches.py

app = FastAPI()
coach_resource = CoachResource()

# Updated database and table names
db_config = {
    "host": "34.23.76.102",
    "database": "Managers",
    "user": "doe2102",
    "password": "sql_for_mgmt",
}

"""
GET operations here
"""

@app.get("/")
async def root():
    return {"message": "Dariel, microservice - Coach searching, work in progress"}

"""
Show the coach information based on the coach_id as an HTML table webpage
"""
@app.get("/v1/coaches/{coach_id}/info", response_class=HTMLResponse)
async def coach_info_by_id(coach_id: int):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = f"SELECT * FROM coach_info WHERE coach_id = {coach_id}"

        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        if len(rows) == 0:
            message = f"Sorry, no data found for coach ID: {coach_id}, please check the input."
            return Response(content=message, media_type="text/plain", status_code=200)
        else:
            message = "<html><body>"
            message += "Here is the coach information you requested:"
            message += "<table border='1'>"
            message += "<tr>"
            for column_name in cursor.column_names:
                message += f"<th>{column_name}</th>"
            message += "</tr>"
            for row in rows:
                message += "<tr>"
                for value in row:
                    message += f"<td>{value}</td>"
                message += "</tr>"
            message += "</table></body></html>"

        return HTMLResponse(content=message, status_code=200)

    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

"""
POST operation to add a new coach
"""
@app.post("/coaches")
async def add_coach(coach_data: CoachModel):
    try:
        result = coach_resource.add_coach(coach_data)
        coach_id = coach_data.coach_id
        coach_name = coach_data.name
        
        message_content = f'New Coach {coach_name} Added to the database!'
        subject="Coach Added"
        
        GET_response = await player_by_id(player_id)
           
        return GET_response

    except Exception as e:
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

"""
PUT operation to modify coach information by ID
"""
@app.put("/coaches/{coach_id}")
async def modify_coach(coach_id: int, coach_data: CoachModel):
    try:
        coach_resource.modify_coach(coach_id, coach_data)
        
        GET_response = await player_by_id(player_id)
        return GET_response


    except Exception as e:
        #raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

"""
DELETE operation to delete a coach by ID
"""
@app.delete("/coaches/{coach_id}")
async def delete_coach(coach_id: int):
    try:
        coach_resource.delete_coach(coach_id)

        message = "Complete."
        return Response(content=message, media_type="text/plain", status_code=200)


    except Exception as e:
        #raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        return Response(content=f"Error: {str(e)}", media_type="text/plain", status_code=500)

if __name__ == "__main__":
    try:
        connection = mysql.connector.connect(**db_config)
        print("Connected to MySQL")
    except Exception as e:
        print(f"Error: {str(e)}")

    #uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)





