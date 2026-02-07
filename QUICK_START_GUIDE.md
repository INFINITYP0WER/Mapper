# SBS Mapping System - Quick Start Guide
## Get Up and Running in 5 Minutes

---

## What You'll Need

Before starting, gather:
1. ✓ **SBS V2-V3 Mapping File** - `SBS_V2_to_V3_Map.xlsx` (from CHI)
2. ✓ **Your Price List** - Excel or CSV file with service codes and descriptions
3. ✓ **Python 3.7+** - Download from python.org if needed
4. ✓ **30 minutes** - For initial setup and first run

---

## Step 1: Install Dependencies (2 minutes)

Open your terminal/command prompt and run:

```bash
pip install pandas numpy openpyxl matplotlib seaborn
```

**Verify installation:**
```bash
python --version
# Should show Python 3.7 or higher
```

---

## Step 2: Download System Files (1 minute)

Save these files to a new folder (e.g., `sbs_mapping`):
- `sbs_ai_mapping_system.py` - The core engine
- `sbs_mapping_cli.py` - Command-line tool
- `sbs_mapping_notebook.ipynb` - Interactive notebook (optional)

---

## Step 3: Prepare Your Data (5 minutes)

### A. Check Your Price List Format

Open your price list in Excel. It should have:
- **Code column**: Service codes (e.g., "SRV001", "PROC-123")
- **Description column**: Service descriptions
- **Price column**: Prices (optional)

**Example:**
| Code | Description | Price |
|------|-------------|-------|
| SRV001 | Comprehensive oral examination | 150.00 |
| SRV002 | Dental x-ray, bitewing | 75.00 |

### B. Note Your Column Names

Write down the exact column names from your price list:
- Code column: __________________
- Description column: __________________
- Price column: __________________

---

## Step 4: Run Your First Mapping (10 minutes)

### Option A: Command Line (Recommended for First Time)

Open terminal in your `sbs_mapping` folder and run:

```bash
python sbs_mapping_cli.py \
  --v2v3-file SBS_V2_to_V3_Map.xlsx \
  --pricelist YOUR_PRICELIST.xlsx \
  --code-col "YOUR_CODE_COLUMN" \
  --desc-col "YOUR_DESCRIPTION_COLUMN" \
  --price-col "YOUR_PRICE_COLUMN"
```

**Real Example:**
```bash
python sbs_mapping_cli.py \
  --v2v3-file SBS_V2_to_V3_Map.xlsx \
  --pricelist hospital_services.xlsx \
  --code-col "Service Code" \
  --desc-col "Service Description" \
  --price-col "Unit Price"
```

### Option B: Interactive Notebook (Better for Learning)

```bash
jupyter notebook sbs_mapping_notebook.ipynb
```

Then follow the step-by-step cells in your browser.

---

## Step 5: Review Results (10 minutes)

After the process completes, you'll have these files:

### 1. **mapping_results.xlsx** - Complete Results
Open this to see all mappings with similarity scores.

**Key columns:**
- `sbs_code` - SBS billing code
- `matched_pricelist_code` - Your matched code
- `similarity_score` - Match quality (0-100%)
- `confidence` - Quality level

### 2. **high_confidence_mappings.xlsx** - Ready to Use
These mappings scored 90%+ and can be used immediately.

**Action:** Import these into your billing system.

### 3. **items_for_review.xlsx** - Need Attention
These need manual verification.

**Action:** Review and correct as needed.

### 4. **mapping_report.json** - Statistics
Summary of mapping quality.

---

## Understanding Your Results

### Confidence Levels

| Level | Score | What It Means | Action |
|-------|-------|---------------|--------|
| ✅ Exact Match | 95-100% | Perfect match | Use immediately |
| ✅ High Confidence | 90-94% | Very good match | Spot check a few |
| ⚠️ Medium | 70-89% | Good match | Review recommended |
| ⚠️ Low | 50-69% | Possible match | Manual review required |
| ❌ No Match | <50% | No good match | Create manual mapping |

### What to Look For

**Good Signs:**
- Match rate > 80%
- High confidence rate > 70%
- Average similarity > 75%

**Warning Signs:**
- Match rate < 50% → Check threshold or data quality
- Many ambiguous matches → Descriptions too similar
- High confidence rate < 50% → Review configuration

---

## Common First-Time Issues

### Issue 1: "No matches found" or very low match rate

**Solution:**
```bash
# Lower the threshold
python sbs_mapping_cli.py \
  --threshold 0.50 \
  [other parameters]
```

### Issue 2: "Column not found" error

**Solution:**
- Check exact column names in your price list
- Column names are case-sensitive
- Use quotes for names with spaces

