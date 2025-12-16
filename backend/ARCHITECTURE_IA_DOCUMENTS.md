# Architecture : Lien entre IA et Documents

## 📊 Vue d'ensemble

**OUI**, le dossier `IA` est **directement lié** au dossier `documents` pour l'extraction de texte. Voici comment :

## 🔗 Flux de données complet

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUX COMPLET                              │
└─────────────────────────────────────────────────────────────┘

1. UPLOAD DOCUMENT
   └─> POST /api/documents/upload
       └─> documents/routes.py
           └─> documents/service.py::upload_document()
               ├─> Sauvegarde le fichier (PDF/DOCX/TXT)
               ├─> documents/extractor.py::extract_text_from_file()
               │   ├─> _read_pdf() pour PDF (PyMuPDF)
               │   ├─> _read_docx() pour DOCX (python-docx)
               │   └─> _read_txt() pour TXT
               └─> Crée Document avec extracted_text stocké en DB
                   └─> documents/models.py::Document
                       └─> extracted_text (db.Column(db.Text))

2. GÉNÉRATION QCM
   └─> POST /api/ia/generate
       └─> IA/routes.py::generate_qcm()
           └─> IA/service.py::generate_and_save_qcm()
               ├─> DocumentService.get_document_by_id(document_id)
               │   └─> Récupère le Document avec extracted_text
               ├─> Vérifie que extracted_text n'est pas vide
               ├─> GeminiQCMGenerator.generate_qcm_json()
               │   └─> Utilise extracted_text comme document_text
               └─> QCMRepository.create_qcm()
                   └─> Sauvegarde le QCM avec document_id (ForeignKey)
```

## 🔍 Détails des liens

### 1. Import dans IA/service.py

```python
# backend/src/IA/service.py ligne 1
from src.documents.service import DocumentService
```

**Lien direct** : Le service IA importe le service Documents.

### 2. Utilisation dans generate_and_save_qcm()

```python
# backend/src/IA/service.py lignes 10-16
document = DocumentService.get_document_by_id(document_id)
if not document:
    return None, "Document introuvable."

extracted_text = document.extracted_text  # ← Texte déjà extrait !
if not extracted_text:
    return None, "Texte du document vide. Veuillez le ré-extraire."
```

**Point clé** : Le texte est **déjà extrait** lors de l'upload. L'IA utilise simplement ce texte stocké.

### 3. Relation base de données

```python
# backend/src/IA/models.py ligne 10
document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
```

**Lien DB** : Le modèle QCM a une **ForeignKey** vers `documents.id`, créant une relation directe.

### 4. Extraction du texte (dans documents/)

```python
# backend/src/documents/service.py lignes 28-30
# INTELLIGENT EXTRACTION (The Core Value)
# We extract text NOW so the AI is fast LATER.
extracted_text = extract_text_from_file(file_path)
```

**Moment d'extraction** : Le texte est extrait **immédiatement lors de l'upload**, pas lors de la génération de QCM.

## 📁 Structure des fichiers

```
backend/src/
├── documents/
│   ├── __init__.py
│   ├── models.py          → Document (avec extracted_text)
│   ├── service.py         → DocumentService (upload + extraction)
│   ├── extractor.py       → extract_text_from_file()
│   ├── repository.py      → DocumentRepository
│   └── routes.py          → POST /api/documents/upload
│
└── IA/
    ├── __init__.py
    ├── models.py          → QCM (avec document_id ForeignKey)
    ├── service.py         → QCMService (importe DocumentService)
    ├── gemini_model.py    → GeminiQCMGenerator
    ├── repository.py      → QCMRepository
    └── routes.py          → POST /api/ia/generate
```

## ✅ Points importants

### 1. **Extraction en amont**
- ✅ Le texte est extrait **lors de l'upload** du document
- ✅ Stocké dans `Document.extracted_text` (colonne DB de type TEXT)
- ✅ L'IA n'a pas besoin de ré-extraire, elle lit directement depuis la DB

### 2. **Performance optimisée**
- ✅ Extraction une seule fois (lors de l'upload)
- ✅ Génération de QCM rapide (pas besoin de re-lire le fichier)
- ✅ Le texte est prêt pour l'IA immédiatement

### 3. **Dépendances**
- ✅ `IA/service.py` dépend de `documents/service.py`
- ✅ `IA/models.py` a une ForeignKey vers `documents.id`
- ✅ Pas de dépendance circulaire (documents n'importe pas IA)

### 4. **Validation**
- ✅ Vérification que le document existe
- ✅ Vérification que `extracted_text` n'est pas vide
- ✅ Message d'erreur clair si le texte est vide

## 🔄 Flux de données détaillé

### Étape 1 : Upload Document
```python
# User upload file
POST /api/documents/upload
  ↓
DocumentService.upload_document()
  ↓
extract_text_from_file(file_path)  # Extrait le texte
  ↓
Document(
  filename="cours.pdf",
  extracted_text="Le contenu complet du PDF...",  # Stocké ici
  user_id=1
)
  ↓
Sauvegarde en DB avec extracted_text
```

### Étape 2 : Génération QCM
```python
# User demande génération QCM
POST /api/ia/generate {"document_id": 1}
  ↓
QCMService.generate_and_save_qcm(document_id=1)
  ↓
DocumentService.get_document_by_id(1)  # Récupère le Document
  ↓
document.extracted_text  # Lit le texte déjà extrait
  ↓
GeminiQCMGenerator.generate_qcm_json(
  document_text=extracted_text  # Utilise le texte stocké
)
  ↓
QCM(
  title="QCM...",
  document_id=1,  # Lien vers le document
  questions=[...]
)
```

## 🎯 Résumé

| Aspect | Détails |
|--------|---------|
| **Lien** | ✅ OUI, IA est directement lié à Documents |
| **Import** | `IA/service.py` importe `DocumentService` |
| **Relation DB** | `QCM.document_id` → `Document.id` (ForeignKey) |
| **Extraction** | Fait lors de l'upload, pas lors de la génération |
| **Texte utilisé** | `Document.extracted_text` (déjà stocké en DB) |
| **Dépendance** | IA dépend de Documents (pas l'inverse) |

## ⚠️ Points d'attention

1. **Le texte doit être extrait avant la génération**
   - Si `extracted_text` est vide, la génération échouera
   - Message : "Texte du document vide. Veuillez le ré-extraire."

2. **L'extraction se fait lors de l'upload**
   - Si l'extraction échoue à l'upload, le document ne sera pas créé
   - Message : "Could not extract text. File might be empty or a scanned image."

3. **Le document doit exister**
   - Si `document_id` n'existe pas, erreur : "Document introuvable."

## 🔧 Vérification du lien

Pour vérifier que tout est bien lié, regardez :

1. **Import** : `backend/src/IA/service.py` ligne 1
   ```python
   from src.documents.service import DocumentService
   ```

2. **Utilisation** : `backend/src/IA/service.py` ligne 10
   ```python
   document = DocumentService.get_document_by_id(document_id)
   ```

3. **Relation DB** : `backend/src/IA/models.py` ligne 10
   ```python
   document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
   ```

**Conclusion** : Le lien est **solide et bien structuré** ! ✅

