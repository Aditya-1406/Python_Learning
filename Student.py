marks = [0]*5

def input_marks():
    
    for i in range(5):
        validate_mark = int(input(f"Enter marks for subject {i+1}: "))
        if 0<=validate_mark<=100:
            marks[i] = validate_mark
        else:
            print("Invalid marks, Retry")
            break
    else:
        print("your report would be generated now")


def average():
    total = sum(marks)
    avg = total / len(marks)
    return avg

def total():
    return sum(marks)

def percentage():
    return (total() / 500) * 100

def grade():
    percent = percentage()
    if percent >= 90:
        return 'A'
    elif percent >= 80:
        return 'B'
    elif percent >= 70:
        return 'C'
    elif percent >= 60:
        return 'D'
    else:
        return 'F'
    
def report():
    input_marks()
    print("Student Report")
    print("--------------"*3)
    for i in range(5):
        print(f"Subject {i+1}: {marks[i]} marks")
    print(f"Total Marks: {total()} out of 500")
    print(f"Average Marks: {average()}")
    print(f"Percentage: {percentage():.2f}%")
    print(f"Grade: {grade()}")
    print(f"Maximum Marks: {max(marks)}")
    print(f"Minimum Marks: {min(marks)}")

if __name__ == "__main__":
    report()