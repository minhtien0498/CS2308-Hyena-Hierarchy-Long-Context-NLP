# Hyena Hierarchy — Paper Presentation & Small-Scale Reproduction
**Môn:** CS2308 – Chuyên đề Nghiên cứu và Ứng dụng về Xử lý Ngôn ngữ Tự nhiên  
**Bài báo:** *Hyena Hierarchy: Towards Larger Convolutional Language Models* (Poli et al., ICML 2023)

---

## 📋 Tổng Quan

Repo này phục vụ hai mục tiêu chính:

1. **Trình bày lại bài báo Hyena Hierarchy** trong buổi seminar 30 phút và chuẩn bị 15 phút hỏi đáp.
2. **Tái hiện ở quy mô nhỏ** kiến trúc Hyena Hierarchy, so sánh với Transformer baseline trên dataset WikiText-2.

**Mục tiêu:** Kiểm chứng xu hướng:
- Perplexity tương đương giữa Transformer và Hyena ở scale nhỏ
- Hyena có lợi thế về tốc độ và bộ nhớ khi sequence length tăng

---

## 🗂️ Cấu Trúc Thư Mục

```
.
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
│   ├── 02_model_training.ipynb      # Training walkthrough (Colab-ready)
│   └── reproduce.ipynb              # Notebook tái hiện nhanh
├── results/
│   └── plots/
│       └── reproduce_runtime.png    # Biểu đồ runtime reproduction
├── docs/
│   ├── paper_summary.md            # Tóm tắt bài báo Hyena
│   ├── theory_attention.md         # Lý thuyết Transformer + Attention
│   ├── comparison_table.md         # Bảng so sánh Transformer vs Hyena
│   ├── related_work_notes.md       # SSM, H3, GSS, Mamba
│   ├── ke_hoach_trien_khai_hyena.md
│   ├── huong_dan_de_tai_hyena.md
│   ├── phan_cong_present_hyena_3_tuan.md
│   └── poli23a.pdf                 # Paper gốc
└── slides/
    ├── slide_outline.md            # Outline slide
    └── slides.md                   # Slide Marp
```

---

## ⚡ Cài Đặt Nhanh

### 1. Clone repo và cài dependencies

```bash
git clone <your-repo-url>
cd CS2308-Hyena-Hierarchy-Long-Context-NLP
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

## 🎤 Chuẩn Bị Thuyết Trình

Buổi seminar dự kiến gồm **30 phút trình bày** và **15 phút hỏi đáp**. Nhóm chia nội dung thành khoảng **24 slide**, mỗi thành viên phụ trách khoảng **8 slide**.

| Thành viên | Slide | Nội dung chính |
|---|---:|---|
| TV1 | 1–8 | Nền tảng, motivation, Self-Attention, `O(L²)`, related work |
| TV2 | 9–16 | Hyena operator, long convolution, gating, FFTConv, kết quả paper gốc |
| TV3 | 17–24 | Small-scale reproduction, dataset, setup, kết quả nhóm, thảo luận |

Tài liệu phân công chi tiết:

- [`docs/phan_cong_present_hyena_3_tuan.md`](docs/phan_cong_present_hyena_3_tuan.md): phân công slide, output cần chuẩn bị, liên kết giữa các thành viên và Q&A.
- [`slides/slide_outline.md`](slides/slide_outline.md): outline slide đề xuất.
- [`slides/slides.md`](slides/slides.md): bản slide Marp hiện có.

Phần hỏi đáp được chia theo phần trình bày:

| Nhóm câu hỏi | Người trả lời chính |
|---|---|
| Transformer, Self-Attention, complexity, related work | TV1 |
| Hyena operator, FFTConv, gating, kết quả paper gốc | TV2 |
| Dataset, code, reproduction, kết quả nhóm, giới hạn | TV3 |

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
| TV1 | Nền tảng & Paper Survey | Motivation, Self-Attention, related work, slide 1–8 |
| TV2 | Hyena Method & Paper Results | Hyena operator, FFTConv, kết quả paper gốc, slide 9–16 |
| TV3 | Reproduction & Evaluation | Dataset, model setup, kết quả nhóm, slide 17–24 |
