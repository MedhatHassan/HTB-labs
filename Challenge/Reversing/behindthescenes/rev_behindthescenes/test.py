def saveToFile(data):
    try:
        with open('elfOutput', 'w') as file:
            file.write(data)
        print(f"Data saved to {'elfOutput'} successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")