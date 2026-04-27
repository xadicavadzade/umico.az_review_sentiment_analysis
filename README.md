## Data Collection & Preprocessing

### Data Collection
- Reviews were collected from **umico.az** via API endpoints discovered through browser DevTools
- Each review contained customer text, score, name, and other metadata
- Only `score` and `review text` columns were kept for modeling

### Preprocessing Steps

**1. Anomaly Detection & Manual Review**
- Checked whether scores and review texts were consistent with each other using keyword-based rules
- Flagged suspicious rows (e.g. high score but negative words, low score but positive words)
- Exported flagged rows to Excel, manually corrected or deleted inconsistent entries
- Applied corrections back to the dataset using the `flag` column

**2. Binary Label Creation**
- Original score distribution was highly imbalanced:

| Score | Count |
|-------|-------|
| 1 | 175 |
| 2 | 38 |
| 3 | 60 |
| 4 | 132 |
| 5 | 2088 |

- Due to severe imbalance across 5 classes, a **binary classification** approach was chosen
- Score 3 was removed as it represented neutral sentiment and had few samples
- Binary labels assigned: `0` (negative) for scores 1–2, `1` (positive) for scores 4–5

**3. Quality Checks**
- Checked for null values
- Detected and resolved duplicate texts with conflicting labels manually

---

## Model

Model weights are available on HuggingFace Hub:
🤗 [xadicavadzade/sentiment-azerbaijani](https://huggingface.co/xadicavadzade/sentiment-azerbaijani)

### Base Model
- **xlm-roberta-base** — multilingual transformer pre-trained on 100 languages, fine-tuned for Azerbaijani sentiment analysis

### Handling Class Imbalance
- Even after binary conversion, negative class (0) remained underrepresented
- **Class weights** were first tested using `compute_class_weight` with a custom `WeightedTrainer`, but results were poor
- Switched to **oversampling**: negative samples were duplicated to match the size of the positive class, which yielded significantly better results

### Training
- Tokenizer: `xlm-roberta-base`, max length 128
- Optimizer: AdamW, learning rate 2e-5, weight decay 0.01
- 5 epochs, best model selected based on `f1_macro`
- Early stopping with patience 2
- **Best model: Epoch 3** (F1 macro: 0.83)

### Results

| Class | Precision | Recall | F1 |
|-------|-----------|--------|----|
| Negative (0) | 0.67 | 0.71 | 0.69 |
| Positive (1) | 0.97 | 0.97 | 0.97 |
| **Macro avg** | **0.82** | **0.84** | **0.83** |
| **Accuracy** | | | **0.95** |

> **Note:** Negative class F1 is lower due to limited negative samples in the dataset (only 213 negative vs 2220 positive reviews). Collecting more negative reviews would improve this metric.

---

## TODO
- [ ] Collect more negative reviews to improve negative class performance
- [ ] Build REST API with FastAPI
- [ ] Deploy model
