import traceback

def handle_error(error):
    return {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "trace": traceback.format_exc()
    }
