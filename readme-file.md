# OpenHoldem Profile Generator

A powerful GUI application that allows poker players to generate customized OpenHoldem poker profiles with fine-grained control over strategy parameters at every stage of the game.

![OpenHoldem Profile Generator](https://example.com/images/openpg-screenshot.png) *(Screenshot example)*

## Overview

OpenHoldem Profile Generator is a Python application designed to streamline the creation of complex poker bot profiles for the OpenHoldem platform. It provides an intuitive interface for configuring detailed poker strategies across all game stages:

- **Preflop**: Configure opening ranges by position, 3-bet and 4-bet strategies, and squeeze plays
- **Flop**: Set c-bet frequencies, board texture adaptations, and facing bet responses
- **Turn**: Define second barrel strategies, scare card adjustments, and floating ranges
- **River**: Customize value betting, bluffing frequencies, and showdown decision-making
- **Push/Fold**: Create detailed push/fold ranges for tournament play by stack depth

The generator creates optimized OpenHoldem (.ohf) format profiles that can be directly loaded into the OpenHoldem poker platform.

## Features

- **Comprehensive Strategy Controls**: Adjust hundreds of poker strategy parameters through an intuitive UI
- **Predefined Player Profiles**: Choose from multiple pre-configured playing styles (TAG, LAG, Nit, Fish, etc.)
- **Game Type Customization**: Optimize for cash games, tournaments, SNGs, or MTTs
- **Stack-Dependent Adjustments**: Apply automatic adaptations based on stack sizes
- **Position-Based Settings**: Fine-tune your ranges and sizings based on table position
- **Board Texture Adaptations**: Customize how the bot responds to different board textures
- **Real-time Profile Preview**: See the generated OpenHoldem code as you adjust parameters
- **Save and Load Profiles**: Store your custom profiles for future reference or modification

## Installation

### Prerequisites

- Python 3.9+
- PyQt6

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/OpenHoldem-Profile-Generator.git
   cd OpenHoldem-Profile-Generator
   ```

2. Install the required packages:
   ```
   pip install PyQt6
   ```

3. Run the application:
   ```
   python main.py
   ```

## Usage

### Basic Workflow

1. **Select a Base Profile**: Choose a predefined player style from the dropdown or start from scratch
2. **Customize Settings**: Navigate through the tabs to adjust parameters for each game phase
3. **Generate Profile**: Click "Generate Profile" to create your OpenHoldem code
4. **Save Profile**: Save the generated profile as an .ohf file for use with OpenHoldem

### Tab Descriptions

#### Configuration Tab
- General application settings and profile preview

#### Preflop Settings
- **Open Raise**: Configure opening ranges and sizing by position
- **3-Bet Defense**: Set up 3-bet, 4-bet, and 5-bet strategies
- **Squeeze**: Define squeeze play frequencies and adjustments

#### Flop Settings
- **C-Bet Settings**: Adjust c-bet frequencies and sizes
- **Board Texture Adjustments**: Modify strategy based on wet/dry boards
- **Facing Bets**: Configure responses to opponent bets
- **Hand Ranges**: Define value betting and semi-bluffing ranges

#### Turn Settings
- **Second Barrel**: Set continuation betting frequencies
- **Turn Card Adjustments**: Adapt to scare cards and completed draws
- **Facing Turn Bets**: Configure defensive strategies

#### River Settings
- **Third Barrel**: Adjust value betting and bluffing frequencies
- **River Ranges**: Define showdown value thresholds
- **River Responses**: Configure check-raise frequencies and defensive strategies

#### Push/Fold Tab
- Configure short stack strategies for tournament play with stack-specific ranges

## Customizing Profiles

### Player Style Profiles

The generator includes several predefined player profiles:

- **TAG (Tight-Aggressive)**: Solid play with tight preflop ranges and aggressive postflop
- **LAG (Loose-Aggressive)**: Wider ranges with high aggression throughout the hand
- **Nit**: Ultra-conservative play focusing primarily on premium hands
- **Fish**: Loose-passive style mimicking recreational players
- **Loose-Passive**: Wide ranges with passive postflop tendencies

### Game Type Profiles

- **Cash Game**: Optimized for deep stack cash game play
- **Tournament**: Balanced approach for general tournament play
- **SNG**: Specialized for Sit & Go tournament formats
- **MTT**: Strategies for multi-table tournament play

### Stack Size Adjustments

Apply additional adjustments based on effective stack size:
- **Big Stack (>50BB)**: More speculative plays and aggressive 3-betting
- **Medium Stack (25-50BB)**: Balanced approach
- **Small Stack (10-25BB)**: More conservative with selective aggression
- **Short Stack (<10BB)**: Push/fold oriented strategy

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenHoldem community for documentation and profile structure references
- PyQt for providing the UI framework
- All contributors who have invested time in improving this generator

## Disclaimer

This software is designed for educational purposes and for use in jurisdictions where automated poker play is legal. Please ensure you comply with the terms of service of any poker site and all applicable laws in your jurisdiction.