### Issue 3: Too many items for review

**Solution:**
```bash
# Raise the threshold
python sbs_mapping_cli.py \
  --threshold 0.70 \
  [other parameters]
```

### Issue 4: Process is very slow

**Solution:**
- Large files (10,000+ rows) take longer
- Close other programs
- Process will show progress messages
- Be patient - first run takes longest

---

## Next Steps

### After Your First Successful Run:

1. **Review Sample Matches**
   - Open `high_confidence_mappings.xlsx`
   - Check 10-20 random rows
   - Verify codes match correctly

2. **Handle Manual Reviews**
   - Open `items_for_review.xlsx`
   - Sort by `similarity_score`
   - Start with highest scores first
   - Update descriptions if needed
   - Re-run mapping

3. **Prepare for Import**
   - Export validated mappings
   - Format for your billing system
   - Test with small batch first
   - Full deployment

4. **Set Up Periodic Updates**
   - Map new SBS codes quarterly
   - Update when price list changes
   - Keep audit trail

---

## Quick Reference: Command Options

```bash
# Basic usage
python sbs_mapping_cli.py \
  --v2v3-file [SBS_FILE] \
  --pricelist [YOUR_FILE]

# Custom threshold
--threshold 0.70

# Custom output location
--output-dir ./results

# Add filename prefix
--output-prefix "2026_Q1"

# Skip visualizations (faster)
--no-visualizations

# Quiet mode
--quiet

# Get help
python sbs_mapping_cli.py --help
```

---

## Cheat Sheet: Typical Workflows

### Scenario 1: First Time Setup
```bash
# Start with balanced threshold
python sbs_mapping_cli.py \
  --v2v3-file SBS_V2_to_V3_Map.xlsx \
  --pricelist hospital_prices.xlsx \
  --threshold 0.60 \
  --output-dir ./initial_mapping
```

### Scenario 2: High Quality Matches Only
```bash
# Strict matching
python sbs_mapping_cli.py \
  --v2v3-file SBS_V2_to_V3_Map.xlsx \
  --pricelist hospital_prices.xlsx \
  --threshold 0.80
```

### Scenario 3: Quarterly Update
```bash
# With date prefix
python sbs_mapping_cli.py \
  --v2v3-file SBS_V2_to_V3_Map_Q1_2026.xlsx \
  --pricelist hospital_prices_2026.xlsx \
  --output-prefix "2026_Q1" \
  --output-dir ./quarterly_updates
```

### Scenario 4: Quick Check (No Extras)
```bash
# Minimal output
python sbs_mapping_cli.py \
  --v2v3-file SBS_V2_to_V3_Map.xlsx \
  --pricelist prices.xlsx \
  --no-visualizations \
  --no-review-list \
  --quiet
```

---

## Getting Help

### Documentation Files
- `SBS_MAPPING_DOCUMENTATION.md` - Complete reference
- `sbs_mapping_notebook.ipynb` - Interactive examples
- This file - Quick start guide

### Support Checklist

Before asking for help:
1. ✓ Check error message carefully
2. ✓ Review this quick start guide
3. ✓ Check troubleshooting section in full documentation
4. ✓ Verify input files are not corrupted
5. ✓ Try with smaller dataset first

---

## Success Checklist

You're ready to go live when:
- ✅ Match rate > 80%
- ✅ High confidence rate > 60%
- ✅ Sample validation shows 95%+ accuracy
- ✅ Review list has been manually verified
- ✅ Test import successful
- ✅ Backup of original data created
- ✅ Team trained on process

---

## Tips for Best Results

1. **Start Small**: Test with 100-500 codes first
2. **Clean Your Data**: Remove duplicates, fix typos
3. **Be Consistent**: Use standard medical terminology
4. **Document Changes**: Keep log of manual corrections
5. **Iterate**: Re-run mapping as you improve descriptions
6. **Validate**: Always spot-check results
7. **Backup**: Keep copies of all files

---

## Time Estimates

| Activity | Estimated Time |
|----------|----------------|
| Initial setup | 30 minutes |
| First mapping run | 10-30 minutes |
| Review high confidence | 1-2 hours |
| Manual review process | 2-8 hours |
| System integration | 4-8 hours |
| **Total first time** | **1-2 days** |
| **Subsequent updates** | **2-4 hours** |

---

## You're Ready! 🚀

You now have everything you need to start mapping your SBS codes.

**Remember:**
- Start with the command-line example above
- Review the output files
- Iterate and improve
- Don't hesitate to adjust the threshold

**Good luck with your mapping!**

---

*For detailed information, see the complete documentation in `SBS_MAPPING_DOCUMENTATION.md`*
