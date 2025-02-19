# Chinese Listening Comprehension Practice

This project provides a platform for practicing listening comprehension, particularly for learners of Chinese. It includes a frontend application built with Streamlit and a backend that generates audio and questions using AWS services.

## Features

- **Audio Generation:** Uses AWS Polly and Bedrock to generate audio in Mandarin.
- **Question Generation:** Automatically generates practice questions.
- **Interactive UI:** Streamlit-based interface for practicing listening comprehension.

## Requirements

- Python 3.8+
- AWS credentials configured for accessing Polly and Bedrock services.

## Setup

1. **Clone the repository:**

   ```sh
   git clone <repository-url>
   cd listening-comp-main
   ```

2. **Install Backend Dependencies:**

   ```sh
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Install Frontend Dependencies:**  
   Ensure Streamlit is installed:

   ```sh
   pip install streamlit
   ```

## Running the Application

### Frontend

To start the frontend application, run:

```sh
streamlit run frontend/main.py
```

### Backend

To run backend services, use:

```sh
python backend/main.py
```

## Usage

- Access the Streamlit app through your browser to interact with the listening practice interface.
- Use the backend scripts to generate audio and questions as needed.

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License.