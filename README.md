# Plant Doctor 🌿

Scans a plant leaf with the camera, detects the disease with a trained model, and gives farmer advice
and chat through Groq. UI: Streamlit.

## Folder structure
```
plant-doctor/
├── app.py              <- Streamlit screen (run this)
├── .env                <- your API key and settings (never share)
├── .env.example        <- empty template
├── requirements.txt
├── .streamlit/
│   └── config.toml     <- port, theme
├── models/
│   ├── plant_model.keras
│   └── class_names.json
└── src/
    ├── config.py       <- reads .env
    ├── classifier.py   <- photo -> disease
    ├── advisor.py      <- Groq advice
    └── chat.py         <- chat logic
```

## Run (Windows)
1. Put your Groq key in `.env`: `GROQ_API_KEY=gsk_...`
2. In the project folder:
```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
(If `python` is not recognised, use the full path to your python.exe instead.)
3. The browser opens at http://localhost:8501. Allow camera access when asked.

## Notes
- The camera only works on `localhost` or on an HTTPS address. Opening the app from a phone through a
  plain `http://192.168...` address will not give camera access.
- The camera widget uses the browser's default camera. On a phone, "Or upload a photo instead" opens the
  phone camera app (rear camera) via the Take Photo option.
- The model was trained on clean, single-leaf photos (PlantVillage). Photos from a real field may be
  detected less accurately.
