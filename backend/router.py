from language_detector import lang_detected

def router(text):

	language = lang_detected(text)
	is_mixed = True if language[0] == 'Mixed' else False
	classfier = language[1]

	return {"is_mixed": is_mixed, "classfier": classfier}