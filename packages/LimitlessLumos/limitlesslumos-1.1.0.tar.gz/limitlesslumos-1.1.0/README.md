# LimitlessLumos

**LimitlessLumos** is a powerful Python package designed to ensure that your Telegram bots or other long-running scripts stay alive indefinitely. By integrating a lightweight Flask web server, **LimitlessLumos** guarantees that your scripts remain active and free from timeouts.

## Features

- **Persistent Uptime**: Keeps your script or bot running indefinitely by utilizing a Flask-based server to prevent timeouts.
- **Flexible Configuration**: Easily customize the server's host and port settings according to your needs.
- **Concurrent Execution**: The Flask server runs in a separate thread, allowing your main script to execute without interruptions.
- **Effortless Integration**: Seamlessly integrates into existing Python scripts or Telegram bots with minimal code changes.

## Installation

To install **LimitlessLumos**, ensure you have Python 3.6 or higher, then install it via pip:

```bash
pip install LimitlessLumos
```

## Usage

Here’s how to use **LimitlessLumos** to ensure your script or bot runs indefinitely, with different configurations available for your convenience:

### Basic Example: Default Flask Server

1. **Create Your Script** (e.g., `my_bot.py`):

    ```python
    from LimitlessLumos import lumosServer
    from my_telegram_bot import start_bot  # Replace with your bot’s start function

    # Start your bot or main script
    start_bot()

    # Run the default Flask server to keep the script alive
    lumosServer()
    ```

    This will run the Flask server with the default settings (`localhost` on port `5000`).

2. **Run Your Script**:

    ```bash
    python my_bot.py
    ```

### Advanced Usage: Customizing the Flask Server

- **Run on All Interfaces with an Auto-Assigned Port**:

    ```python
    lumosServer("All")
    ```

    This command configures the Flask server to listen on `0.0.0.0` (all available interfaces) with an auto-assigned port, allowing access from any IP address.

- **Specify Host and Port Manually**:

    ```python
    lumosServer(host="0.0.0.0", port="8080")
    ```

    This configuration allows you to define both the host and port manually. For example, setting `host="0.0.0.0"` and `port="8080"` makes the server accessible on all network interfaces at port `8080`.

### Example Script with Custom Configuration:

```python
from LimitlessLumos import lumosServer
from my_telegram_bot import start_bot

# Start your bot or main script
start_bot()

# Example: Custom host and port configuration
lumosServer(host="0.0.0.0", port="8080")
```

## Configuration

**LimitlessLumos** provides flexible configuration options for the underlying Flask server. By adjusting the `lumosServer` parameters, you can control how and where your server runs:

- **Default Settings**: `lumosServer()` starts a Flask server on `localhost` at port `5000`.
- **All Interfaces**: `lumosServer("All")` makes the server accessible from any IP address, with an automatically assigned port.
- **Custom Host and Port**: `lumosServer(host="", port="")` allows you to specify the host and port according to your needs.

## Contributing

Contributions to **LimitlessLumos** are highly encouraged! Whether you have suggestions, bug fixes, or new features, your input is valuable. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Submit a Pull Request for review.

## License

**LimitlessLumos** is distributed under the [CC-BY-SA 4.0](https://github.com/TraxDinosaur/LimitlessLumos/blob/main/LICENSE) license. You are free to share and adapt the software as long as appropriate credit is given and any derivatives are licensed under the same terms.

## Support

For questions, issues, or support, feel free to reach out to [TraxDinosaur](https://traxdinosaur.github.io). We are here to assist with any challenges you may encounter while using **LimitlessLumos**.

---

By using **LimitlessLumos**, you can confidently keep your scripts and bots running indefinitely, ensuring maximum uptime and reliability.
