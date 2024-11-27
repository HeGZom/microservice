import sys
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from loguru import logger
from typing import Optional

# Настройка логирования с использованием loguru для вывода в консоль
logger.add(sys.stderr, level="INFO")

app = FastAPI()

class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str

# POST /calculate/ - выполнение арифметической операции
@app.post("/calculate/")
def calculate(request: CalculationRequest):
    logger.info("Calculation request received: {}", request)

    num1 = request.num1
    num2 = request.num2
    operation = request.operation

    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="Division by zero")
        result = num1 / num2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    logger.info("Calculation result: {}", result)
    return {"result": result}

# GET /add/ - сложение двух чисел
@app.get("/add/")
def add(num1: float = Query(..., description="First number"), num2: float = Query(..., description="Second number")):
    logger.info("Addition request received: num1={}, num2={}", num1, num2)
    result = num1 + num2
    logger.info("Addition result: {}", result)
    return {"result": result}

# PUT /subtract/ - вычитание двух чисел
@app.put("/subtract/")
def subtract(num1: float = Query(..., description="First number"), num2: float = Query(..., description="Second number")):
    logger.info("Subtraction request received: num1={}, num2={}", num1, num2)
    result = num1 - num2
    logger.info("Subtraction result: {}", result)
    return {"result": result}

# DELETE /clear/ - очистка логов
@app.delete("/clear/")
def clear_logs():
    logger.info("Clearing logs")
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    return {"detail": "Logs cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
