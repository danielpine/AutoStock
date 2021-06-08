from tinyWinToast import tinyWinToast


def show(title, message):
    config = tinyWinToast.Config()
    config.APP_ID = "Auto Stock"
    toast = tinyWinToast.Toast(config)
    toast.setTitle(title, maxLines=2)
    toast.setMessage(message, maxLines=2)
    toast.show()
