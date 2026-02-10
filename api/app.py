from fastapi import FastAPI, HTTPException, UploadFile, File

from api.inference_queue import JobQueue
from api.schemas import LearnRequest, LearnJobResponse, PredictRequest, JobResponse, JobResultResponse
from config import Config
from llm.service import LLMService
from ocr.service import OCRService

app = FastAPI(
    title="LLM-Extractor",
    version="1.0.0",
)

config = Config()
llm = LLMService(config)
ocr_service = OCRService()
queue = JobQueue()


@app.post("/learn", response_model=LearnJobResponse)
def learn(req: LearnRequest):
    def task():
        return llm.learn_field_location(
            document_type=req.document_type,
            field_name=req.field_name,
            examples=[ex.dict() for ex in req.examples],
            force=req.force,
        )

    job_id = queue.submit(task, job_type="learn")
    return LearnJobResponse(job_id=job_id)


@app.post("/predict", response_model=JobResponse)
def predict(req: PredictRequest):
    def task():
        return llm.extract_field(
            target_ocr_json=req.ocr_json,
            document_type=req.document_type,
            field_name=req.field_name,
        )

    job_id = queue.submit(task, job_type="predict")
    return JobResponse(job_id=job_id)


@app.get("/result/{job_id}", response_model=JobResultResponse)
def result(job_id: str):
    job = queue.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobResultResponse(
        status=job.status,
        value=job.result,
        error=job.error,
    )

@app.post("/generate-ocr", response_model=JobResponse)
def generate_ocr(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = file.file.read()

    def task():
        return ocr_service.recognize_images([image_bytes])

    job_id = queue.submit(task, job_type="ocr")
    return JobResponse(job_id=job_id)