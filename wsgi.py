from app import app, main, asyncio

if __name__ == '__main__':
    asyncio.run(main())
    app.run(debug=True, port=5000)
    




