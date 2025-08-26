# ATA Thyroid Guidelines Comparison Website

## Project Overview
This project creates an interactive website for the 2025 American Thyroid Association (ATA) guidelines on thyroid nodules and differentiated thyroid cancer, with comprehensive comparison features against the 2015 guidelines.

## Purpose
- Provide healthcare professionals with easy access to the latest 2025 ATA thyroid guidelines
- Highlight key changes and updates from the 2015 version
- Offer interactive tools for quick reference and comparison
- Support clinical decision-making with up-to-date recommendations

## Technical Setup

### Prerequisites
- Python 3.8+ (for PDF processing)
- markitdown with PDF support: `pip install markitdown[pdf]`
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation
```bash
# Install PDF processing dependencies
pip install markitdown[pdf] pdfplumber pymupdf

# Clone or download the project
git clone https://github.com/zinojeng/ATA-update.git
cd ATA-update

# Open the website
open index.html  # macOS
# or
start index.html  # Windows
# or
xdg-open index.html  # Linux
```

## Content Structure

### PDF Processing
The content is extracted from two source documents:
- `2025 ATA thyroid nodule and cancer.pdf` (4.3MB)
- `2015 ATA thyroid nodule and cancer.pdf` (1.6MB)

### Key Sections Extracted
1. **Executive Summary**
   - Major recommendations
   - Strength of recommendations
   - Quality of evidence

2. **Thyroid Nodule Evaluation**
   - Clinical evaluation
   - Ultrasound assessment (TI-RADS)
   - Laboratory testing
   - FNA biopsy indications

3. **Cytopathology (Bethesda System)**
   - Category definitions
   - Management recommendations
   - Risk of malignancy updates

4. **Molecular Testing**
   - Available tests
   - Clinical utility
   - Integration with cytology

5. **Initial Management**
   - Surgical approaches
   - Extent of surgery
   - Active surveillance criteria

6. **Risk Stratification**
   - ATA risk categories
   - TNM staging updates
   - Dynamic risk assessment

7. **Radioactive Iodine Therapy**
   - Indications
   - Dosing recommendations
   - Preparation protocols

8. **Follow-up & Surveillance**
   - Monitoring protocols
   - Imaging recommendations
   - Biomarker interpretation

## Website Features

### 1. Interactive Comparison Tool
- **Side-by-side View**: Display 2015 and 2025 guidelines simultaneously
- **Highlight Changes**: Color-coded system
  - 🟢 Green: New additions in 2025
  - 🟡 Yellow: Modified recommendations
  - 🔴 Red: Removed or deprecated content
  - ⚪ Gray: Unchanged content

### 2. Search Functionality
- Full-text search across both guidelines
- Filter by section or topic
- Quick jump to relevant sections
- Search history for frequently accessed topics

### 3. Navigation System
- Collapsible table of contents
- Breadcrumb navigation
- Section bookmarks
- Quick access toolbar

### 4. Comparison Modes
- **Overview Mode**: High-level summary of changes
- **Detailed Mode**: Line-by-line comparison
- **Change-only Mode**: Show only modified content
- **Version Toggle**: Switch between 2015/2025 views

### 5. Export Options
- Download comparison reports (PDF)
- Print-friendly version
- Share specific sections via URL
- Copy formatted citations

## Key Updates in 2025 Guidelines

### Major Changes
1. **Updated TI-RADS Classification**
   - Refined scoring system
   - New size thresholds for FNA

2. **Molecular Testing Integration**
   - Expanded role in clinical decision-making
   - New test interpretations

3. **Active Surveillance**
   - Broadened eligibility criteria
   - Standardized monitoring protocols

4. **Risk Stratification Refinements**
   - Modified ATA risk categories
   - Enhanced dynamic risk assessment

5. **Treatment De-escalation**
   - Less aggressive surgical approaches
   - Reduced radioiodine use

## File Structure
```
ATA-update/
├── CLAUDE.md                 # This documentation file
├── README.md                 # User guide
├── index.html               # Main website
├── styles.css               # Custom styling
├── app.js                   # Main JavaScript
├── comparison.js            # Comparison logic
├── guidelines-data.json     # Structured content
├── 2025 ATA thyroid nodule and cancer.pdf
└── 2015 ATA thyroid nodule and cancer.pdf
```

## Development Notes

### PDF Processing Workflow
1. Use markitdown to convert PDFs to markdown
2. Parse markdown to extract structured sections
3. Generate JSON data for web consumption
4. Create comparison mappings between versions

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Performance Optimization
- Lazy loading for PDF content
- Indexed search for quick lookups
- Cached comparison results
- Compressed data format

## Maintenance

### Updating Content
1. Process new PDF versions with markitdown
2. Run comparison script to identify changes
3. Update guidelines-data.json
4. Test all interactive features

### Adding Features
- Modify app.js for new functionality
- Update styles.css for visual changes
- Extend comparison.js for analysis features

## Clinical Disclaimer
This website is for educational and reference purposes. Always refer to the official ATA publications for clinical decision-making. The comparison tool highlights differences but may not capture all nuances. Healthcare providers should use clinical judgment and consult the full guidelines.

## Support & Feedback
For questions or issues:
- GitHub Issues: https://github.com/zinojeng/ATA-update/issues
- Email: [contact information]

## Version History
- v1.0.0 (2025-01): Initial release with 2025 vs 2015 comparison
- Future: Integration with clinical calculators and risk assessment tools

## License
Educational use only. ATA guidelines are copyright of the American Thyroid Association.

---
Last Updated: January 2025