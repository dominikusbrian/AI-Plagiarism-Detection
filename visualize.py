import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
import numpy as np
import base64
from jinja2 import Template
import io
from streamlit.components.v1 import html
from script import OriginalityAI, initialize_client, format_results
import tempfile


class OriginalityVisualizer:
    def __init__(self, json_data: Dict):
        """Initialize visualizer with JSON data"""
        self.data = json_data
        
    def plot_ai_detection_results(self) -> go.Figure:
        """Create an interactive pie chart for AI detection results"""
        if not self.data.get('ai'):
            return None
            
        ai_data = self.data['ai']
        labels = ['AI Generated', 'Original']
        values = [
            ai_data['confidence'].get('AI', 0) * 100,
            ai_data['confidence'].get('Original', 0) * 100
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            marker_colors=['#FF9999', '#66B2FF']
        )])
        
        fig.update_layout(
            title="AI Detection Confidence Scores",
            annotations=[dict(text='AI Analysis', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        return fig
    
    def plot_readability_metrics(self) -> go.Figure:
        """Create a radar chart for readability metrics"""
        if not self.data.get('readability'):
            return None
            
        metrics = self.data['readability']['readability']
        
        categories = ['Flesch Reading Ease', 'Flesch-Kincaid Grade', 
                     'Gunning Fox Index', 'SMOG Index', 'Coleman-Liau']
        values = [
            metrics.get('fleschReadingEase', 0),
            metrics.get('fleschGradeLevel', 0),
            metrics.get('gunningFoxIndex', 0),
            metrics.get('smogIndex', 0),
            metrics.get('colemanLiauIndex', 0)
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Readability Scores'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) * 1.2]
                )),
            showlegend=False,
            title="Readability Metrics"
        )
        return fig
    
    def plot_text_statistics(self) -> go.Figure:
        """Create a bar chart for text statistics"""
        if not self.data.get('readability'):
            return None
            
        stats = self.data['readability']['textStats']
        
        metrics = {
            'Word Count': stats.get('uniqueWordCount', 0),
            'Sentence Count': stats.get('sentenceCount', 0),
            'Syllable Count': stats.get('syllableCount', 0),
            'Speaking Time (min)': stats.get('averageSpeakingTime', 0),
            'Reading Time (min)': stats.get('averageReadingTime', 0)
        }
        
        fig = go.Figure([go.Bar(
            x=list(metrics.keys()),
            y=list(metrics.values()),
            marker_color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
        )])
        
        fig.update_layout(
            title="Text Statistics",
            xaxis_title="Metric",
            yaxis_title="Value"
        )
        return fig
    
    def plot_sentence_complexity(self) -> go.Figure:
        """Create a visualization of sentence complexity"""
        analysis = self.analyze_sentence_complexity()
        if not analysis:
            return None
            
        labels = ['Simple', 'Hard', 'Very Hard']
        values = [
            analysis['total_sentences'] - analysis['hard_sentences'] - analysis['very_hard_sentences'],
            analysis['hard_sentences'],
            analysis['very_hard_sentences']
        ]
        
        fig = go.Figure([go.Bar(
            x=labels,
            y=values,
            marker_color=['#99FF99', '#FFCC99', '#FF9999']
        )])
        
        fig.update_layout(
            title="Sentence Complexity Distribution",
            xaxis_title="Complexity Level",
            yaxis_title="Number of Sentences"
        )
        return fig

    def analyze_sentence_complexity(self) -> Dict:
        """Analyze sentence complexity and return insights"""
        if not self.data.get('readability'):
            return {}
            
        sentences = self.data['readability'].get('sentences', [])
        
        analysis = {
            'total_sentences': len(sentences),
            'hard_sentences': sum(1 for s in sentences if s.get('isHard', False)),
            'very_hard_sentences': sum(1 for s in sentences if s.get('isVeryHard', False)),
            'sentences_with_long_words': sum(1 for s in sentences if s.get('wordsOver13Chars', [])),
            'sentences_with_complex_words': sum(1 for s in sentences if s.get('wordsOver4Syllables', []))
        }
        
        return analysis
    
    def analyze_ai_blocks(self) -> pd.DataFrame:
        """Analyze AI detection results for individual text blocks"""
        if not self.data.get('ai') or not self.data['ai'].get('blocks'):
            return pd.DataFrame()
        
        blocks = self.data['ai']['blocks']
        df = pd.DataFrame(blocks)
        df['ai_score'] = df['result'].apply(lambda x: x.get('fake', 0) * 100)
        df['human_score'] = df['result'].apply(lambda x: x.get('real', 0) * 100)
        return df[['text', 'ai_score', 'human_score']]

    def plot_plagiarism_metrics(self) -> go.Figure:
        """Create visualization for plagiarism metrics"""
        if not self.data.get('plagiarism'):
            return None
            
        plag_data = self.data['plagiarism']
        
        # Create metrics for plagiarism
        metrics = {
            'Overall Score': plag_data.get('score', 0),
        }
        
        # Add match scores if available
        if plag_data.get('matches'):
            for i, match in enumerate(plag_data['matches'], 1):
                metrics[f'Match {i}'] = match.get('score', 0)
        
        fig = go.Figure([go.Bar(
            x=list(metrics.keys()),
            y=list(metrics.values()),
            marker_color='#FF9999',
            text=[f'{v}%' for v in metrics.values()],
            textposition='auto',
        )])
        
        fig.update_layout(
            title="Plagiarism Analysis",
            xaxis_title="Source",
            yaxis_title="Match Percentage (%)",
            yaxis_range=[0, 100]
        )
        return fig

    def plot_readability_details(self) -> go.Figure:
        """Create detailed readability visualization"""
        if not self.data.get('readability'):
            return None
            
        read_data = self.data['readability']
        text_stats = read_data['textStats']
        
        # Create detailed metrics
        metrics = {
            'Unique Words': text_stats.get('uniqueWordCount', 0),
            'Total Syllables': text_stats.get('totalSyllables', 0),
            'Avg Syllables/Word': text_stats.get('averageSyllablesPerWord', 0),
            'Words with 3+ Syllables': text_stats.get('wordsWithThreeSyllables', 0),
            '% Complex Words': text_stats.get('percentWordsWithThreeSyllables', 0)
        }
        
        fig = go.Figure([go.Bar(
            x=list(metrics.keys()),
            y=list(metrics.values()),
            marker_color=['#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#FF9999'],
            text=[f'{v:.1f}' if isinstance(v, float) else v for v in metrics.values()],
            textposition='auto',
        )])
        
        fig.update_layout(
            title="Detailed Readability Metrics",
            xaxis_title="Metric",
            yaxis_title="Value"
        )
        return fig

    def plot_sentence_heatmap(self) -> go.Figure:
        """Create a heatmap of sentence complexity and AI probability"""
        if not self.data.get('ai') or not self.data['ai'].get('blocks'):
            return None
        
        blocks = self.data['ai']['blocks']
        df = pd.DataFrame(blocks)
        
        # Calculate metrics for each block
        df['length'] = df['text'].str.len()
        df['ai_prob'] = df['result'].apply(lambda x: x.get('fake', 0))
        
        # Create heatmap data
        heatmap_data = np.column_stack((
            df['length'].values,
            df['ai_prob'].values * 100
        ))
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.T,
            x=np.arange(len(df)),
            y=['Length', 'AI Probability'],
            colorscale='RdBu_r',
            showscale=True
        ))
        
        fig.update_layout(
            title="Sentence Analysis Heatmap",
            xaxis_title="Sentence Index",
            yaxis_title="Metrics"
        )
        return fig

    def plot_readability_timeline(self) -> go.Figure:
        """Create a timeline view of readability metrics across the text"""
        if not self.data.get('readability') or not self.data['readability'].get('sentences'):
            return None
        
        sentences = self.data['readability']['sentences']
        df = pd.DataFrame(sentences)
        
        # Calculate rolling averages
        window_size = 5
        metrics = {
            'Complexity': df['isHard'].astype(int) + df['isVeryHard'].astype(int),
            'Long Words': df['wordsOver13Chars'].str.len(),
            'Complex Words': df['wordsOver4Syllables'].str.len()
        }
        
        fig = go.Figure()
        
        for name, values in metrics.items():
            rolling_avg = values.rolling(window=window_size, min_periods=1).mean()
            fig.add_trace(go.Scatter(
                x=np.arange(len(rolling_avg)),
                y=rolling_avg,
                name=name,
                mode='lines+markers'
            ))
        
        fig.update_layout(
            title=f"Readability Timeline (Rolling Average: {window_size} sentences)",
            xaxis_title="Sentence Position",
            yaxis_title="Metric Value",
            showlegend=True
        )
        return fig

    def generate_detailed_insights(self) -> List[str]:
        """Generate detailed insights from all analyses"""
        insights = []
        
        # AI Detection Insights
        if self.data.get('ai'):
            ai_conf = self.data['ai']['confidence']
            ai_prob = ai_conf.get('AI', 0) * 100
            insights.append(f"🤖 AI Detection:")
            insights.append(f"  - Overall AI Probability: {ai_prob:.1f}%")
            
            blocks = self.data['ai'].get('blocks', [])
            if blocks:
                high_ai_blocks = sum(1 for b in blocks if b['result'].get('fake', 0) > 0.75)
                insights.append(f"  - {high_ai_blocks} text blocks show strong AI characteristics")
        
        # Readability Insights
        if self.data.get('readability'):
            metrics = self.data['readability']['readability']
            stats = self.data['readability']['textStats']
            
            insights.append("\n📚 Readability Analysis:")
            insights.append(f"  - Flesch Reading Ease: {metrics.get('fleschReadingEase', 0):.1f}")
            insights.append(f"  - Average Reading Time: {stats.get('averageReadingTime', 0):.1f} minutes")
            
            complexity = self.analyze_sentence_complexity()
            if complexity:
                total = complexity['total_sentences']
                hard = complexity['hard_sentences']
                very_hard = complexity['very_hard_sentences']
                if total > 0:
                    hard_percent = (hard + very_hard) / total * 100
                    insights.append(f"  - {hard_percent:.1f}% of sentences are complex")
        
        # Plagiarism Insights
        if self.data.get('plagiarism'):
            plag_data = self.data['plagiarism']
            insights.append("\n🔍 Plagiarism Check:")
            insights.append(f"  - Overall Score: {plag_data.get('score', 0)}%")
            
            if plag_data.get('matches'):
                insights.append(f"  - Found {len(plag_data['matches'])} potential matches")
        
        return insights

