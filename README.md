# Chatbot Helpdesk System with FastAPI Backend

## Project Name

This project is a chatbot designed to provide helpdesk support. It is built using FastAPI backend and aims to [briefly describe the chatbot's purpose, e.g., automate common inquiries, provide self-service support, etc.].

## Features

- **[Feature 1]:** [Brief description of the feature]
- **[Feature
 2]:** [Brief description of the feature]
- **[Feature 3]:** [Brief description of the feature]

## Installation

1. **Prerequisites:**
   - Python 3.10
   - [Poetry](https://python-poetry.org/docs/#installation)
   - OpenAI API Key (You can get it from https://platform.openai.com/account/api-keys)
   - Gemini API Key (You can get it from https://aistudio.google.com/app/apikey)

2. **Steps:**
   - Clone the repository: 
     ```shell
     git clone https://github.com/ilzarachman/chatbot-helpdesk.git
     ```
   - Navigate to the project directory: `cd chatbot-helpdesk`
   - Create a Poetry virtual environment: `poetry install`
   - Run the server:
      - There are two ways to run the server, either you can set the environment variables manually using `export` or you can use third party tools like [Infisical](https://infisical.com/).
      - Then you can run the server using 
     ```shell
     poetry run python chatbot/main.py
     ```
      - If you are using Infisical, you can run it using `infisical run -- poetry run python chatbot/main.py`
     ```shell
     infisical run -- poetry run python chatbot/main.py
     ```

3. **Testing:**
   
    Run the tests using `pytest` or you can run 
    ```shell
    poetry run python test.py unit
    ```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository.**
2. **Create a new branch for your feature or bug fix.**
3. **Make your changes and commit them with descriptive commit messages.**
4. **Push your changes to your fork.**
5. **Submit a pull request.**

## Development Logs
- [x] Implementasi OOP dengan FastAPI Backend untuk mempermudah proses development.
- [x] Unit testing dan integration testing.
- [x] Database management.
- [x] Frontend development.
  - [x] Implementasi UI.
- [ ] Implementasi Sistem Admin staff untuk mengelola data document.
- [ ] Deployment.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing Guidelines

- **Commit Messages:** Use clear and concise commit messages that follow the [Conventional Commits](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13) specification.
- **Code Style:** Adhere to the project's code style guidelines.
- **Testing:** Write tests for any new features or bug fixes.

## Contact

For any questions or feedback, please contact [your email address or other contact information].
