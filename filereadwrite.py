def createuseragefile(filename, user_ages):
    """Creates a file with user names and their ages.

    Args:
        filename (str): The name of the file to create.
        user_ages (dict): A dictionary with user names as keys and ages as values.
    """
    with open(filename, 'w') as file:
        for user, age in user_ages.items():
            file.write(f"{user},{age}\n")

def readuseragefile(filename):
    """Reads a file with user names and their ages.

    Args:
        filename (str): The name of the file to read.

    Returns:
        dict: A dictionary with user names as keys and ages as values.
    """
    user_ages = {}
    with open(filename, 'r') as file:
        for line in file:
            user, age = line.strip().split(',')
            user_ages[user] = int(age)
    return user_ages

def updateuseragefile(filename, user, new_age):
    """Updates the age of a user in the file.

    Args:
        filename (str): The name of the file to update.
        user (str): The name of the user whose age is to be updated.
        new_age (int): The new age of the user.
    """
    user_ages = readuseragefile(filename)
    user_ages[user] = new_age
    createuseragefile(filename, user_ages)  

def appenduseragefile(filename, user, age):
    """Appends a new user and their age to the file.

    Args:
        filename (str): The name of the file to append to.
        user (str): The name of the user to add.
        age (int): The age of the user to add.
    """
    with open(filename, 'a') as file:
        file.write(f"{user},{age}\n")

def main():
    # Example usage
    filename = 'user_ages.txt'
    user_ages = {'Alice': 30, 'Bob': 25, 'Charlie': 35}
    createuseragefile(filename, user_ages)
    print("Initial user ages:", readuseragefile(filename))
    updateuseragefile(filename, 'Bob', 26)
    print("After updating Bob's age:", readuseragefile(filename))
    appenduseragefile(filename, 'Diana', 28)
    print("After appending Diana:", readuseragefile(filename))
    

if __name__ == "__main__":
    main()  