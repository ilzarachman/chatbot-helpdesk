# Set the environment variable for development or production
export ENVIRONMENT=${ENVIRONMENT:-"development"}

# Run the Python script based on the environment
if [ "$ENVIRONMENT" == "development" ]; then
    python chatbot/main.py
elif [ "$ENVIRONMENT" == "production" ]; then
    # Production-specific startup script here
    echo "Starting chatbot in production mode..."
else
    echo "Invalid environment specified. Please set ENVIRONMENT to either 'development' or 'production'."
fi
