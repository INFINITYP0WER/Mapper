# SBS V2/V3 AI-Powered Mapping System
## Complete Implementation Guide for Healthcare Providers

---

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Installation & Setup](#installation--setup)
4. [Usage Guide](#usage-guide)
5. [Configuration](#configuration)
6. [Output Files](#output-files)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)
9. [API Reference](#api-reference)

---

## Overview

### Purpose
This AI-powered mapping system helps healthcare providers in Saudi Arabia:
- Map between SBS V2 and V3 billing codes
- Match SBS codes to internal price lists
- Automate code matching based on service descriptions
- Identify ambiguous or uncertain matches for manual review
- Generate comprehensive mapping reports

### Key Features
- **Intelligent Matching**: Uses multiple AI algorithms (Jaccard similarity, Levenshtein distance)
- **Confidence Scoring**: Assigns confidence levels to each match
- **Batch Processing**: Handles thousands of records efficiently
- **Review Flagging**: Automatically identifies records needing manual review
- **Multiple Export Formats**: Excel, JSON, CSV outputs
- **Visualization**: Charts and graphs for mapping quality assessment

### Who Should Use This
- **Insurance Managers**: Map provider service lists to SBS codes
- **Billing Departments**: Automate price list updates
- **Revenue Cycle Teams**: Ensure accurate code mapping
- **IT Teams**: Integrate with existing billing systems

---

## System Architecture

### Components

```
┌─────────────────────────────────────────────────┐
│         SBS AI Mapping System                    │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐      ┌──────────────┐        │
│  │  Text        │      │  Similarity  │        │
│  │  Normalizer  │─────>│  Calculator  │        │
│  └──────────────┘      └──────────────┘        │
│                                │                 │
│                                v                 │
│                     ┌──────────────────┐        │
│                     │  Mapping Engine  │        │
│                     └──────────────────┘        │
│                                │                 │
│                                v                 │
│                     ┌──────────────────┐        │
│                     │  Validator       │        │
│                     └──────────────────┘        │
│                                                  │
└─────────────────────────────────────────────────┘
                       │
                       v
        ┌──────────────────────────────┐
        │  Output Files                 │
        │  - Mapping Results            │
        │  - High Confidence Matches    │
        │  - Review List                │
        │  - Statistical Reports        │
        └──────────────────────────────┘
```

### Matching Algorithm

The system uses a weighted combination of:

1. **Jaccard Similarity** (40% weight)
   - Compares keyword sets
   - Good for identifying similar concepts

2. **Normalized Levenshtein Distance** (60% weight)
   - Character-by-character comparison
   - Good for catching typos and variations

**Final Score = (0.4 × Jaccard) + (0.6 × Levenshtein)**

### Confidence Levels

| Score Range | Confidence Level | Recommendation |
|-------------|-----------------|----------------|
| 95-100% | Exact Match | Auto-approve |
| 90-94% | High Confidence | Spot check |
| 70-89% | Medium Confidence | Review recommended |
| 50-69% | Low Confidence | Manual review required |
| <50% | Very Low / No Match | Create new mapping |

---

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Microsoft Excel (for viewing results)

### Step 1: Install Python Dependencies

```bash
pip install pandas numpy openpyxl xlsxwriter matplotlib seaborn jupyter
```

### Step 2: Download System Files

Place the following files in your working directory:
- `sbs_ai_mapping_system.py` - Core engine
- `sbs_mapping_notebook.ipynb` - Interactive notebook
- `sbs_mapping_cli.py` - Command-line interface (optional)

### Step 3: Prepare Your Data

You'll need:
1. **SBS V2-V3 Mapping File** (`SBS_V2_to_V3_Map.xlsx`)
   - Provided by CHI
   - Contains official V2 to V3 mappings

2. **Your Price List** (Excel or CSV)
   - Must contain:
     - Service codes
     - Service descriptions
     - Prices (optional but recommended)

### Step 4: Verify Installation

```python
from sbs_ai_mapping_system import SBSMappingEngine
engine = SBSMappingEngine()
print("✓ Installation successful!")
```

---

## Usage Guide

### Method 1: Interactive Notebook (Recommended for First-Time Users)

1. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook sbs_mapping_notebook.ipynb
   ```

2. **Follow the step-by-step cells**:
   - Each cell is documented
   - Run cells in order (Shift+Enter)
   - Customize parameters as needed

3. **Review outputs**:
   - Charts appear inline
   - Files saved to working directory

### Method 2: Python Script

```python
from sbs_ai_mapping_system import SBSMappingEngine, MappingValidator

# Initialize
engine = SBSMappingEngine()

# Load data
v2_v3_map = engine.load_sbs_v2_v3_mapping('SBS_V2_to_V3_Map.xlsx')
price_list = engine.load_price_list(
    'your_pricelist.xlsx',
    code_column='Service_Code',
    description_column='Service_Description',
    price_column='Unit_Price'
)

# Run mapping
results = engine.map_to_price_list(
    sbs_df=v2_v3_map,
    sbs_code_col='V3_Code',
    sbs_desc_col='V3_Description',
    min_threshold=0.60
)

# Generate reports
report = engine.generate_mapping_report(results, 'report.json')
review_list = MappingValidator.generate_review_list(results, 'review.xlsx')

# Export
results.to_excel('final_results.xlsx', index=False)
```

### Method 3: Command-Line Interface

```bash
python sbs_mapping_cli.py \
    --v2v3-file SBS_V2_to_V3_Map.xlsx \
    --pricelist your_pricelist.xlsx \
    --code-col "Service Code" \
    --desc-col "Description" \
    --price-col "Price" \
    --threshold 0.60 \
    --output mapping_results.xlsx
```

---

## Configuration

### Key Parameters

#### Similarity Threshold
```python
min_threshold = 0.60  # 60% minimum similarity
```
- **0.50-0.60**: More matches, lower quality
- **0.60-0.70**: Balanced (recommended)
- **0.70-0.80**: Fewer matches, higher quality
- **0.80+**: Very strict, may miss valid matches

#### Weighting Adjustments
```python
# In SimilarityCalculator.weighted_similarity()
jaccard_weight = 0.4      # Keyword matching
levenshtein_weight = 0.6  # Character matching
```

Adjust based on your data:
- **More structured descriptions**: Increase Jaccard weight
- **Many typos/variations**: Increase Levenshtein weight

#### Column Name Mapping
```python
# When loading price list
engine.load_price_list(
    filepath='pricelist.xlsx',
    code_column='YOUR_CODE_COLUMN_NAME',
    description_column='YOUR_DESC_COLUMN_NAME',
    price_column='YOUR_PRICE_COLUMN_NAME'
)
```

---

## Output Files

### 1. Complete Mapping Results
**File**: `complete_mapping_results.xlsx`

Columns:
- `sbs_code`: SBS billing code
- `sbs_description`: SBS service description
- `matched_pricelist_code`: Your matched code
- `matched_pricelist_description`: Your matched description
- `similarity_score`: Match quality (0-1)
- `confidence`: Confidence level
- `price`: Price from your list
- `alternative_matches`: Number of other potential matches
- `second_best_score`: Next best match score

### 2. High Confidence Matches
**File**: `high_confidence_mappings.xlsx`

Filtered results with confidence >= 90%
- Ready to import into your system
- Minimal review needed

### 3. Manual Review List
**File**: `items_for_manual_review.xlsx`

Records flagged for review:
- Low confidence (<70%)
- Ambiguous (multiple similar matches)
- Includes `is_ambiguous` and `requires_review` flags

### 4. Statistical Report
**File**: `mapping_report.json`

```json
{
  "total_records": 5000,
  "matched_records": 4650,
  "match_rate": 0.93,
  "average_similarity_score": 0.847,
  "high_confidence_matches": 4200,
  "high_confidence_rate": 0.84,
  "confidence_distribution": {
    "Exact Match": 1500,
    "High Confidence": 2700,
    "Medium Confidence": 450,
    "Low Confidence": 200,
    "No Match Found": 150
  }
}
```

### 5. Visualization
**File**: `mapping_visualization.png`

Four charts:
- Confidence distribution
- Similarity score histogram
- Match vs. no-match pie chart
- Alternative matches distribution

---

## Best Practices

### Data Preparation

1. **Clean your price list**:
   ```python
   # Remove duplicates
   pricelist = pricelist.drop_duplicates(subset=['code', 'description'])
   
   # Remove empty descriptions
   pricelist = pricelist[pricelist['description'].notna()]
   ```

2. **Standardize descriptions**:
   - Use consistent terminology
   - Avoid excessive abbreviations
   - Include key medical terms

3. **Backup original data**:
   - Keep copies before running mapping
   - Version control your price list

### Mapping Process

1. **Start with high threshold** (0.70+):
   - Get high-quality matches first
   - Gradually lower threshold if needed

2. **Review samples**:
   - Check 10-20 random matches
   - Verify accuracy before bulk approval

3. **Handle no-matches**:
   - Extract unmatched codes
   - Manually create mappings
   - Add to system for future use

4. **Iterative refinement**:
   - Run mapping
   - Review flagged items
   - Update descriptions
   - Re-run mapping

### Quality Assurance

1. **Spot check high-confidence**:
   - Even 95%+ matches can be wrong
   - Sample 5-10% for verification

2. **Focus review effort**:
   - Priority: Medium confidence (70-89%)
   - Skip: Exact matches (95%+)
   - Flag: Low confidence (<70%)

3. **Track corrections**:
   - Document manual overrides
   - Build a feedback loop

---

## Troubleshooting

### Common Issues

#### Issue: Low Match Rate (<50%)

**Causes**:
- Threshold too high
- Different terminology/language
- Incomplete descriptions

**Solutions**:
```python
# Lower threshold
min_threshold = 0.50

# Check description quality
print(pricelist['description'].head(20))

# Review unmatched items
unmatched = results[results['similarity_score'] == 0]
print(unmatched[['sbs_description']].head())
```

#### Issue: Too Many Ambiguous Matches

**Causes**:
- Similar service descriptions
- Generic terminology

**Solutions**:
```python
# Increase score difference threshold
MappingValidator.flag_ambiguous_matches(
    mapping_results,
    score_difference_threshold=0.10  # Require 10% difference
)

# Add code similarity to weighting
# (Modify SimilarityCalculator.weighted_similarity())
```

#### Issue: Wrong Matches Despite High Scores

**Causes**:
- Keywords overlap but services differ
- Need domain-specific matching

**Solutions**:
1. Add medical specialty filtering
2. Use block/category grouping
3. Implement exclusion rules

```python
# Example: Filter by category
dental_codes = results[results['sbs_code'].str.startswith('97')]
```

#### Issue: Memory Error with Large Files

**Solutions**:
```python
# Process in batches
batch_size = 1000
results = []

for i in range(0, len(sbs_df), batch_size):
    batch = sbs_df.iloc[i:i+batch_size]
    batch_results = engine.map_to_price_list(batch, ...)
    results.append(batch_results)

final_results = pd.concat(results)
```

---

## API Reference

### SBSMappingEngine

Main class for mapping operations.

#### Methods

**`__init__()`**
Initialize the mapping engine.

**`load_sbs_v2_v3_mapping(filepath: str) -> pd.DataFrame`**
Load official SBS V2-V3 mapping file.

**`load_price_list(filepath: str, code_column: str, description_column: str, price_column: str) -> pd.DataFrame`**
Load healthcare provider price list.

**`find_best_match(source_description: str, target_df: pd.DataFrame, description_column: str, code_column: str, top_n: int = 5, min_threshold: float = 0.5) -> List[Dict]`**
Find top matching records for a single description.

**`map_to_price_list(sbs_df: pd.DataFrame, sbs_code_col: str, sbs_desc_col: str, min_threshold: float = 0.6) -> pd.DataFrame`**
Map entire SBS dataset to price list.

**`generate_mapping_report(mapping_df: pd.DataFrame, output_path: str = None) -> Dict`**
Generate statistical report on mapping results.

### MappingValidator

Class for validating and reviewing mappings.

#### Methods

**`flag_ambiguous_matches(mapping_df: pd.DataFrame, score_difference_threshold: float = 0.05) -> pd.DataFrame`**
Flag records with ambiguous matches.

**`generate_review_list(mapping_df: pd.DataFrame, output_path: str = None) -> pd.DataFrame`**
Generate list of items requiring manual review.

### TextNormalizer

Utilities for text preprocessing.

#### Methods

**`normalize(text: str) -> str`**
Normalize text for matching.

**`extract_keywords(text: str) -> List[str]`**
Extract important keywords from medical descriptions.

### SimilarityCalculator

Calculate similarity between descriptions.

#### Methods

**`jaccard_similarity(text1: str, text2: str) -> float`**
Calculate Jaccard coefficient (0-1).

**`normalized_levenshtein(text1: str, text2: str) -> float`**
Calculate normalized Levenshtein similarity (0-1).

**`weighted_similarity(text1: str, text2: str, jaccard_weight: float = 0.4, levenshtein_weight: float = 0.6) -> float`**
Calculate weighted combination of metrics.

**`code_similarity(code1: str, code2: str) -> float`**
Calculate similarity between SBS codes.

---

## Support & Maintenance

### Getting Help

1. Review this documentation
2. Check the troubleshooting section
3. Examine example code in notebook
4. Review output files for clues

### Updating the System

When SBS codes update:
1. Get new mapping file from CHI
2. Re-run mapping process
3. Compare with previous results
4. Update validated mappings

### Data Retention

Recommended:
- Keep all mapping results (dated)
- Version control price lists
- Archive review decisions
- Maintain audit trail

---

## Advanced Topics

### Custom Matching Logic

Extend the system for your needs:

```python
class CustomMappingEngine(SBSMappingEngine):
    def specialty_filter(self, sbs_code, specialty):
        """Filter by medical specialty"""
        specialty_prefixes = {
            'dental': '97',
            'imaging': '55',
            'lab': '73'
        }
        prefix = specialty_prefixes.get(specialty)
        return sbs_code.startswith(prefix) if prefix else True
```

### Integration with Billing Systems

Export format for common systems:

```python
# For SQL import
results[['sbs_code', 'matched_pricelist_code', 'price']].to_csv(
    'import.csv',
    index=False,
    header=False  # For bulk SQL INSERT
)

# For API integration
import json
api_format = results.to_dict('records')
with open('api_import.json', 'w') as f:
    json.dump(api_format, f)
```

### Scheduled Automation

```python
import schedule
import time

def automated_mapping():
    engine = SBSMappingEngine()
    # Load latest files
    # Run mapping
    # Email results
    pass

schedule.every().monday.at("02:00").do(automated_mapping)

while True:
    schedule.run_pending()
    time.sleep(3600)
```

---

## Appendix

### File Formats

#### Input File Requirements

**SBS V2-V3 Mapping**:
- Format: Excel (.xlsx)
- Required columns: Code columns, Description columns
- Encoding: UTF-8

**Price List**:
- Format: Excel (.xlsx) or CSV (.csv)
- Required columns: Code, Description
- Optional: Price, Category, Status
- Encoding: UTF-8

#### Output File Specifications

All Excel outputs:
- Format: .xlsx
- Encoding: UTF-8
- Include headers
- Date-stamped filenames optional

### Glossary

- **SBS**: Saudi Billing System
- **CHI**: Council of Health Insurance
- **Jaccard**: Set-based similarity metric
- **Levenshtein**: Edit distance metric
- **Confidence Score**: Quality measure for matches
- **Ambiguous Match**: Multiple similar-scoring matches

### Version History

- **v1.0** - Initial release
- **v1.1** - Added batch processing
- **v1.2** - Improved Arabic text handling
- **v2.0** - AI-powered matching engine

---

**Document Version**: 2.0  
**Last Updated**: February 2026  
**Prepared for**: Healthcare Insurance Managers, Saudi Arabia
