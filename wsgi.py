from app import app, main, asyncio

if __name__ == '__main__':
    app.run(debug=True)
    asyncio.run(main())




