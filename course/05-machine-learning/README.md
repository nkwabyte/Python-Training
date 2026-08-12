# Level 05 — Machine Learning

**Start here if you can write and ship real Python, and you now want to build
models rather than call them.**

Twenty one modules from what learning is, through the classical toolbox and deep
learning in PyTorch, to generative models, to pretraining a small language model
of your own and fine tuning a large one, ending with how to choose the right
approach in the first place. Every architecture is built from parts before a
library is allowed to build it for you.

| | |
|---|---|
| Modules | M01 to M21, in Parts 8, 9, 10, and 11 |
| Duration | 18 weeks |
| Weekly load | 10 to 15 hours |
| Prerequisite | Level 03, in particular Module 29 for NumPy and pandas |
| Framework | PyTorch throughout, with the Hugging Face stack layered on top from Module M17 |
| Ends with | A model you pretrained, a model you fine tuned, a decision record that justifies both, and a service that serves them |

---

## Part 8 — Foundations of Learning

Weeks 1 to 4. What learning is, the maths you will actually use, the classical
toolbox, and the experimental discipline, while the models are still small
enough to run in seconds.

| Module | Title | Time |
|---|---|---|
| [M01](part-8-ml-foundations/m01-what-learning-is/README.md) | What Learning Is | L4 E5 |
| [M02](part-8-ml-foundations/m02-the-maths-you-will-use/README.md) | The Maths You Will Actually Use | L5 E6 |
| [M03](part-8-ml-foundations/m03-linear-models-and-gradient-descent/README.md) | Linear Models and Gradient Descent from Scratch | L4 E6 |
| [M04](part-8-ml-foundations/m04-evaluation-and-the-experimental-loop/README.md) | Evaluation, Data, and the Experimental Loop | L4 E6 |
| [M05](part-8-ml-foundations/m05-classical-toolbox/README.md) | The Classical Toolbox: Trees, Ensembles, and Unsupervised Methods | L5 E7 |

## Part 9 — Deep Learning with PyTorch

Weeks 5 to 9. Tensors, autograd, backpropagation derived by hand, the training
diagnostics nobody writes down, then convolution, recurrence, and the
transformer built from tensors up.

| Module | Title | Time |
|---|---|---|
| [M06](part-9-deep-learning/m06-tensors-and-autograd/README.md) | Tensors and Autograd | L4 E6 |
| [M07](part-9-deep-learning/m07-neural-networks/README.md) | Neural Networks, Derived and Built | L5 E7 |
| [M08](part-9-deep-learning/m08-training-that-works/README.md) | Training That Actually Works | L5 E7 |
| [M09](part-9-deep-learning/m09-convolutional-networks-and-vision/README.md) | Convolutional Networks and Vision | L4 E7 |
| [M10](part-9-deep-learning/m10-sequences-and-attention/README.md) | Sequences, Recurrence, and the Road to Attention | L4 E6 |
| [M11](part-9-deep-learning/m11-the-transformer/README.md) | The Transformer, Built from Parts | L5 E8 |

## Part 10 — Generative Models

Weeks 10 to 12. Modelling the data rather than the label: latent spaces,
adversarial training, and denoising. Each of the three is implemented and
trained from scratch, and the last two are then also adapted from pretrained
checkpoints, because that is how generative models are used in practice.

| Module | Title | Time |
|---|---|---|
| [M12](part-10-generative-models/m12-autoencoders-and-vaes/README.md) | Autoencoders and Variational Autoencoders | L4 E6 |
| [M13](part-10-generative-models/m13-gans/README.md) | Generative Adversarial Networks, trained and fine-tuned | L5 E9 |
| [M14](part-10-generative-models/m14-diffusion-models/README.md) | Diffusion Models, trained and adapted | L5 E9 |

## Part 11 — Language Models and LLMs

Weeks 13 to 18. Tokenisation, a small language model you pretrain yourself, the
open ecosystem, fine tuning and alignment, serving, how to choose an approach at
all, and the capstone.

| Module | Title | Time |
|---|---|---|
| [M15](part-11-language-models/m15-tokenisation-and-language-modelling/README.md) | Tokenisation and Language Modelling | L4 E6 |
| [M16](part-11-language-models/m16-build-a-mini-llm/README.md) | Build a Mini LLM from Scratch | P16 |
| [M17](part-11-language-models/m17-pretrained-models-and-the-ecosystem/README.md) | Pretrained Models and the Open Ecosystem | L4 E6 |
| [M18](part-11-language-models/m18-fine-tuning-and-alignment/README.md) | Fine-tuning and Alignment | L5 E9 |
| [M19](part-11-language-models/m19-serving-evaluation-and-cost/README.md) | Serving, Evaluation, and Cost | L4 E7 |
| [M20](part-11-language-models/m20-choosing-an-approach/README.md) | Choosing an Approach: Matching Model to Problem | L3 E8 |
| [M21](part-11-language-models/m21-capstone/README.md) | Capstone: Build, Fine-tune, Evaluate, and Ship | P24 |

---

## How this level is taught

**Build it before you call it.** Autodiff, backpropagation, attention, the
transformer block, a tokeniser, and a language model are each implemented from
scratch and then checked numerically against the library version. The library is
introduced only after you have written the thing it replaces, which is why
Module M17 comes after Module M16 rather than before it.

**Derive what you implement.** The maths appears where a module needs it, not in
a block at the front. Backpropagation is derived by hand exactly once, in Module
M07, because everything after it is a corollary.

**Every claim is measured.** This is the same rule as the rest of the course. A
statement that quantisation costs quality, or that continuous batching helps, is
worth nothing here without your own numbers.

**The data is the model.** Modules M01, M04, M16, and M18 all return to the same
point from different directions: dataset problems outnumber architecture
problems, and an evaluation built after the model is not an evaluation.

**The strongest baseline goes first.** Module M05 builds a gradient boosted model
before any neural network appears, and Part 9 has to beat it. Frequently it does
not, and that result is the point rather than an embarrassment.

**Choosing is a skill, not an afterthought.** Module M20 drills the decision on
thirty cases before the capstone applies it once.

---

## Hardware

You do not need a GPU to complete this level, and you should not buy one before
Module M08.

| Path | What it covers |
|---|---|
| CPU only | Parts 8 and 9 comfortably. Reduced configurations for M09, M12, M13, M14, and a character-level configuration for M16 that trains in about twenty minutes. |
| Free hosted notebook | Everything, with session limits. The recommended path for M13, M14, and M18 if you have no local GPU. |
| One consumer GPU with 12GB or more | Everything at the reference configuration, including QLoRA fine tuning of a seven billion parameter model in Module M18. |

Every module states its own compute budget and its fallback.

## How this level connects to the rest of the course

| From | Used here |
|---|---|
| Advanced Module 29 | NumPy, pandas, and the scikit-learn estimator API, assumed from Module M01 and extended in M05 |
| Advanced Module 23 | Measure before you change, applied to every performance claim |
| Advanced Modules 20 and 30 | The packaging and CLI discipline behind the experiment harness in M04 |
| Advanced Module 28 | The FastAPI service that becomes the inference server in M19 |
| System Design Module 32 | Worker and concurrency models, reused for inference serving |
| System Design Module 35 | Observability, reused for model monitoring and drift |
| System Design Module 36 | The design document format and review checklist, reused by the M20 decision record and the M21 capstone |

Level 04 is not a strict prerequisite, but Modules M19, M20, and M21 assume its
vocabulary. If you are taking the levels in order, you already have it.
