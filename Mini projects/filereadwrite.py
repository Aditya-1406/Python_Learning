def createuseragefile(filename, user_ages):
   
    with open(filename, 'w') as file:
        for user, age in user_ages.items():
            file.write(f"{user},{age}\n")

def readuseragefile(filename):
   
    user_ages = {}
    with open(filename, 'r') as file:
        for line in file:
            user, age = line.strip().split(',')
            user_ages[user] = int(age)
    return user_ages

def updateuseragefile(filename, user, new_age):
    
    user_ages = readuseragefile(filename)
    user_ages[user] = new_age
    createuseragefile(filename, user_ages)  

def appenduseragefile(filename, user, age):
 
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