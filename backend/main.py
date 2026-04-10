from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional


from router import router
from grok_client import generate_explanation
from amharic_classifier import get_amharic_classification
from english_classifier import get_english_classification


app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Request(BaseModel):
	headline: str
	article_body: str
	source_url: Optional[str] = None


class Response(BaseModel):
	category: str
	confidence: float
	explanation: str
	language_detected: str
	model_used: str
	source_url: Optional[str] = None
	mixed_warning: bool


@app.post("/classify", response_model=Response)
async def classify(request: Request):
	lang_result = router(request.article_body)

	combined_text = request.headline + " " + request.article_body

	if request.source_url:
		combined_text = combined_text + " " + request.source_url

	if lang_result["classifier"] == "Amharic":
		category, confidence = get_amharic_classification(combined_text)
		model_used = "Amharic Model"
	else:
		category, confidence = get_english_classification(combined_text)
		model_used = "English Model"

	explanation = await generate_explanation(
		request.headline,
		request.article_body,
		category,
		confidence
	)

	return Response(
			category=category,
			confidence=confidence,
			explanation=explanation,
	        language_detected=lang_result["classifier"],
	        model_used=model_used,
	        source_url=request.source_url,
	        mixed_warning=lang_result["is_mixed"]
		)

@app.get("/health")
async def health():
	return {"status": "ok"}