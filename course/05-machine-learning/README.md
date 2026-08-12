# Level 05 — Machine Learning

**Start here if you can write and ship real Python, and you now want to build
models rather than call them.**

Nineteen modules from what learning is, through deep learning in PyTorch, to
generative models, to pretraining a small language model of your own and fine
tuning a large one. Every architecture is built from parts before a library is
allowed to build it for you.

| | |
|---|---|
| Modules | M01 to M19, in Parts 8, 9, 10, and 11 |
| Duration | 16 weeks |
| Weekly load | 10 to 15 hours |
| Prerequisite | Level 03, in particular Module 29 for NumPy and pandas |
| Framework | PyTorch throughout, with the Hugging Face stack layered on top from Module M16 |
| Ends with | A model you pretrained, a model you fine tuned, and a service that serves it |

---

## Part 8 — Foundations of Learning

Weeks 1 to 3. What learning is, the maths you will actually use, and the
experimental discipline, while the models are still small enough to run in
seconds.

| Module | Title | Time |
|---|---|---|
| [M01](part-8-ml-foundations/m01-what-learning-is/README.md) | What Learning Is | L4 E5 |
| [M02](part-8-ml-foundations/m02-the-maths-you-will-use/README.md) | The Maths You Will Actually Use | L5 E6 |
| [M03](part-8-ml-foundations/m03-linear-models-and-gradient-descent/README.md) | Linear Models and Gradient Descent from Scratch | L4 E6 |
| [M04](part-8-ml-foundations/m04-evaluation-and-the-experimental-loop/README.md) | Evaluation, Data, and the Experimental Loop | L4 E6 |

## Part 9 — Deep Learning with PyTorch

Weeks 4 to 8. Tensors, autograd, backpropagation derived by hand, the training
diagnostics nobody writes down, then convolution, recurrence, and the
transformer built from tensors up.

| Module | Title | Time |
|---|---|---|
| [M05](part-9-deep-learning/m05-tensors-and-autograd/README.md) | Tensors and Autograd | L4 E6 |
| [M06](part-9-deep-learning/m06-neural-networks/README.md) | Neural Networks, Derived and Built | L5 E7 |
| [M07](part-9-deep-learning/m07-training-that-works/README.md) | Training That Actually Works | L5 E7 |
| [M08](part-9-deep-learning/m08-convolutional-networks-and-vision/README.md) | Convolutional Networks and Vision | L4 E7 |
| [M09](part-9-deep-learning/m09-sequences-and-attention/README.md) | Sequences, Recurrence, and the Road to Attention | L4 E6 |
| [M10](part-9-deep-learning/m10-the-transformer/README.md) | The Transformer, Built from Parts | L5 E8 |

## Part 10 — Generative Models

Weeks 9 to 11. Modelling the data rather than the label: latent spaces,
adversarial training, and denoising.

| Module | Title | Time |
|---|---|---|
| [M11](part-10-generative-models/m11-autoencoders-and-vaes/README.md) | Autoencoders and Variational Autoencoders | L4 E6 |
| [M12](part-10-generative-models/m12-gans/README.md) | Generative Adversarial Networks | L5 E7 |
| [M13](part-10-generative-models/m13-diffusion-models/README.md) | Diffusion Models | L5 E7 |

## Part 11 — Language Models and LLMs

Weeks 12 to 16. Tokenisation, a small language model you pretrain yourself, the
open ecosystem, fine tuning and alignment, serving, and the capstone.

| Module | Title | Time |
|---|---|---|
| [M14](part-11-language-models/m14-tokenisation-and-language-modelling/README.md) | Tokenisation and Language Modelling | L4 E6 |
| [M15](part-11-language-models/m15-build-a-mini-llm/README.md) | Build a Mini LLM from Scratch | P16 |
| [M16](part-11-language-models/m16-pretrained-models-and-the-ecosystem/README.md) | Pretrained Models and the Open Ecosystem | L4 E6 |
| [M17](part-11-language-models/m17-fine-tuning-and-alignment/README.md) | Fine-tuning and Alignment | L5 E9 |
| [M18](part-11-language-models/m18-serving-evaluation-and-cost/README.md) | Serving, Evaluation, and Cost | L4 E7 |
| [M19](part-11-language-models/m19-capstone/README.md) | Capstone: Build, Fine-tune, Evaluate, and Ship | P24 |

---

## How this level is taught

**Build it before you call it.** Autodiff, backpropagation, attention, the
transformer block, a tokeniser, and a language model are each implemented from
scratch and then checked numerically against the library version. The library
is introduced only after you have written the thing it replaces, which is why
Module M16 comes after Module M15 rather than before it.

**Derive what you implement.** The maths appears where a module needs it, not in
a block at the front. Backpropagation is derived by hand exactly once, in Module
M06, because everything after it is a corollary.

**Every claim is measured.** This is the same rule as the rest of the course. A
statement that quantisation costs quality, or that continuous batching helps, is
worth nothing here without your own numbers.

**The data is the model.** Modules M01, M04, M15, and M17 all return to the same
point from different directions: dataset problems outnumber architecture
problems, and an evaluation built after the model is not an evaluation.

---

## Hardware

You do not need a GPU to complete this level, and you should not buy one before
Module M07.

| Path | What it covers |
|---|---|
| CPU only | Parts 8 and 9 comfortably. Reduced configurations for M08, M11, M12, M13, and a character-level configuration for M15 that trains in about twenty minutes. |
| Free hosted notebook | Everything, with session limits. The recommended path for M12, M13, and M17 if you have no local GPU. |
| One consumer GPU with 12GB or more | Everything at the reference configuration, including QLoRA fine tuning of a seven billion parameter model in Module M17. |

Every module states its own compute budget and its fallback.

## How this level connects to the rest of the course

| From | Used here |
|---|---|
| Advanced Module 29 | NumPy, pandas, and the scikit-learn estimator API, assumed from Module M01 |
| Advanced Module 23 | Measure before you change, applied to every performance claim |
| Advanced Modules 20 and 30 | The packaging and CLI discipline behind the experiment harness in M04 |
| Advanced Module 28 | The FastAPI service that becomes the inference server in M18 |
| System Design Module 32 | Worker and concurrency models, reused for inference serving |
| System Design Module 35 | Observability, reused for model monitoring and drift |
| System Design Module 36 | The design document format and review checklist, reused by the M19 capstone |

Level 04 is not a strict prerequisite, but Modules M18 and M19 assume its
vocabulary. If you are taking the levels in order, you already have it.
