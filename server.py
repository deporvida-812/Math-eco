import os,base64
from flask import Flask,request,jsonify
from flask_cors import CORS
from openai import OpenAI

app=Flask(__name__)
CORS(app)
client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])

METHODS="""
Приоритет: примеры пользователя, затем его лекции и практики.
EX-01 кредит: дано → формула → подстановка → расчёт → ответ.
EX-02 спрос/выручка: спрос → выручка → производная → подстановка.
EX-03 потребитель: бюджет → предельные полезности → условие оптимума → система.
EX-04 транспортная: таблица → начальный план → базис → цикл → проверка оптимальности.
EX-05 ЛП: целевая функция → ограничения → прямые → допустимая область → вершины → значение цели.
EX-06 планирование/диета: таблица → ограничения → модель → расчёт → проверка.
Если подходящего шаблона нет, прямо сказать об этом и не выдумывать методику преподавателя.
"""

@app.get("/")
def home(): return "Math-Eco AI backend is running."

@app.post("/api/solve")
def solve():
    if "image" not in request.files:
        return jsonify(error="Фото не получено"),400
    f=request.files["image"]
    raw=f.read()
    mime=f.mimetype or "image/jpeg"
    image="data:"+mime+";base64,"+base64.b64encode(raw).decode()
    prompt=f"""Ты решаешь учебные задачи по предмету «Математические методы в экономике».
{METHODS}
Проанализируй фотографию. Сначала перепиши условие и числа, не додумывая нечитабельные данные.
Определи тип задачи и подходящий шаблон. Решай именно по его последовательности.
Формат:
1. Условие
2. Дано
3. Модель
4. Расчёты по шагам
5. Ответ
6. Проверка
Если фото нечитабельно, перечисли, какие данные нужно переснять."""
    response=client.responses.create(
        model=os.getenv("OPENAI_MODEL","gpt-5.6-luna"),
        input=[{"role":"user","content":[
            {"type":"input_text","text":prompt},
            {"type":"input_image","image_url":image}
        ]}]
    )
    return jsonify(solution=response.output_text)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","8000")))
