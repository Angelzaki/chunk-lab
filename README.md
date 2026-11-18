<div align="center">

# chunk-lab

**Laboratorio de chunking local** · Angel Salazar

`fixed | paragraph | sentence → retrieval score`

</div>

---

### `$ whoami`

```text
pregunta: ¿qué fragmentación recupera mejor el doc fuente?
respuesta: se mide, no se discute
runtime: offline
```

---

### `$ ./lab.sh`

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pytest
python -m chunk_lab
```

Artefactos: `results/chunk_experiment.json` · `.md`

---

### `$ cat strategies.md`

| strategy | idea |
|---|---|
| `fixed` | ventana fija + overlap |
| `paragraph` | bloques por párrafo |
| `sentence` | oraciones hasta un tope |

Métrica: hit@k del `doc_id` esperado.

---

### `$ ls related`

`retrieval-tuner-local` · `local-rag-pipeline` · `rag-eval-platform`

---

Hecho en Lima · Angel Salazar · CIP 404730
