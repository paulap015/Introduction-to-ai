import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    print("\n\n")
    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python shopping.py data [k=1]")
    if len(sys.argv) == 3:
        try:
            k = int(sys.argv[2])
        except ValueError:
            sys.exit("k setting must be an integer")
    else:
        k = 1

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train, k)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")
    
    print("\n\n\n")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    #raise NotImplementedError
    # Dictionary Mapping Months to Numerical values
    months = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}

    # Mapping Visitor Types to integers
    visitors = {'Returning_Visitor': 1, 'New_Visitor': 0, 'Other': 0}

    # Mapping Boolean Strings to integers
    bools = {'TRUE': 1, 'FALSE': 0}

    # Create list of lists for evidence, list for labels:
    evidence = []
    labels = []

    # Open CSV file and load in data as dict:
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')
        print('Loading Data from csv file...')
        lines = 0
        for row in csvreader:

            lines += 1

            line = []

            # Append Evidence to List of Lists
            line.append(int(row['Administrative']))
            line.append(float(row['Administrative_Duration']))
            line.append(int(row['Informational']))
            line.append(float(row['Informational_Duration']))
            line.append(int(row['ProductRelated']))
            line.append(float(row['ProductRelated_Duration']))
            line.append(float(row['BounceRates']))
            line.append(float(row['ExitRates']))
            line.append(float(row['PageValues']))
            line.append(float(row['SpecialDay']))
            line.append(months[row['Month']])
            line.append(int(row['OperatingSystems']))
            line.append(int(row['Browser']))
            line.append(int(row['Region']))
            line.append(int(row['TrafficType']))
            line.append(visitors[row['VisitorType']])
            line.append(bools[row['Weekend']])

            # Add evidence line to evidence
            evidence.append(line)

            # Append Labels to List
            labels.append(bools[row['Revenue']])

        # Confirm data loaded in successfully:
        if len(evidence) != len(labels):
            sys.exit('Error when loading data! Evidence length does not match label length')

        print('Data loaded successfully from csv file! Total lines: ', lines)

        return evidence, labels



def train_model(evidence, labels,k):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    #raise NotImplementedError
    print('Fitting Model using k-Nearest Neighbours Classifier, with k = ', k)

    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    #raise NotImplementedError
    pos_labels = labels.count(1)
    neg_labels = labels.count(0)

    correct_positive = 0
    correct_negative = 0

    for i in range(len(predictions)):
        if predictions[i] == labels[i]:
            if predictions[i] == 1:
                correct_positive += 1
            else:
                correct_negative += 1

    sensitivity = correct_positive / pos_labels
    specificity = correct_negative / neg_labels

    return sensitivity, specificity


if __name__ == "__main__":
    main()
