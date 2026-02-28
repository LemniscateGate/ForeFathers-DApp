import os
import json
import glob
import requests
os.environ["OPENAI_API_KEY"] = "fake"
os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process, LLM
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.environ.get("GROQ_API_KEY"),
)

brain = ""
for fp in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "forefathers_brain", "knowledge", "brain_*.json"))):
    d = json.load(open(fp, encoding="utf-8"))
    if isinstance(d, list):
        for i in d:
            brain += i.get("content", "") if isinstance(i, dict) else str(i)
    elif isinstance(d, dict):
        brain += d.get("content", "")
brain = brain[:12000]

class Req(BaseModel):
    message: str

@app.get("/")
def home():
    return HTMLResponse(open(r"C:\Users\Gabriel\Downloads\ForeFathers-DApp\weberdy.html", encoding="utf-8").read())

@app.post("/")
async def chat(req: Req):
    try:
        a = Agent(
            role="Weberdy",
            goal="Answer about ForeFathers DAO and Gabriel Ross",
            backstory="You are Weberdy, sovereign AI of ForeFathers DAO.\n" + brain,
            llm=llm,
            verbose=True,
        )
        t = Task(
            description="Respond to: {message}",
            expected_output="Clear response as Weberdy",
            agent=a,
        )
        r = Crew(agents=[a], tasks=[t], process=Process.sequential, verbose=True).kickoff(inputs={"message": req.message})
        return {"reply": str(r)}
    except Exception as e:
        return {"reply": f"Weberdy error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