def export_to_html(figs: List[go.Figure], insights: List[str], data: Dict) -> str:
    """Convert dashboard to HTML with enhanced styling"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Originality.AI Analysis Report</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container { 
                max-width: 1200px;
                margin: auto;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .section { 
                margin: 30px 0;
                padding: 20px;
                border: 1px solid #eee;
                border-radius: 8px;
                background-color: white;
            }
            .section h2 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            .insights { 
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                font-family: monospace;
                white-space: pre-wrap;
            }
            .metric { 
                display: inline-block;
                margin: 10px;
                padding: 15px 25px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }
            .metric:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            .plot-container {
                margin: 20px 0;
                padding: 10px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #2c3e50; text-align: center;">Originality.AI Analysis Report</h1>
            
            <div class="section">
                <h2>Document Properties</h2>
                {% if properties %}
                    <div class="metric">Title: {{ properties.title }}</div>
                    <div class="metric">ID: {{ properties.id }}</div>
                    <div class="metric">Public Link: <a href="{{ properties.public_link }}" target="_blank">View</a></div>
                {% endif %}
            </div>
            
            <div class="section">
                <h2>Key Insights</h2>
                <div class="insights">
                    {% for insight in insights %}
                        {{ insight }}
                    {% endfor %}
                </div>
            </div>
            
            {% for plot in plots %}
                <div class="section">
                    <div class="plot-container">
                        {{ plot }}
                    </div>
                </div>
            {% endfor %}
            
            <div class="section">
                <h2>Credits Information</h2>
                {% if credits %}
                    <div class="metric">Used Credits: {{ credits.used }}</div>
                    <div class="metric">Base Credits: {{ credits.base_credits }}</div>
                    <div class="metric">Subscription Credits: {{ credits.subscription_credits }}</div>
                {% endif %}
            </div>
        </div>
        <script>
            // Add any interactive features here
            document.addEventListener('DOMContentLoaded', function() {
                // Make plots responsive
                window.onresize = function() {
                    Plotly.Plots.resize();
                };
            });
        </script>
    </body>
    </html>
    """
    
    # Convert figures to HTML
    plot_htmls = [fig.to_html(full_html=False, include_plotlyjs=False) for fig in figs if fig is not None]
    
    # Use the insights passed to the function instead of generating them here
    template = Template(html_template)
    html_content = template.render(
        plots=plot_htmls,
        insights=insights,  # Use the insights passed to the function
        properties=data.get('properties', {}),
        credits=data.get('credits', {})
    )
    
    return html_content

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate download link for binary file"""
    b64 = base64.b64encode(bin_file.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{file_label}.html">Download {file_label}</a>'

def process_text_input(text: str) -> Dict:
    """
    Process input text using OriginalityAI API and return results
    """
    try:
        # Initialize the API client
        client = initialize_client()
        
        # Perform the scan
        result = client.new_scan(text)
        
        # Save results to temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as formatted_file:
            formatted_file.write(format_results(result))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as raw_file:
            json.dump(result, raw_file, indent=2, ensure_ascii=False)
            
        return result
        
    except Exception as e:
        raise Exception(f"Error processing text: {str(e)}")

def main():
    st.set_page_config(page_title="Originality.AI Analysis", layout="wide")
    st.title("Originality.AI Analysis Dashboard")
    
    # Add tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["Upload JSON", "Upload Text File", "Enter Text"])
    
    with tab1:
        # Existing JSON upload functionality
        uploaded_file = st.file_uploader("Upload JSON result file", type=['json'], key="json_uploader")
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                display_analysis(data)
            except Exception as e:
                st.error(f"Error analyzing JSON file: {str(e)}")
    
    with tab2:
        # Text file upload functionality
        text_file = st.file_uploader("Upload text file", type=['txt'], key="text_uploader")
        if text_file is not None:
            try:
                text_content = text_file.getvalue().decode()
                with st.spinner('Processing text...'):
                    result = process_text_input(text_content)
                display_analysis(result)
            except Exception as e:
                st.error(f"Error processing text file: {str(e)}")
    
    with tab3:
        # Direct text input functionality
        text_input = st.text_area("Enter text to analyze", height=200)
        if st.button("Analyze Text"):
            if text_input.strip():
                try:
                    with st.spinner('Processing text...'):
                        result = process_text_input(text_input)
                    display_analysis(result)
                except Exception as e:
                    st.error(f"Error processing text: {str(e)}")
            else:
                st.warning("Please enter some text to analyze")

def display_analysis(data: Dict):
    """Display analysis results using the OriginalityVisualizer"""
    visualizer = OriginalityVisualizer(data)
    
    # Display document properties
    st.header("Document Properties")
    if 'properties' in data:
        props = data['properties']
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Title: {props.get('title', 'N/A')}")
            st.write(f"ID: {props.get('id', 'N/A')}")
        with col2:
            st.write(f"Public Link: {props.get('public_link', 'N/A')}")
            st.write(f"Private ID: {props.get('privateID', 'N/A')}")
    
    # AI Detection Results
    st.header("AI Detection Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        ai_fig = visualizer.plot_ai_detection_results()
        if ai_fig:
            st.plotly_chart(ai_fig, use_container_width=True)
    
    with col2:
        if data.get('ai'):
            ai_conf = data['ai']['confidence']
            ai_prob = ai_conf.get('AI', 0) * 100
            st.metric("AI Probability", f"{ai_prob:.1f}%")
            
            # Add risk level indicator
            if ai_prob > 75:
                st.error("⚠️ High Risk of AI Generation")
            elif ai_prob > 50:
                st.warning("⚡ Moderate Risk of AI Generation")
            else:
                st.success("✅ Low Risk of AI Generation")
    
    # Readability Analysis
    st.header("Readability Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        read_fig = visualizer.plot_readability_metrics()
        if read_fig:
            st.plotly_chart(read_fig, use_container_width=True)
    
    with col2:
        text_fig = visualizer.plot_text_statistics()
        if text_fig:
            st.plotly_chart(text_fig, use_container_width=True)
    
    # Sentence Complexity
    st.header("Sentence Complexity")
    comp_fig = visualizer.plot_sentence_complexity()
    if comp_fig:
        st.plotly_chart(comp_fig, use_container_width=True)
    
    # AI Block Analysis
    st.header("Detailed AI Detection by Text Block")
    df = visualizer.analyze_ai_blocks()
    if not df.empty:
        # Add color highlighting based on AI score
        def highlight_ai_score(val):
            if val > 75:
                return 'background-color: #ffcccc'
            elif val > 50:
                return 'background-color: #ffffcc'
            return ''
        
        # Use .map instead of .applymap
        styled_df = df.style.map(highlight_ai_score, subset=['ai_score'])
        st.dataframe(styled_df, use_container_width=True)
    
    # Add Plagiarism Analysis
    st.header("Plagiarism Analysis")
    plag_fig = visualizer.plot_plagiarism_metrics()
    if plag_fig:
        st.plotly_chart(plag_fig, use_container_width=True)
        
        # Display plagiarism matches if available
        if data.get('plagiarism', {}).get('matches'):
            st.subheader("Plagiarism Matches")
            matches_df = pd.DataFrame(data['plagiarism']['matches'])
            st.dataframe(matches_df, use_container_width=True)
    
    # Add Detailed Readability Analysis
    st.header("Detailed Readability Analysis")
    read_detail_fig = visualizer.plot_readability_details()
    if read_detail_fig:
        st.plotly_chart(read_detail_fig, use_container_width=True)
    
    # Add new visualizations
    st.header("Text Analysis Timeline")
    timeline_fig = visualizer.plot_readability_timeline()
    if timeline_fig:
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    st.header("Sentence Complexity Heatmap")
    heatmap_fig = visualizer.plot_sentence_heatmap()
    if heatmap_fig:
        st.plotly_chart(heatmap_fig, use_container_width=True)
    
    # Update export functionality to include new visualizations
    if st.button("Generate HTML Report"):
        visualizer = OriginalityVisualizer(data)  # Make sure visualizer is defined
        figures = [
            visualizer.plot_ai_detection_results(),
            visualizer.plot_readability_metrics(),
            visualizer.plot_text_statistics(),
            visualizer.plot_sentence_complexity(),
            visualizer.plot_plagiarism_metrics(),
            visualizer.plot_readability_details(),
            visualizer.plot_readability_timeline(),
            visualizer.plot_sentence_heatmap()
        ]
        
        # Get insights from the visualizer
        insights = visualizer.generate_detailed_insights()
        
        # Generate HTML with detailed insights
        html_content = export_to_html(figures, insights, data)
        
        # Create download link
        html_download = get_binary_file_downloader_html(html_content, "analysis_report")
        st.markdown(html_download, unsafe_allow_html=True)
    
    # Raw JSON Viewer
    if st.checkbox("Show Raw JSON"):
        st.json(data)

if __name__ == "__main__":
    main()
