# GeneXium - AI-Powered Personalized Training Plans

GeneXium is a web application that generates personalized training plans based on genetic analysis and user fitness goals. The application uses AI to analyze genetic data and create comprehensive training programs tailored to individual genetic profiles.

## Features

- **Gene Selection**: Choose from available genes (ACTN3, PPARGC1A) for analysis
- **Goal Input**: Enter detailed fitness goals and requirements
- **AI-Powered Analysis**: Leverages OpenAI's GPT models to analyze genetic data and create training plans
- **Markdown Rendering**: Beautifully formatted training plans with proper markdown support
- **Download Functionality**: Export training plans as markdown files
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Feedback**: Interactive gene information and loading states

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection for API calls

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd genexium_poc
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Ensure gene documentation is available**:
   Make sure you have the required gene documentation files in the `docs/` directory:
   ```
   docs/
   ├── actn3/
   │   └── (gene documentation files)
   └── ppargc1a/
       └── (gene documentation files)
   ```

## Usage

1. **Start the Flask application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Generate a training plan**:
   - Select a gene from the dropdown menu
   - Enter your fitness goal in the text area
   - Click "Generate Training Plan"
   - Wait for the AI to analyze your genetics and create a personalized plan
   - View the formatted training plan
   - Optionally download the plan as a markdown file

## Project Structure

```
genexium_poc/
├── app.py                 # Flask web application
├── main.py               # Original command-line interface
├── research_agent.py     # Core AI research and plan generation logic
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/
│   └── index.html       # Main web interface template
├── static/
│   ├── css/
│   │   └── style.css    # Custom styling
│   └── js/
│       └── app.js       # Frontend JavaScript logic
├── prompts/
│   ├── build_training_plan.txt
│   └── process_study.txt
└── docs/
    ├── actn3/           # ACTN3 gene documentation
    └── ppargc1a/        # PPARGC1A gene documentation
```

## API Endpoints

- `GET /`: Main application interface
- `POST /generate_plan`: Generate training plan endpoint
  - Request body: `{"gene": "gene_name", "goal": "fitness_goal"}`
  - Response: `{"success": true, "training_plan": "markdown_content", "gene": "gene_name", "goal": "fitness_goal"}`

## Supported Genes

### ACTN3 (Alpha-actinin-3)
- **Role**: Muscle function, particularly fast-twitch muscle fibers
- **Training Focus**: Power training, sprint performance, strength training
- **Best For**: Explosive movements, high-intensity workouts

### PPARGC1A (PGC-1α)
- **Role**: Mitochondrial biogenesis and energy metabolism
- **Training Focus**: Endurance training, aerobic capacity
- **Best For**: Long-distance activities, recovery optimization

## Technical Details

- **Backend**: Flask web framework
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Markdown Rendering**: Marked.js library
- **Styling**: Bootstrap 5 with custom CSS
- **AI Integration**: OpenAI GPT models via OpenAI API
- **Data Processing**: BeautifulSoup for web scraping

## Development

To run the application in development mode:

```bash
export FLASK_ENV=development
python app.py
```

The application will run on `http://localhost:5000` with debug mode enabled.

## Troubleshooting

1. **OpenAI API Key Issues**:
   - Ensure your API key is correctly set in the `.env` file
   - Verify you have sufficient API credits
   - Check that the API key has the necessary permissions

2. **Gene Documentation Missing**:
   - Ensure the `docs/` directory contains the required gene folders
   - Verify that the gene names in `app.py` match your directory structure

3. **Port Already in Use**:
   - Change the port in `app.py` or kill the process using the current port
   - Default port is 5000

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue in the repository or contact the development team. 