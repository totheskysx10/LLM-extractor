import uvicorn


def main():
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        workers=1
    )


if __name__ == "__main__":
    main()