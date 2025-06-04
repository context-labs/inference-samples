<img src="logo.png" alt="Inference.net Logo" width="200">

# Inference.net API Examples

Welcome to the Inference.net API examples repository! This collection provides code samples and guides for common tasks using the Inference.net API.

## Getting Started

To run these examples, you'll need:

1. An Inference.net account - [Create a free account here](https://inference.net/signin)
2. An API key from your account dashboard

### Setting Up Your API Key

You can set up your API key in one of two ways:

1. **Environment Variable**:
   ```bash
   export INFERENCE_API_KEY=your_api_key_here
   ```

2. **.env File** (recommended for development):
   Create a `.env` file in your project root:
   ```bash
   INFERENCE_API_KEY=your_api_key_here
   ```
   Most IDEs (like VS Code) will automatically load this file.

## Available Resources

Most examples are written in Python, but the concepts can be applied to any language.

### Featured Examples

- [Webhook Example](webhook-example/README.md) - A minimalistic API that uses inference.net to detect Magnus Carlsen in images using webhooks
- [Batch Processing](https://docs.inference.net/batch-api) - Process multiple asynchronous requests in a single API call
- [Function Calling](https://docs.inference.net/function-calling) - Use structured outputs with your models
- [Vision](https://docs.inference.net/vision) - Process images with AI models
- [Background Inference](https://docs.inference.net/background-inference) - Use the asynchronous API for cost-effective processing

## License

MIT License