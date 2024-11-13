from framework.runtime.application import Application
from framework.runtime.drive.application_impl import ApplicationImpl


def main():
    Application.launch(ApplicationImpl())


if __name__ == "__main__":
    main()
