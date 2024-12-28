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
| | Create comprehensive README documentation | 🏗️ | Week 1 |
| **Phase 2: Core Functionality** | | | |
| | Implement basic API connection | ✅ | Week 2 |
| | Develop JSON data extraction utilities | ✅ | Week 2 |
| | Add error handling and logging | 🏗️ | Week 2 |
| **Phase 3: Data Analysis** | | | |
| | Implement basic data visualization | 📅 | Week 3 |
| | Create statistical analysis functions | 📅 | Week 3 |
| | Generate automated reports | 📅 | Week 3 |
| **Phase 4: Frontend Development** | | | |
| | Create Streamlit app structure | 📅 | Week 4 |
| | Implement file upload functionality | 📅 | Week 4 |
| | Add visualization components | 📅 | Week 5 |
| | Develop download functionality | 📅 | Week 5 |
| | Create interactive dashboard | 📅 | Week 6 |

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

## 📊 Streamlit Visualization Dashboard

The project includes a comprehensive visualization dashboard (`visualize.py`) that provides an interactive way to analyze and visualize the results from Originality.ai.

### Dashboard Features

1. **Multiple Input Methods**:
   - Upload JSON result files
   - Upload text files for direct analysis
   - Enter text directly for real-time analysis

2. **Interactive Visualizations**:
   - AI Detection confidence pie chart
   - Readability metrics radar chart
   - Text statistics bar charts
   - Sentence complexity distribution
   - Plagiarism analysis charts
   - Readability timeline
   - Sentence complexity heatmap

3. **Detailed Analysis Sections**:
   - Document properties overview
   - AI detection analysis with risk levels
   - Readability metrics and text statistics
   - Sentence complexity analysis
   - AI detection by text block
   - Plagiarism detection results
   - Detailed readability insights

4. **Export Capabilities**:
   - Generate interactive HTML reports
   - Download complete analysis results
   - Export visualizations

### Running the Dashboard

1. Install required dependencies:
```bash
pip install streamlit pandas matplotlib seaborn plotly
```

2. Launch the dashboard:
```bash
streamlit run visualize.py
```

3. Access the dashboard in your browser at `http://localhost:8501`

### Dashboard Workflow

1. **Input**: Choose your preferred input method:
   - Upload a JSON file containing previous analysis results
   - Upload a text file for new analysis
   - Enter text directly into the interface

2. **Analysis**: The dashboard will automatically process the input and generate:
   - Interactive visualizations
   - Detailed metrics
   - Risk assessments
   - Statistical analysis
