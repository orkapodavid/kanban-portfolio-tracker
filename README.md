# Kanban Portfolio Tracker

A responsive, full-featured Kanban board application for tracking and managing a portfolio of financial instruments with drag-and-drop functionality, comprehensive audit trail, and automated testing.

## 🚀 Features

- **8-Stage Kanban Board**: Universe → Prospects → Outreach → Discovery → Live Deal → Execute → Tracker → Ocean
- **Drag-and-Drop Interface**: Intuitive card movement with validation and forced transition handling
- **Audit Trail**: Immutable StateTransitionLog with user comments and timestamps
- **CSV Export**: One-click export of current board state
- **Responsive Design**: Mobile-first with tab navigation and hamburger menu
- **Search & Filters**: Real-time filtering by ticker/company and stale status
- **Detail Modals**: View individual stock details and complete activity history
- **Ocean Archive**: Special view for archived deals

## 📦 Installation

bash
# Clone the repository
git clone https://github.com/orkapodavid/kanban-portfolio-tracker.git
cd kanban-portfolio-tracker

# Install dependencies
pip install -r requirements.txt

# Run the application
reflex run


## 🏗️ Architecture


app/
├── components/          # Reusable UI components
│   ├── header.py       # Application header with search and filters
│   ├── modals.py       # All modal dialogs
│   ├── stage_column.py # Droppable Kanban columns
│   └── stock_card.py   # Draggable stock cards
├── pages/              # Page layouts
│   └── dashboard.py    # Main Kanban board
├── states/             # State management
│   ├── base_state.py   # Base app configuration
│   └── kanban_state.py # Board-specific logic
├── models.py           # Data models (Stock, StateTransitionLog, StageDef)
└── app.py              # Application entry point


## 🧪 Testing

bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/


## 📱 Mobile Design

- Responsive hamburger menu for mobile navigation
- Tab-based column switching on small screens
- 44x44px minimum touch targets for accessibility
- Optimized layout for thumb-zone interaction

## 🔒 Security

- No hardcoded secrets or API keys
- Comprehensive `.gitignore` for sensitive files
- Environment variable support for configuration

## 📊 Audit Trail

Every stock movement is logged in `StateTransitionLog` with:
- Previous and new stage
- User comment (required)
- Timestamp (UTC)
- User identity
- Forced transition flag and rationale (if applicable)

## 🛠️ Development

bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest

# Export current board state
# Click "Export CSV" button in the application header


## 📝 License

MIT License - feel free to use this project for your own portfolio tracking needs.

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.
