# Hyena Hierarchy — Small-Scale Reproduction
**Môn:** CS2308 – Chuyên đề Nghiên cứu và Ứng dụng về Xử lý Ngôn ngữ Tự nhiên  
**Bài báo:** *Hyena Hierarchy: Towards Larger Convolutional Language Models* (Poli et al., ICML 2023)

---

## 📋 Tổng Quan

Repo này tái hiện kiến trúc **Hyena Hierarchy** ở quy mô nhỏ, so sánh với Transformer baseline trên dataset WikiText-2.

**Mục tiêu:** Kiểm chứng xu hướng:
- Perplexity tương đương giữa Transformer và Hyena ở scale nhỏ
- Hyena có lợi thế về tốc độ và bộ nhớ khi sequence length tăng

---

## 🗂️ Cấu Trúc Thư Mục

```
hyena-reproduction/
├── README.md
├── requirements.txt
├── data/
│   ├── preprocess.py          # Load WikiText-2, tokenize, tạo dataloader
│   └── synthetic_task.py      # (Bonus) Synthetic recall task generator
├── models/
│   ├── __init__.py
│   ├── transformer.py         # GPT-like Transformer-small
│   └── hyena.py               # Hyena-small (FFT-based, pure PyTorch)
├── train.py                   # Training loop chính
├── evaluate.py                # Evaluation: val loss + perplexity + time
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Khám phá dataset
│   ├── 02_model_training.ipynb      # Training walkthrough (Colab-ready)
│   └── 03_results_analysis.ipynb   # Phân tích kết quả + plots
├── results/
│   ├── E1_baseline.csv              # PPL Transformer vs Hyena, L=256
│   ├── E2_transformer_scale.csv    # Time/Mem Transformer vs L
│   ├── E3_hyena_scale.csv          # Time/Mem Hyena vs L
│   └── plots/
│       ├── loss_curves.png
│       ├── scaling_time.png
│       └── scaling_memory.png
├── docs/
│   ├── paper_summary.md            # Tóm tắt bài báo Hyena (TV1 điền)
│   ├── theory_attention.md         # Lý thuyết Transformer + Attention (TV1 điền)
│   ├── comparison_table.md         # Bảng so sánh Transformer vs Hyena (TV1 điền)
│   └── related_work_notes.md       # SSM, H3, Mamba (TV1 điền)
├── report/
│   └── report.pdf                  # Báo cáo PDF cuối cùng
└── slides/
    └── presentation.pdf            # Slide thuyết trình
```

---

## ⚡ Cài Đặt Nhanh

### 1. Clone repo và cài dependencies

```bash
git clone <your-repo-url>
cd hyena-reproduction
pip install -r requirements.txt
```

### 2. Chạy trên Google Colab

Mở file `notebooks/02_model_training.ipynb` — notebook đã được thiết kế để chạy end-to-end trên Colab T4.

### 3. Chạy từng bước thủ công

```bash
# Bước 1: Khám phá dataset
python data/preprocess.py --seq_len 256 --split train

# Bước 2: Train Transformer-small
python train.py --model transformer --seq_len 256 --epochs 20 --batch_size 16

# Bước 3: Train Hyena-small
python train.py --model hyena --seq_len 256 --epochs 20 --batch_size 16

# Bước 4: Evaluate cả hai
python evaluate.py --model transformer --checkpoint results/checkpoints/transformer_best.pt
python evaluate.py --model hyena --checkpoint results/checkpoints/hyena_best.pt
```

---

## 🔧 Cấu Hình Mô Hình

| Tham số | Transformer-small | Hyena-small |
|---|---|---|
| Layers | 4 | 4 |
| d_model | 256 | 256 |
| d_ff | 1024 | 1024 |
| Heads / Order | 4 heads | N=2 (Hyena²) |
| Vocab size | 50257 (GPT-2) | 50257 (GPT-2) |
| Max seq len | 1024 | 1024 |
| Parameters | ~10M | ~10M |

---

## 📊 Dataset

- **WikiText-2** (chính): `datasets.load_dataset("wikitext", "wikitext-2-raw-v1")`
  - Train: ~2M tokens, Val: ~220K tokens, Test: ~245K tokens
- **Synthetic recall task** (bonus): Tự tạo bằng `data/synthetic_task.py`

---

## 📈 Thực Nghiệm

| ID | Mô tả | Dataset | Seq Length | Status |
|---|---|---|---|---|
| E1 | Baseline: Transformer vs Hyena PPL | WikiText-2 | 256 | `[ ] TODO` |
| E2 | Scale seq length (Transformer) | WikiText-2 | 256→512→1024 | `[ ] TODO` |
| E3 | Scale seq length (Hyena) | WikiText-2 | 256→512→1024→2048 | `[ ] TODO` |
| E4 | GPU memory comparison | WikiText-2 | 256, 512, 1024 | `[ ] Bonus` |
| E5 | Synthetic recall accuracy | Synthetic | 128, 256, 512 | `[ ] Bonus` |

---

## 📚 Tài Liệu Tham Khảo Chính

1. Poli et al. (2023). *Hyena Hierarchy: Towards Larger Convolutional Language Models*. ICML 2023.
2. Vaswani et al. (2017). *Attention Is All You Need*. NeurIPS 2017.
3. Gu et al. (2021). *Efficiently Modeling Long Sequences with Structured State Spaces*. ICLR 2022.
4. Dao et al. (2022). *Hungry Hungry Hippos: Towards Language Modeling with State Space Models*. ICLR 2023.
5. Merity et al. (2016). *Pointer Sentinel Mixture Models*. (WikiText dataset)

---

## 👥 Nhóm

| Thành viên | Vai trò | Phụ trách |
|---|---|---|
| TV1 | Lý thuyết & Paper Survey | `docs/`, Sections 1-3 báo cáo |
| TV2 | Dataset & Pipeline | `data/`, `README.md`, notebooks |
| TV3 | Model & Training | `models/`, `train.py`, `evaluate.py`, `results/` |
