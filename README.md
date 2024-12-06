# AI Plagiarism Detection

A robust tool that leverages the Originality.ai API to perform comprehensive document analysis, including plagiarism detection, AI content detection, readability metrics, and skill assessment.

## 🚀 Features

- Plagiarism Detection
- AI Content Detection
- Readability Analysis
- Grammar & Spelling Check
- Batch Processing Capability
- Detailed Results Storage

## 📋 How It Works

1. **Input**: Place your text in `input.txt` or modify the script to read from your desired source
2. **Processing**: The script connects to Originality.ai API and performs the requested analysis
3. **Output**: Results are stored in the `originality_results` directory in both formatted (.txt) and raw JSON formats

## 🛠️ Setup

1. Install required dependencies:

```bash
pip install requests
```

2. Configure your API key in `config.py`:

```python
ORIGINALITY_AI_API_KEY = "your_api_key_here"
```

## 📊 Project Milestones

| Phase | Milestone | Status | Timeline |
|-------|-----------|---------|----------|
| **Phase 1: API Integration** | | | |
| | Research Originality.ai API capabilities | ✅ | Week 1 |
| | Document API endpoints and functionality | ✅ | Week 1 |
| | Create comprehensive README documentation | ✅  | Week 1 |
| **Phase 2: Core Functionality** | | | |
| | Implement basic API connection | ✅ | Week 1 |
| | Develop JSON data extraction utilities | ✅ | Week 1 |
| | Add error handling and logging | ✅  | Week 1 |
| **Phase 3: Data Analysis** | | | |
| | Implement basic data visualization | ✅  | Week 1 |
| | Create statistical analysis functions | ✅  | Week 1 |
| | Generate automated reports |  🏗️ | Week 1 |
| **Phase 4: Frontend Development** | | | |
| | Create Streamlit app structure |  🏗️ | Week 2 |
| | Implement file upload and text adding functionality |  🏗️ | Week 2 |
| | Add visualization components of graphs and text distribution of plagiarism | 🏗️ | Week 2 |
| | Develop download functionality for analysis report | 📅 | Week 2 |
| | Create interactive dashboard | 📅 | Week 2 |

Legend: ✅ Complete | 🏗️ In Progress | 📅 Planned

## 💡 Script Functionality

The `script.py` file provides the following key functionalities:

1. **Text Analysis**:
   - Plagiarism detection
   - AI content detection
   - Readability metrics
   - Grammar and spelling check

2. **Input Methods**:
   - Direct text input via `input.txt`
   - URL scanning
   - Batch processing capability

3. **Output Storage**:
   - Results are saved in `originality_results` directory
   - Two formats per scan:
     - Formatted text file (.txt)
     - Raw JSON data (_raw.json)

## 📁 Results Storage

The results are stored in the `originality_results` directory with the following structure:

```
originality_results/
├── scan_result_YYYYMMDD_HHMMSS.txt    # Formatted results
└── scan_result_YYYYMMDD_HHMMSS_raw.json    # Raw JSON data
```

## 📝 Using the Script

1. **Prepare Input**:
   - Add your text to `input.txt`
   - Or modify script to read from URLs or batch process multiple files

2. **Run the Script**:
   ```bash
   python script.py
   ```

3. **Check Results**:
   - Navigate to `originality_results` directory
   - View formatted results in .txt file
   - Access raw data in _raw.json file
