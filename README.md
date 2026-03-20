# Blood Smear Image Categorization

## Objective
Develop a machine learning model to categorize 8 different types of blood smears from image data.

1. Data Collection & Preparation
   - Source: high-res images from medical databases or labs.
   - Annotation: images annotated by medical professionals for accuracy.
   - Augmentation: rotation, scaling, and cropping to enhance dataset size and robustness.
   - Data split: 60% training, 15% validation, 25% test.
2. Model Development & Architecture
   - Pre-processing: resize, normalize, and enhance images.
   - Architecture: CNNs implemented with PyTorch.
   - Training: regularization techniques such as dropout and batch normalization.
3. Model Evaluation
   - Validation: monitor training quality on a validation split.
   - Metrics: accuracy, F1 score, precision, recall, and confusion matrix.
   - Testing: final performance assessment on unseen data.
4. Deployment
   - Integration: web/mobile upload workflow for predictions.
   - Feedback loop: user feedback used for model improvement.
5. Limitations & Future Work
   - Variability: performance can vary based on image quality and collection conditions.
   - Expansion: potential to include more smear types and cell anomalies.

---

## Backend API (FastAPI)

A self-contained backend is available under `backend/` with:

- `GET /health`
- `GET /properties`
- `GET /properties/{id}`
- `POST /search`
- `POST /ai/chat`

### Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Environment configuration template is available in `backend/.env.example`.

### Create a brand-new repo with all current code

If you want everything bundled into a fresh git repository, run:

```bash
./scripts/create_new_repo_bundle.sh /path/to/new-repo
```

This script copies the project files, initializes a new git repo, and creates an initial commit.
